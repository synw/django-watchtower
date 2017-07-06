package db

import (
	"fmt"
	"github.com/influxdata/influxdb/client/v2"
	"github.com/synw/terr"
	"github.com/synw/watchtower/types"
	"sync"
	"time"
)

var cli client.Client

func Init(db *types.Db) *terr.Trace {
	var err error
	// influxdb
	addr := "http://" + db.Addr
	cli, err = client.NewHTTPClient(client.HTTPConfig{
		Addr:     addr,
		Username: db.User,
		Password: db.Pwd,
	})
	if err != nil {
		tr := terr.New("db.Init", err)
		return tr
	}
	return nil
}

func SaveEvents(db *types.Db, events []*types.Event, domain string, mutex *sync.Mutex, verbosity int) (int, *terr.Trace) {
	t1 := time.Now()
	num := 0
	// Create a new point batch
	bp, err := client.NewBatchPoints(client.BatchPointsConfig{
		Database:  db.Events,
		Precision: "ms",
	})
	if err != nil {
		tr := terr.New("db.SaveEvents", err)
		return num, tr
	}
	// Create a point and add to batch
	tags := make(map[string]string)
	for _, event := range events {
		tags = map[string]string{
			"service":      event.Service,
			"domain":       domain,
			"name":         event.Name,
			"class":        event.Class,
			"obj_pk":       event.ObjPk,
			"content_type": event.ContentType,
			"user":         event.User,
			"url":          event.Url,
			"admin_url":    event.AdminUrl,
			"notes":        event.Notes,
			"request":      event.Request,
			"bucket":       event.Bucket,
			"data":         event.Data,
		}
		fields := map[string]interface{}{
			"num": 1,
		}
		pt, err := client.NewPoint("event", tags, fields, time.Now())
		if err != nil {
			tr := terr.New("db.SaveEvents", err)
			return num, tr
		}
		bp.AddPoint(pt)
		num++
	}
	// Write the batch
	mutex.Lock()
	if err := cli.Write(bp); err != nil {
		tr := terr.New("db.SaveEvents", err)
		return 0, tr
	}
	mutex.Unlock()
	// metrics
	t2 := time.Since(t1)
	if verbosity > 1 {
		if num > 0 {
			t := time.Now()
			strt := t.Format("15:04:05")
			fmt.Println(strt, "Saved", num, "events in the database in", t2)
		}
	}
	return num, nil
}

func SaveHits(db *types.Db, hits []*types.Hit, mutex *sync.Mutex, verbosity int) (int, *terr.Trace) {
	t1 := time.Now()
	num := 0
	// Create a new point batch
	bp, err := client.NewBatchPoints(client.BatchPointsConfig{
		Database:  db.Hits,
		Precision: "ms",
	})
	if err != nil {
		tr := terr.New("db.SaveHits", err)
		return num, tr
	}
	// Create a point and add to batch
	tags := make(map[string]string)
	for _, hit := range hits {
		tags = map[string]string{
			"service":       "hitsmon",
			"domain":        hit.Domain,
			"user":          hit.User,
			"path":          hit.Path,
			"referer":       hit.Referer,
			"user_agent":    hit.UserAgent,
			"method":        hit.Method,
			"authenticated": hit.IsAuthenticated,
			"staff":         hit.IsStaff,
			"superuser":     hit.IsSuperuser,
			"status_code":   hit.StatusCode,
			"view":          hit.View,
			"module":        hit.Module,
			"ip":            hit.Ip,
		}
		fields := map[string]interface{}{
			"num":            1,
			"request_time":   hit.RequestTime,
			"content_length": hit.ContentLength,
			"num_queries":    hit.NumQueries,
			"queries_time":   hit.QueriesTime,
		}
		pt, err := client.NewPoint("hits", tags, fields, time.Now())
		if err != nil {
			tr := terr.New("db.SaveHits", err)
			return num, tr
		}
		bp.AddPoint(pt)
		num++
	}
	// Write the batch
	mutex.Lock()
	if err := cli.Write(bp); err != nil {
		tr := terr.New("db.SaveHits", err)
		return 0, tr
	}
	mutex.Unlock()
	// metrics
	t2 := time.Since(t1)
	if verbosity > 1 {
		if num > 0 {
			t := time.Now()
			strt := t.Format("15:04:05")
			fmt.Println(strt, "Saved", num, "hits in the database in", t2)
		}
	}
	return num, nil
}
