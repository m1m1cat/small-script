package colorutil

import "fmt"

// 定义颜色控制符
const (
	red    = "\033[31m"
	green  = "\033[32m"
	yellow = "\033[33m"
	blue   = "\033[34m"
	reset  = "\033[0m" // 恢复默认颜色
)

// 函数用于包装输出并添加颜色
func PrintRed(text string) {
	fmt.Println(red + text + reset)
}

func PrintGreen(text string) {
	fmt.Println(green + text + reset)
}

func PrintYellow(text string) {
	fmt.Println(yellow + text + reset)
}

func PrintBlue(text string) {
	fmt.Println(blue + text + reset)
}
