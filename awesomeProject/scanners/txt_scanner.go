package scanners

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
)

type texScanner struct {
	reg        *regexp.Regexp // insensitive
	patternLen int
}

func NewTextScanner() (*texScanner, error) {
	// TODO: How to get the pattern
	pattern := "A1a2SS"
	reg, err := regexp.Compile("(?i)" + pattern)
	if err != nil {
		return nil, fmt.Errorf("couldn't compile pattern %v. err: %v", pattern, err)
	}
	return &texScanner{reg, len(pattern)}, nil
}

func (tR *texScanner) Scan(path string) bool {
	// Open the file for reading
	file, err := os.Open(path)
	if err != nil {
		fmt.Printf("Couldn't open %v file. error:%v", path, err)
		return false
	}
	defer file.Close()

	// Create a buffered reader
	reader := bufio.NewReader(file)

	// Read the file in 4-byte chunks
	chunkSize := 100

	// TODO: Please pay attention that end of chunk & start of another can match the pattern
	for {

		// Read the next chunk
		chunk := make([]byte, chunkSize)
		n, err := reader.Read(chunk)

		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			log.Fatal(err)
		}

		// Print the chunk
		fmt.Printf("%s\n", chunk[:n])

		if tR.reg.Match(chunk) {
			fmt.Printf("Match\n")
			return true
		}

		// Check for EOF
		if err == nil && n < chunkSize {
			break
		}
	}
	return false
}
