参考：https://www.yuque.com/aceld/mo95lb/kk9cvo

# GO

## 背景

使用Go：Docker，Go1.5以上也使用Go，Kubernetes（构建在Docker之上的容器调度），codis（redis），etcd

以太坊

并发模型——协程Goroutine

内存分配

垃圾回收

静态链接

标准库

工具链

### 环境、IDE

GoLand远程

一般都使用最新版本的Go

## Go Module

```go
go mod init 	
```

创建一个`go.mod`

相比于 "go path" "go vendor"模式，你的项目可以随意放置，没有路径限制。

```
go mod tidy # 寻找依赖
```





## 包package



（包是一种对函数进行分组的方法，它由同一目录中的所有文件组成）

你必须在第一行指明这个文件属于哪个包。另外，即使你只使用 main 包也不必把所有的代码都写在一个巨大的文件里：你可以用一些较小的文件，并且在每个文件非注释的第一行都使用 `package main` 来指明这些文件都属于 `main` 包。

如果你打算编译包名不是为 main 的源文件，如 `pack1`，编译后产生的对象文件将会是 `pack1.a` 而不是可执行程序。另外要注意的是，所有的包名都应该使用小写字母。

**标准库**：
一般情况下，标准包会存放在 `$GOROOT/pkg/$GOOS_$GOARCH/` 目录下。



**如果对一个包进行更改或重新编译，所有引用了这个包的客户端程序都必须全部重新编译。**

Go 中的包模型采用了显式依赖关系的机制来达到快速编译的目的，编译器会从后缀名为 `.o` 的对象文件（需要且只需要这个文件）中提取传递依赖类型的信息。

如果 `A.go` 依赖 `B.go`，而 `B.go` 又依赖 `C.go`：

- 编译 `C.go`, `B.go`, 然后是 `A.go`.
- 为了编译 `A.go`, 编译器读取的是 `B.o` 而不是 `C.o`.

这种机制对于编译大型的项目时可以显著地提升编译速度。



### 导出名

 Go 中，如果一个名字以大写字母开头，那么它就是已导出的。

例如，`Pizza` 就是个已导出名，`Pi` 也同样，它导出自 `math` 包。

`pizza` 和 `pi` 并未以大写字母开头，所以它们是未导出的。

在导入一个包时，你只能引用其中已导出的名字。 任何「未导出」的名字在该包外均无法访问。

执行代码，观察错误信息。

要修复错误，请将 `math.pi` 改名为 `math.Pi`，然后再试着执行一次。

## Go main()

在 Go 项目中，可以有多个 `main` 函数，但它们的组织方式使得不会在同一时刻出现冲突。这是因为 `main` 函数的可见性和作用范围依赖于它所在的包和如何运行代码。

Go 项目中最常见的结构是多个包。每个包中的代码是独立的，互不干扰。在 Go 语言中，`main` 函数只对 `package main` 可见，并且只有编译和运行 `package main` 时，才会调用这个 `main` 函数。

只有 `package main` 中的 `main` 函数会在程序启动时被调用！！

举例：

```bash
project/
├── cmd/
│   ├── tool1/
│   │   └── main.go (package main, contains main())
│   └── tool2/
│       └── main.go (package main, contains main())
└── pkg/
    └── somepackage/
        └── other.go (package somepackage, contains other code)
```

在这个例子中，`cmd/tool1` 和 `cmd/tool2` 都有自己的 `main.go` 文件，每个文件都定义了 `main` 函数，并且每个 `main` 函数位于 `package main` 中。你可以分别编译这两个文件生成两个不同的可执行文件（`tool1` 和 `tool2`）。

**不同的可执行文件**

在一个项目中，如果你想生成多个可执行文件，每个可执行文件都有自己的 `main` 函数。常见的做法是将不同的程序逻辑放在不同的子目录（如 `cmd` 目录）中，每个子目录中有一个 `main.go` 文件。

例如，一个项目可能有多个命令行工具，每个工具都有一个独立的 `main` 函数。你可以根据需求编译和运行这些工具，而它们不会互相冲突。

**单一编译目标**

Go 的编译器在编译时只会选择一个 `package main` 进行编译。因此，即使项目中有多个 `main` 函数，编译器会根据你指定的路径或文件来选择要编译的 `main` 函数。

例如：

```bash
go run ./cmd/tool1  # 编译并运行 cmd/tool1 目录下的 main 函数
go run ./cmd/tool2  # 编译并运行 cmd/tool2 目录下的 main 函数
```

每个命令都会编译并运行相应目录中的 `main` 函数，而不会混淆多个 `main` 函数。



## 调试

