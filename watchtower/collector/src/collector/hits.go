package collector

import (
	"github.com/garyburd/redigo/redis"
	"github.com/synw/terr"
	influxdb "github.com/synw/watchtower/db"
	"github.com/synw/watchtower/types"
	"strings"
	"sync"
)

func processHits(domain string, db *types.Db, separator string, mutex *sync.Mutex, verbosity int) *terr.Trace {
	// get hits set
	prefix := domain + "_hit*"
	keys, err := redis.Values(conn.Do("KEYS", prefix))
	if err != nil {
		tr := terr.New("db.hits.ProcessHits", err)
		return tr
	}
	var args []interface{}
	for _, k := range keys {
		args = append(args, k)
	}
	if len(keys) > 0 {
		values, err := redis.Strings(conn.Do("MGET", args...))
		if err != nil {
			tr := terr.New("db.hits.ProcessHits", err)
			return tr
		}
		// save the keys into the db
		hits := getHits(values, separator)
		go influxdb.SaveHits(db, hits, mutex, verbosity)
		// delete the recorded keys from Redis
		conn.Send("MULTI")
		for i, _ := range keys {
			conn.Send("DEL", keys[i])
		}
		_, err = conn.Do("EXEC")
		if err != nil {
			tr := terr.New("db.hits.ProcessHits", err)
			return tr
		}
	}
	return nil
}

func getHits(values []string, separator string) []*types.Hit {
	hits := []*types.Hit{}
	for _, doc := range values {
		// unpack the data
		data := strings.Split(doc, separator)
		id := g.Generate()
		hit := &types.Hit{
			id,
			data[0],
			data[1],
			data[2],
			data[3],
			data[4],
			data[5],
			data[6],
			data[7],
			data[8],
			data[9],
			data[10],
			data[11],
			data[12],
			data[13],
			data[14],
			data[15],
			data[16],
			data[17],
		}
		hits = append(hits, hit)
	}
	return hits
}
