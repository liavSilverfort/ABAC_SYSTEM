package main

import (
	"awesomeProject/scanners"
	"fmt"
	"os"
)

func main() {
	fmt.Printf("aaaaaaa -> %v\n", os.Args)
	if len(os.Args) != 2 {
		fmt.Printf("Unexpected number of args %v\n", os.Args)
	}
	path := os.Args[1]

	files, err := readDir(path)
	if err != nil {
		fmt.Printf("Couldn't find files in the path: %v. error: %v\n", path, err)
	}
	fmt.Printf("%v\n", files)

	txtScanner, err := scanners.NewTextScanner()
	if err != nil {
		fmt.Printf(err.Error())
		return
	}

	for _, filePath := range files {
		fmt.Printf("%v\n", filePath)
		if txtScanner.Scan(filePath) {
			fmt.Printf("yes\n")
		}
	}

}