应用程序的开发过程中调试是必不可少的一个环节，因此有一个好的调试器是非常重要的，可惜的是，Go 在这方面的发展还不是很完善。目前可用的调试器是 gdb，最新版均以内置在集成开发环境 LiteIDE 和 GoClipse 中，但是该调试器的调试方式并不灵活且操作难度较大。

如果你不想使用调试器，你可以按照下面的一些有用的方法来达到基本调试的目的：

1. 在合适的位置使用打印语句输出相关变量的值（`print`/`println` 和 `fmt.Print`/`fmt.Println`/`fmt.Printf`）。
2. 在 `fmt.Printf` 中使用下面的说明符来打印有关变量的相关信息：
   - `%+v` 打印包括字段在内的实例的完整信息
   - `%#v` 打印包括字段和限定类型名称在内的实例的完整信息
   - `%T` 打印某个类型的完整说明
3. 使用 `panic()` 语句（[第 13.2 节](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/13.2.md)）来获取栈跟踪信息（直到 `panic()` 时所有被调用函数的列表）。
4. 使用关键字 `defer` 来跟踪代码执行过程（[第 6.4 节](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/06.4.md)）。



## Go run

```
go run mrsequential.go ws.so pg*.txt
```

这个命令是在Linux或类Unix操作系统的终端中使用的，它使用Go语言编写的程序来处理文件。下面是命令各部分的解释：

综上所述，这个命令的意思是编译并运行`mrsequential.go`这个Go程序，并且将`ws.so`和所有匹配`pg*.txt`模式的文本文件作为参数传递给这个程序。程序可能会对这些文件进行某种处理，具体取决于`mrsequential.go`中编写的代码。

复制再试一次分享

# 基本语法



## 函数

一个最简单的函数，（Go是后写返回值类型的）

```Go
func add(x, y int) int {
	return x + y
}
```



当连续两个或多个函数的已命名形参类型相同时，除最后一个类型以外，其它都可以省略。如:

```go
func add(x, y int) int {
	return x + y
}

```

**多返回值**

Go函数可以返回任意数量的返回值。

```go
func swap(x, y string) (string, string) {
	return y, x
}
```

`swap` 函数返回了两个字符串。

注意，这里的返回值处，只写了类型，没命名。

**在函数首行命名返回值**

```go
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}
```

没有参数的 `return` 语句会直接返回已命名的返回值，也就是「裸」返回值。

裸返回语句应当仅用在下面这样的短函数中。在长的函数中它们会影响代码的可读性





包级方法，（普通的函数）

```Go
func NewDBFile(path string) (*DBFile, error) {
    // ...
}
```

因为它不属于任何特定类型。它可以直接在包中调用。

带接受器的方法

func后面加括号，`df DBFile` 部分称为接收器。它指定了该方法可以作用于 `DBFile` 类型的实例。

```Go
type DBFile struct {
    // ...
}

func (df DBFile) Read(offset int64) (*Entry, error) {
    // ...
}

func (df DBFile) Write(e *Entry) error {
    // ...
}func (df DBFile) Read(offset int64) (*Entry, error) {
    // ...
}
```

**何时使用带接收器的方法和包级方法**

通常，当方法需要访问接收器类型的状态或字段时，应使用带接收器的方法。例如，`Read` 方法需要访问 `DBFile` 实例的 `Offset` 字段。

当方法不需要访问接收器类型的状态或字段时，可以使用包级方法。例如，`NewDBFile` 方法不需要访问 `DBFile` 实例的任何状态或字段。

**注意：**

- 带接收器的方法和包级方法都可以是并发安全的或非并发安全的。
- 带接收器的方法可以通过指针接收器或值接收器定义。



## 变量

### 变量的初始化

变量声明可以包含初始值，每个变量对应一个。

如果提供了初始值，则类型可以省略，变量会从初始值中推断出类型。

```go
package main

import "fmt"

var i, j int = 1, 2 //变量声明可以包含初始值，每个变量对应一个。

func main() {
	var c, python, java = true, false, "no!" // 提供了初始值，自动推断出类型。
	
	fmt.Println(i, j, c, python, java)
}

```

### 短赋值语句 `:=`

```Go
//也可以省去var关键字，用`:=`创建并赋值
e := 100        //创建并赋值
```

 Go规定，函数外的每个语句都 **必须** 以关键字开始（`var`、`func` 等），因此 `:=` 结构不能在函数外使用。



### 变量类型

```go
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // uint8 的别名

rune // int32 的别名
     // 表示一个 Unicode 码位

float32 float64

complex64 complex128
```

