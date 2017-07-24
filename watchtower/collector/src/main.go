package main

import (
	"flag"
	"fmt"
	"github.com/synw/watchtower/collector"
	"github.com/synw/watchtower/db"
	"github.com/synw/watchtower/types"
	"strconv"
	"time"
)

var verbosityS = flag.String("v", "0", "Verbosity")
var redisAddr = flag.String("ra", "localhost", "Redis address")
var redisDbS = flag.String("rdb", "0", "Redis database")
var dbAddr = flag.String("ia", "localhost", "Influxdb address")
var dbUser = flag.String("iu", "", "Influxdb user")
var dbPwd = flag.String("ip", "", "Influxdb password")
var dbEvents = flag.String("ine", "", "Influxdb database for events")
var dbHits = flag.String("inh", "", "Influxdb database for hits")
var freqS = flag.String("f", "5", "Frequency")
var sep = flag.String("s", "#!#", "Separator")
var domain = flag.String("d", "", "Domain name")

func main() {
	flag.Parse()
	verbosity, err := strconv.Atoi(*verbosityS)
	if err != nil {
		fmt.Println("Unable to convert flag")
	}
	redisDbNum, err := strconv.Atoi(*redisDbS)
	if err != nil {
		fmt.Println("Unable to convert flag")
	}
	freq, err := strconv.Atoi(*freqS)
	if err != nil {
		fmt.Println("Unable to convert flag")
	}
	// verify conf
	if *dbUser == "" {
		fmt.Println("Unable to initialize database: username is missing")
		return
	}
	if *dbPwd == "" {
		fmt.Println("Unable to initialize database: password is missing")
		return
	}
	if *dbHits == "" {
		fmt.Println("Unable to initialize database: database for hits is missing")
		return
	}
	if *dbEvents == "" {
		fmt.Println("Unable to initialize database: database for events is missing")
		return
	}
	if *domain == "" {
		fmt.Println("Unable to initialize collector: domain name is missing")
		return
	}
	// init db
	influxDb := &types.Db{*dbAddr, *dbUser, *dbPwd, *dbHits, *dbEvents}
	tr := db.Init(influxDb, verbosity)
	if tr != nil {
		tr.Print()
		return
	}
	// init collector
	redisDb := &types.RedisDb{*redisAddr, redisDbNum}
	collector.Init(redisDb)
	if tr != nil {
		tr.Print()
		return
	}
	// run
	if verbosity > 1 {
		fmt.Println("Hits database:", *dbHits)
		fmt.Println("Events database:", *dbEvents)
	}
	tr = collector.ProcessData(*domain, influxDb, *sep, verbosity)
	if tr != nil {
		tr.Print()
		return
	}
	for {
		duration := time.Duration(freq) * time.Second
		for range time.Tick(duration) {
			tr := collector.ProcessData(*domain, influxDb, *sep, verbosity)
			if tr != nil {
				tr.Print()
				return
			}
		}
	}
}
