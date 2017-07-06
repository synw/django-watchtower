package collector

import (
	"github.com/garyburd/redigo/redis"
	"github.com/synw/terr"
	influxdb "github.com/synw/watchtower/db"
	"github.com/synw/watchtower/types"
	"strings"
	"sync"
)

func processEvents(domain string, db *types.Db, separator string, mutex *sync.Mutex, verbosity int) *terr.Trace {
	// get hits set
	prefix := domain + "_event*"
	keys, err := redis.Values(conn.Do("KEYS", prefix))
	if err != nil {
		tr := terr.New("collector.events.processEvents", err)
		return tr
	}
	var args []interface{}
	for _, k := range keys {
		args = append(args, k)
	}
	if len(keys) > 0 {
		values, err := redis.Strings(conn.Do("MGET", args...))
		if err != nil {
			tr := terr.New("collector.events.processEvents", err)
			return tr
		}
		// save the keys into the db
		events := getEvents(values, separator)
		go influxdb.SaveEvents(db, events, domain, mutex, verbosity)
		// delete the recorded keys from Redis
		conn.Send("MULTI")
		for i, _ := range keys {
			conn.Send("DEL", keys[i])
		}
		_, err = conn.Do("EXEC")
		if err != nil {
			tr := terr.New("collector.events.processEvents", err)
			return tr
		}
	}
	return nil
}

func getEvents(values []string, separator string) []*types.Event {
	events := []*types.Event{}
	for _, doc := range values {
		// unpack the data
		data := strings.Split(doc, separator)
		event := &types.Event{
			Id:      g.Generate(),
			Service: "watchtower",
		}
		for _, el := range data {
			kv := strings.Split(el, ":;")
			k := kv[0]
			v := kv[1]
			if k == "name" {
				event.Name = v
			} else if k == "event_class" {
				event.Class = v
			} else if k == "content_type" {
				event.ContentType = v
			} else if k == "obj_pk" {
				event.ObjPk = v
			} else if k == "url" {
				event.Url = v
			} else if k == "user" {
				event.User = v
			} else if k == "note" {
				event.Notes = v
			} else if k == "request" {
				event.Request = v
			} else if k == "bucket" {
				event.Bucket = v
			} else if k == "data" {
				event.Data = v
			}
		}
		events = append(events, event)
	}
	return events
}
