package scanners

//
//import (
//	"fmt"
//	"github.com/dslipak/pdf"
//	"regexp"
//)
//
//type pdfScanner struct {
//	reg        *regexp.Regexp // insensitive
//	patternLen int
//}
//
//func NewPdfScanner() (*pdfScanner, error) {
//	// TODO: How to get the pattern
//	pattern := "A1a2SS"
//	reg, err := regexp.Compile("(?i)" + pattern)
//	if err != nil {
//		return nil, fmt.Errorf("couldn't compile pattern %v. err: %v", pattern, err)
//	}
//	return &pdfScanner{reg, len(pattern)}, nil
//}
//
//func (tR *texScanner) Scan(path string) bool {
//	r, err := pdf.Open(path)
//	defer func() {
//		_ = r.f.Close()
//	}()
//	if err != nil {
//		return "", err
//	}
//	totalPage := r.NumPage()
//
//	for pageIndex := 1; pageIndex <= totalPage; pageIndex++ {
//		p := r.Page(pageIndex)
//		if p.V.IsNull() {
//			continue
//		}
//
//		rows, _ := p.GetTextByRow()
//		for _, row := range rows {
//			println(">>>> row: ", row.Position)
//			for _, word := range row.Content {
//				fmt.Println(word.S)
//			}
//		}
//	}
//	return "", nil
//
//	return false
//}
