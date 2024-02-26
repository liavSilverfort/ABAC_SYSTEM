package scanners

type FileScanner interface {
	Scan(path string) bool
}
