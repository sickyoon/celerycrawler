package main

import (
	"flag"
	"log"
	"net"
	"net/http"
	"runtime"
	"strconv"
	"sync"
	"time"

	"golang.org/x/net/netutil"

	"github.com/julienschmidt/httprouter"
	"github.com/mailru/easyjson"
)

var port = flag.Int("port", 9000, "server port")
var connections = flag.Int("connections", 1000, "number of concurrent connections")

// Payload is json object returned by this benchmark server
// easyjson:json
type Payload struct {
	Data      []byte    `json:"random_byte"`
	CreatedAt time.Time `json:"created_at"`
}

var payloadPool = sync.Pool{
	New: func() interface{} {
		return &Payload{}
	},
}

// GetPayload gets Payload struct from sync pool
func GetPayload() *Payload {
	payload := payloadPool.Get().(*Payload)
	payload.Data = []byte("Hello World!")
	payload.CreatedAt = time.Now()
	return payload
}

// RecyclePayload puts back Payload struct into sync pool
func RecyclePayload(payload *Payload) {
	payloadPool.Put(payload)
}

func init() {
	runtime.GOMAXPROCS(runtime.NumCPU())
}

func jsonResponse(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	payload := GetPayload()
	easyjson.MarshalToHTTPResponseWriter(payload, w)
	RecyclePayload(payload)
}

func main() {
	flag.Parse()
	router := httprouter.New()
	router.GET("/json", jsonResponse)
	l, err := net.Listen("tcp", ":"+strconv.Itoa(*port))
	if err != nil {
		log.Fatalf("listening failed %v", err)
	}
	defer l.Close()
	l = netutil.LimitListener(l, *connections)
	log.Printf("Running gocelery benchmark server at port " + strconv.Itoa(*port))
	log.Fatal(http.Serve(l, router))
}
