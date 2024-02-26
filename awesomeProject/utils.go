package main

import (
	"fmt"
	"os"
	"strings"
)

func readDir(path string) ([]string, error) {
	relevantFiles := make([]string, 0)

	entries, err := os.ReadDir(path)
	if err != nil {
		fmt.Printf("error:%v\n", err)
		return nil, fmt.Errorf("Couldn't find files")
	}

	for _, e := range entries {
		fmt.Println(e.Name())
		if e.IsDir() {
			files, err := readDir(path + "/" + e.Name())
			if err != nil || len(files) > 0 {
				relevantFiles = append(relevantFiles, files...)
			}
			continue
		}

		s := strings.Split(e.Name(), ".")
		if len(s) < 2 {
			fmt.Printf("Got an unexpected file name %v. continue\n", e.Name())
			continue
		}
		switch s[1] {
		case "txt":
			relevantFiles = append(relevantFiles, path+"/"+e.Name())
		case "json", "csv", "docx", "pdf":
			fmt.Printf("Got unsupported file type, will be supported in the future: %v\n", e.Name())
		default:
			fmt.Printf("Got an unexpected file type: %v\n", e.Name())
		}

	}
	return relevantFiles, nil
}
