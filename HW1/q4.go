package main

import (
	"fmt"
)

var secretChannel chan byte

func sender(message string) {
	bytes := []byte(message)
	for _, b := range bytes {
		secretChannel <- b
	}
	close(secretChannel)
}

func receiver() string {
	var message []byte
	for b := range secretChannel {
		message = append(message, b)
	}
	return string(message)
}

func main() {
	secretChannel = make(chan byte, 1024)

	go sender("Hello, this is a secret message!")

	fmt.Println("Received secret message:", receiver())
}
