package collector

import (
	"github.com/SKAhack/go-shortid"
	"github.com/garyburd/redigo/redis"
	"github.com/synw/terr"
	"github.com/synw/watchtower/types"
	"sync"
)

var conn redis.Conn
var g = shortid.Generator()

func Init(rdb *types.RedisDb) *terr.Trace {
	var tr *terr.Trace
	conn, tr = connect(rdb)
	if tr != nil {
		tr = terr.Pass("collector.Init", tr)
		return tr
	}
	return nil
}

func ProcessData(domain string, db *types.Db, separator string, verbosity int) *terr.Trace {
	var mutex = &sync.Mutex{}
	tr := processHits(domain, db, separator, mutex, verbosity)
	if tr != nil {
		tr := terr.Pass("collector.ProcessData", tr)
		return tr
	}
	tr = processEvents(domain, db, separator, mutex, verbosity)
	if tr != nil {
		tr := terr.Pass("collector.ProcessData", tr)
		return tr
	}
	return nil
}

func connect(rdb *types.RedisDb) (redis.Conn, *terr.Trace) {
	conn, err := redis.Dial("tcp", rdb.Addr)
	if err != nil {
		tr := terr.New("collector.connect", err)
		return conn, tr
	}
	return conn, nil
}