`int`、`uint` 和 `uintptr` 类型在 32-位系统上通常为 32-位宽，在 64-位系统上则为 64-位宽。当你需要一个整数值时应使用 `int` 类型， 除非你有特殊的理由使用固定大小或无符号的整数类型。



```go
package main

import (
	"fmt"
	"math/cmplx"
)

// 用var成组声明
var ( 
	ToBe bool = false 
	MaxInt uint64 = 1<<64 -1 
	z complex128 = cmplx.Sqrt(-5 + 12 i) 
)

// %T 类型， %v 值
func main() {
	fmt.Printf("类型：%T 值：%v\n", ToBe, ToBe)
	fmt.Printf("类型：%T 值：%v\n", MaxInt, MaxInt)
	fmt.Printf("类型：%T 值：%v\n", z, z)
}

```



### 常量

**iota**

用const来成组地声明常量

const（）可以定义枚举类型，其中iota，**每行**会自动+1

```go
const（
	//在cosnt（）中添加关键字iota，它的初始值=0,每行会自动+1
	BEIJING = iota
	SHANGHAI 	//iota=1
	SHENZHEN	//iota=2
）
//改成10*iota：0 10 20
```

**数值常量**

数值常量是高精度的 **值**。

一个未指定类型的常量由上下文来决定其类型。

（`int` 类型可以存储最大 64 位的整数，根据平台不同有时会更小。）



## for循环

基本的 `for` 循环由三部分组成，它们用分号隔开：

- 初始化语句：在第一次迭代前执行
- 条件表达式：在每次迭代前求值
- 后置语句：在每次迭代的结尾执行

初始化语句通常为一句短变量声明，该变量声明仅在 `for` 语句的作用域中可见。

**注意：**和 C、Java、JavaScript 之类的语言不同，Go 的 `for` 语句后面的三个构成部分外没有小

括号， 大括号 `{ }` 则是必须的。



**省略**

```go
// 初始化语句和后置语句是可选的。
for ; sum < 1000; {
		sum += sum
	}
// 此时也可以去掉分号:
for sum < 1000 {
		sum += sum
	}
```

因此：“ C 的 `while` 在 Go 中叫做 `for`”。



**无限循环**

如果省略循环条件，该循环就不会结束，因此无限循环可以写得很紧凑。

## if判断

Go 的 `if` 语句与 `for` 循环类似，表达式外无需小括号 `( )`，而大括号 `{ }` 则是必须的。



和 `for` 一样，`if` 语句可以在条件表达式前执行一个简短语句。

该语句声明的变量作用域仅在 `if` 之内。

```go
if v := math.Pow(x, n); v < lim {
		return v
	}
```



#### 基于计数器的迭代

```go
package main

import "fmt"

func main() {
	for i := 0; i < 5; i++ {
		fmt.Printf("This is the %d iteration\n", i)
	}
}
```

#### 基于条件判断的迭代

也可以认为这是没有初始化语句和修饰语句的 for 结构，因此 `;;` 便是多余的了。

```go
package main

import "fmt"

func main() {
	var i int = 5 

	for i >= 0 {
		i = i - 1
		fmt.Printf("The variable i is now: %d\n", i)
	}
}
```

####  for-range 结构

这是 Go 特有的一种的迭代结构，可以迭代任意一个集合。（包括数组、字符串和 `map`等）

- `range s` 生成的是字符串中每个字符的索引和该位置的字符值（Unicode code points，而非字节）。

要注意的是，`val` 始终为集合中对应索引的值拷贝，因此它一般只具有只读性质，对它所做的任何修改都不会影响到集合中原有的值（**译者注：如果 `val` 为指针，则会产生指针的拷贝，依旧可以修改集合中的原值**）。





字符串是由字节（byte）序列组成的。每个字节是一个 `uint8` 类型。然而，当你使用 `for range` 遍历一个字符串时，字符串会被解码为 Unicode 码点，每个码点是一个 `rune` 类型。（`rune` 是 `int32` 的）

这样做的好处：当你在 Go 语言中使用 `for range` 遍历字符串 `"hello, 世界"` 时，循环会正确地迭代每个 Unicode 字符，而不仅仅是字节。这意味着对于字符串中的每个中文字符，如 `"世"` 和 `"界"`，尽管它们各自由三个字节组成（在 UTF-8 编码中），`for range` 循环会正确地将它们作为单个字符处理。



- string()
- stringconv.Itoa ()
- 



## 数组

