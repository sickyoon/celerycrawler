package main

import (
	"flag"
	"log"
	"math/rand"
	"net"
	"net/http"
	"runtime"
	"strconv"
	"sync"
	"time"

	"golang.org/x/net/netutil"

	"github.com/gorilla/handlers"
	"github.com/julienschmidt/httprouter"
	"github.com/mailru/easyjson"
)

var port = flag.Int("port", 9000, "server port")
var connections = flag.Int("connections", 1000, "number of concurrent connections")

// Payload is json object returned by this benchmark server
// easyjson:json
type Payload struct {
	RandomString string    `json:"random_string"`
	CreatedAt    time.Time `json:"created_at"`
}

var payloadPool = sync.Pool{
	New: func() interface{} {
		return &Payload{}
	},
}

// GetPayload gets Payload struct from sync pool
func GetPayload() *Payload {
	payload := payloadPool.Get().(*Payload)
	payload.RandomString = GenerateRandomString(256)
	payload.CreatedAt = time.Now()
	return payload
}

// RecyclePayload puts back Payload struct into sync pool
func RecyclePayload(payload *Payload) {
	payloadPool.Put(payload)
}

var src = rand.NewSource(time.Now().UnixNano())

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
const (
	letterIdxBits = 6                    // 6 bits to represent a letter index
	letterIdxMask = 1<<letterIdxBits - 1 // All 1-bits, as many as letterIdxBits
	letterIdxMax  = 63 / letterIdxBits   // # of letter indices fitting in 63 bits
)

// GenerateRandomString generates random string of length n
// https://stackoverflow.com/questions/22892120/how-to-generate-a-random-string-of-a-fixed-length-in-golang#31832326
func GenerateRandomString(n int) string {
	b := make([]byte, n)
	for i, cache, remain := n-1, src.Int63(), letterIdxMax; i >= 0; {
		if remain == 0 {
			cache, remain = src.Int63(), letterIdxMax
		}
		if idx := int(cache & letterIdxMask); idx < len(letterBytes) {
			b[i] = letterBytes[idx]
			i--
		}
		cache >>= letterIdxBits
		remain--
	}
	return string(b)
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
	h := handlers.RecoveryHandler()(router)
	//h = handlers.LoggingHandler(os.Stdout, h)
	l, err := net.Listen("tcp", ":"+strconv.Itoa(*port))
	if err != nil {
		log.Fatalf("listening failed %v", err)
	}
	defer l.Close()
	l = netutil.LimitListener(l, *connections)
	log.Printf("Running gocelery benchmark server at port " + strconv.Itoa(*port))
	log.Fatal(http.Serve(l, h))
}
