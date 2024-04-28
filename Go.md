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

一般都使用最新版本的Go、

## Go Module

```go
go mod init 	
```

创建一个`go.mod`

相比于 "go path" "go vendor"模式，你的项目可以随意放置，没有路径限制。



## Go的结构和要素

### package

你必须在源文件中非注释的第一行指明这个文件属于哪个包。另外，即使你只使用 main 包也不必把所有的代码都写在一个巨大的文件里：你可以用一些较小的文件，并且在每个文件非注释的第一行都使用 `package main` 来指明这些文件都属于 `main` 包。

如果你打算编译包名不是为 main 的源文件，如 `pack1`，编译后产生的对象文件将会是 `pack1.a` 而不是可执行程序。另外要注意的是，所有的包名都应该使用小写字母。

**标准库**：
一般情况下，标准包会存放在 `$GOROOT/pkg/$GOOS_$GOARCH/` 目录下。



**如果对一个包进行更改或重新编译，所有引用了这个包的客户端程序都必须全部重新编译。**

Go 中的包模型采用了显式依赖关系的机制来达到快速编译的目的，编译器会从后缀名为 `.o` 的对象文件（需要且只需要这个文件）中提取传递依赖类型的信息。

如果 `A.go` 依赖 `B.go`，而 `B.go` 又依赖 `C.go`：

- 编译 `C.go`, `B.go`, 然后是 `A.go`.
- 为了编译 `A.go`, 编译器读取的是 `B.o` 而不是 `C.o`.

这种机制对于编译大型的项目时可以显著地提升编译速度。













### 调试

应用程序的开发过程中调试是必不可少的一个环节，因此有一个好的调试器是非常重要的，可惜的是，Go 在这方面的发展还不是很完善。目前可用的调试器是 gdb，最新版均以内置在集成开发环境 LiteIDE 和 GoClipse 中，但是该调试器的调试方式并不灵活且操作难度较大。

如果你不想使用调试器，你可以按照下面的一些有用的方法来达到基本调试的目的：

1. 在合适的位置使用打印语句输出相关变量的值（`print`/`println` 和 `fmt.Print`/`fmt.Println`/`fmt.Printf`）。
2. 在 `fmt.Printf` 中使用下面的说明符来打印有关变量的相关信息：
   - `%+v` 打印包括字段在内的实例的完整信息
   - `%#v` 打印包括字段和限定类型名称在内的实例的完整信息
   - `%T` 打印某个类型的完整说明
3. 使用 `panic()` 语句（[第 13.2 节](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/13.2.md)）来获取栈跟踪信息（直到 `panic()` 时所有被调用函数的列表）。
4. 使用关键字 `defer` 来跟踪代码执行过程（[第 6.4 节](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/06.4.md)）。



## 常量变量

#### 变量声明

```Go
var a int 		//默认0

var a int = 100 //赋初值

var c = 100 	//自动

//也可以省去var关键字，用`:=`创建并赋值
e := 100        //创建并赋值
```



#### const（）与iota

var 替换为  const来声明常量

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





## for循环

#### 基于计数器的迭代

```go\
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

#### 死循环

一般情况下都会直接写 `for { }`。

####  for-range 结构

这是 Go 特有的一种的迭代结构，可以迭代任意一个集合。（包括数组、字符串和 `map`等）

要注意的是，`val` 始终为集合中对应索引的值拷贝，因此它一般只具有只读性质，对它所做的任何修改都不会影响到集合中原有的值（**译者注：如果 `val` 为指针，则会产生指针的拷贝，依旧可以修改集合中的原值**）。



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



## 函数

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





## strings 和 strconv 包

1. strings.HasPrefix(s, prefix string) bool 
2. strings.HasSuffix(s, suffix string) bool
3. strings.Contains(s, substr string) bool
4. strings.Index(s, str string) int 
5. 





## 前缀和后缀



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

https://go-zero.dev/cn/docs/goctl/goctl