```Go
package main

import (
	"fmt"
)

func main() {
	//一维数组
	var arr_1 [5] int
	fmt.Println(arr_1)

	var arr_2 =  [5] int {1, 2, 3, 4, 5}
	fmt.Println(arr_2)

	arr_3 := [5] int {1, 2, 3, 4, 5}
	fmt.Println(arr_3)

	arr_4 := [...] int {1, 2, 3, 4, 5, 6}
	fmt.Println(arr_4)

	arr_5 := [5] int {0:3, 1:5, 4:6}
	fmt.Println(arr_5)

	//二维数组
	var arr_6 = [3][5] int {{1, 2, 3, 4, 5}, {9, 8, 7, 6, 5}, {3, 4, 5, 6, 7}}
	fmt.Println(arr_6)

	arr_7 :=  [3][5] int {{1, 2, 3, 4, 5}, {9, 8, 7, 6, 5}, {3, 4, 5, 6, 7}}
	fmt.Println(arr_7)

	arr_8 :=  [...][5] int {{1, 2, 3, 4, 5}, {9, 8, 7, 6, 5}, {0:3, 1:5, 4:6}}
	fmt.Println(arr_8)
}
```

数组是值类型问题，在函数中传递的时候是传递的值，如果传递数组很大，这对内存是很大开销。

## 切片

### 切片的内部结构

一个切片由三个主要部分组成：

- **指针**：指向底层数组中切片的第一个元素。
- **长度**：切片中元素的数量。
- **容量**：从切片的开始位置到底层数组末尾的元素数量。

当你执行 `stack = stack[:len(stack)-1]` 时，你实际上只是在减少切片的长度部分，而不是改变底层数组或进行内存操作。底层数组并未被修改或重新分配，只是切片视图的边界发生了变化。



切片是一种动态数组，比数组操作灵活，长度不是固定的，可以进行追加和删除。

`len()` 和 `cap()` 返回结果可相同和不同。

```Go
//demo_7.go
package main

import (
	"fmt"
)

func main() {
	var sli_1 [] int      //nil 切片
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_1),cap(sli_1),sli_1)

	var sli_2 = [] int {} //空切片
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_1),cap(sli_2),sli_2)

	var sli_3 = [] int {1, 2, 3, 4, 5}
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_3),cap(sli_3),sli_3)

	sli_4 := [] int {1, 2, 3, 4, 5}
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_4),cap(sli_4),sli_4)

	var sli_5 [] int = make([] int, 5, 8)
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_5),cap(sli_5),sli_5)

	sli_6 := make([] int, 5, 9)
	fmt.Printf("len=%d cap=%d slice=%v\n",len(sli_6),cap(sli_6),sli_6)
}
```







## Struct结构体



## nil

#### errors.New()

```Go
return nil, errors.New("m needs 2^n")
```

在Go语言中，`nil`是一个常量，表示空指针或空值。它可以用于任何类型的变量或表达式，并且通常用于表示某个值不存在或未初始化。



其中`errors.New()`是一个Go标准库中的函数，它会创建一个包含指定错误信息的新error对象。

具体地说，`errors.New("m needs 2^n")`会创建一个新的error对象，并将错误信息设置为"m needs 2^n"。然后，该error对象会作为第二个返回值被传递给构造函数的调用方。

在Go语言中，函数可以返回多个值。如果某个函数需要返回错误信息，通常会将其作为最后一个返回值。调用方可以通过检查返回值中的错误对象来确定函数是否执行成功。如果没有发生错误，则错误对象为nil；否则，错误对象将包含相关的错误信息。




# 编写测试

以 `_test.go`结尾文件名会告诉命令该文件包含测试函数。





# 常用包

## strings 和 strconv 包

1. strings.HasPrefix(s, prefix string) bool 
2. strings.HasSuffix(s, suffix string) bool
3. strings.Contains(s, substr string) bool
4. strings.Index(s, str string) int 
5. 



### 前缀和后缀

`HasPrefix()` 判断字符串 `s` 是否以 `prefix` 开头：

```go
strings.HasPrefix(s, prefix string) bool
```



`HasSuffix()` 判断字符串 `s` 是否以 `suffix` 结尾：

```go
strings.HasSuffix(s, suffix string) bool
```

## GO项目布局

GO没有规范项目，但是GO本身主要是GO编写的，可以参考。

- cmd 可执行程序入口，只放一个main.go代码
- internal 项目自己的包定义，不能被外部引用
- common 可以共用的基本服务，自定义的框架，包含 net、job等子目录
- etc 配置文件 config.yaml



# Go网盘

github项目地址 https://github.com/GetcharZp/cloud-disk

博客：https://blog.csdn.net/weixin_43734095/article/details/124927942



# miniDB





# Gin

# go-zero

goctl（gocontrol）是go-zero微服务框架下的代码生成工具。

**https://go-zero.dev/cn/docs/goctl/goctl**
