package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

const sharedFileName = "shared_file.txt"

func sender(message string) {
	file, err := os.OpenFile(sharedFileName, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	_, err = file.WriteString(message)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	time.Sleep(100 * time.Millisecond)
}

func receiver() string {
	var message string

	time.Sleep(100 * time.Millisecond)

	data, err := ioutil.ReadFile(sharedFileName)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return ""
	}
	message = string(data)

	return message
}

func main() {
	messageToSend := "Hello, this is a secret message!"

	sender(messageToSend)

	receivedMessage := receiver()

	fmt.Println("Received secret message:", receivedMessage)
}
