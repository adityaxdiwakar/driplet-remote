package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"os/signal"
	"time"

	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loaded environment configuration")
	} else {
		log.Printf("Loaded environment variables successfully")
	}

	authDetails := AuthenticationDetails{
		AuthToken: os.Getenv("ACCESS_TOKEN"),
		UserID:    os.Getenv("CLIENT_ID"),
	}

	authURL := fmt.Sprintf("http://backend.driplet.adi.wtf/endpoints/%s/services", authDetails.UserID)

	client := &http.Client{}
	req, _ := http.NewRequest("GET", authURL, nil)
	req.Header.Set("authorization", string(authDetails.AuthToken))
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal("error: could not retrieve service list")
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal("error: could not retrieve service list")
	}
	var responseServices []APIService

	err = json.Unmarshal(body, &responseServices)
	if err != nil {
		log.Fatal("error: could not retrieve service list")
	}

	for _, service := range responseServices {
		log.Printf("%s", service)
		serverConnect(service, authDetails)
	}
}

var addr = flag.String("addr", "vps.adi.wtf:8000", "http service address")

func serverConnect(service APIService, authDetails AuthenticationDetails) {
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	u := url.URL{Scheme: "ws", Host: *addr, Path: "/ws/server"}
	// log.Printf("Connecting to Tradovate Market Data Socket")

	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Printf("dial:", err)
	} else {
		log.Printf("Received 'Hello' from WS")
	}
	defer c.Close()

	authRequest := ServerAuthRequest{
		AuthToken: authDetails.AuthToken,
		UserID:    authDetails.UserID,
		ServiceID: service.ID,
	}

	c.WriteJSON(authRequest)
	cmd := exec.Command("tail", "-f", "/var/log/nginx/access.log")
	cmdReader, err := cmd.StdoutPipe()
	if err != nil {
		log.Printf("%v", err)
	}
	cmd.Start()

	scanner := bufio.NewScanner(cmdReader)
	go func() {
		for scanner.Scan() {
			c.WriteJSON(ServerPayload{ServiceID: service.ID, Log: scanner.Text(), UserID: authDetails.UserID})
		}
	}()

	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	done := make(chan struct{})

	for {
		defer close(done)
		select {
		case <-done:
			return
		case _ = <-ticker.C:
			err := c.WriteJSON(ServerPayload{ServiceID: service.ID, Heartbeat: true})
			if err != nil {
				return
			}
		case <-interrupt:
			return
		}
	}

}
