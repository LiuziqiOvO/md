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

### 项目结构

通常使用 Go Moudule 模式管理相比于 "go path" "go vendor"模式，你的项目可以随意放置，没有路径限制。



```go
go mod init 	
```

创建一个`go.mod`

**Module**：包含一个或多个包（package）

**package**：

- 包是在单个目录中组织的一组 Go 源文件，包名通常等于文件夹名
- 包可以封装数据和函数，供其他包调用。
- 你必须在源文件中非注释的第一行指明这个文件属于哪个包。



**关于main包：**

另外，即使你只使用 main 包也不必把所有的代码都写在一个巨大的文件里：你可以用一些较小的文件，并且在每个文件非注释的第一行都使用 `package main` 来指明这些文件都属于 `main` 包。

如果你打算编译包名不是为 main 的源文件，如 `pack1`，编译后产生的对象文件将会是 `pack1.a` 而不是可执行程序。另外要注意的是，所有的包名都应该使用小写字母。



**标准库**：
一般情况下，标准包会存放在 `$GOROOT/pkg/$GOOS_$GOARCH/` 目录下。



**包的编译**

如果对一个包进行更改或重新编译，所有引用了这个包的客户端程序都必须全部重新编译。

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

> 使用go Delve调试器在服务器进行远程调试

服务器：

```bash
# dlv 自动编译当前项目的代码，并调试生成的临时二进制文件。
dlv debug --headless --listen=:2345 --api-version=2 --accept-multiclient

# 或者直接运行编译好的可执行文件
dlv --listen=:2345 --headless=true --api-version=2 --accept-multiclient exec ./mrcoordinator pg-*.txt

```

笔记本：.vscode/lanch.json

// 使用上个代码块第二条指令，测试通过。

// 第一条指令要求整个项目里没有报错

```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Connect to server",
            "type": "go",
            "request": "attach",
            "mode": "remote",
            "remotePath": "${workspaceFolder}",
            "port": 2345,
            "host": "221.9.165.166"
        },
        // {
        //     "name": "Attach to Process",
        //     "type": "go",
        //     "request": "attach",
        //     "mode": "local",
        //     "processId": 0
        // },

    ]
}
```



## 常量变量

### 变量声明

```Go
var a int 		//默认0

var a int = 100 //赋初值

var c = 100 	//自动

//也可以省去var关键字，用`:=`创建并赋值
e := 100        //创建并赋值
```



### 变量类型

#### string

字符串是由字节（byte）序列组成的。每个字节是一个 `uint8` 类型。然而，当你使用 `for range` 遍历一个字符串时，字符串会被解码为 Unicode 码点，每个码点是一个 `rune` 类型。（`rune` 是 `int32` 的）

这样做的好处：当你在 Go 语言中使用 `for range` 遍历字符串 `"hello, 世界"` 时，循环会正确地迭代每个 Unicode 字符，而不仅仅是字节。这意味着对于字符串中的每个中文字符，如 `"世"` 和 `"界"`，尽管它们各自由三个字节组成（在 UTF-8 编码中），`for range` 循环会正确地将它们作为单个字符处理。



- string()
- stringconv.Itoa ()
- 



### 其他

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

个人认为：指定长度就是array，不指定就是sclice，二者统称list

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

[ ] , 不指定长度就会变成slice

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

## map

在 Go 中，`map` 是一种内置的数据结构，类似于其他编程语言中的字典或哈希表。它用于存储键值对，具有以下特点：

1. **定义和使用**：
   - 语法格式为：`map[KeyType]ValueType`。
   - 例如：`myMap := make(map[string]int)`，表示键类型为 `string`，值类型为 `int` 的映射。

2. **操作**：
   - **插入/更新**：`myMap["key"] = value`。
   - **获取值**：`val := myMap["key"]`，返回键对应的值，如果不存在则返回零值。
   - **删除**：`delete(myMap, "key")`，用于从 `map` 中移除键值对。
   - **检查存在性**：通过双值获取方式来判断键是否存在：`val, ok := myMap["key"]`，如果存在则 `ok` 为 `true`。

3. **并发**：
   - `map` 在并发环境中并不是线程安全的，通常需要配合 `sync.Mutex` 或使用 `sync.Map` 来保证线程安全。

这种结构可以高效地根据键快速查找、插入和删除对应的值，非常适合用于存储和检索数据。



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

- `range s` 生成的是字符串中每个字符的索引和该位置的字符值（Unicode code points，而非字节）。

要注意的是，`val` 始终为集合中对应索引的值拷贝，因此它一般只具有只读性质，对它所做的任何修改都不会影响到集合中原有的值（**译者注：如果 `val` 为指针，则会产生指针的拷贝，依旧可以修改集合中的原值**）。



## 结构体

结构体声明



```go
type Task struct{
	Id		string 
	Type	TaskType
}
```





type也可直接自定义类型名

```go
type TaskType string

```







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

**包级方法**（普通的函数）

```Go
func NewDBFile(path string) (*DBFile, error) {
    // ...
}
```

因为它不属于任何特定类型。它可以直接在包中调用。



**带接受器的方法**

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

> 这个接收器用指针和用值有什么区别？



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







# 接口





# 锁

Go 中常用的锁类型：

1. **互斥锁 (`sync.Mutex`)**：适用于需要保护共享数据的访问，确保同一时刻只有一个协程能访问共享数据。

   ```go
   var mu sync.Mutex
   mu.Lock()
   // critical section
   mu.Unlock()
   ```

2. **读写锁 (`sync.RWMutex`)**：允许多个读操作同时进行，但写操作是独占的。对于读多写少的场景，使用读写锁可以提高性能。

   ```go
   var rwMu sync.RWMutex
   rwMu.RLock()  // 加读锁
   // critical section (read)
   rwMu.RUnlock()
   
   rwMu.Lock()  // 加写锁
   // critical section (write)
   rwMu.Unlock()
   ```

# Go routine

Goroutine 是 Go 语言中的一种并发机制，它让你可以同时执行多个任务。它类似于操作系统的线程，但更加轻量化。

在 Go 中，启动一个新的 Goroutine 非常简单，只需要在函数调用前加上 `go` 关键字。例如：

```go
go someFunction()
```

​	Goroutine 是非常轻量的，它比传统的线程消耗的资源少得多，因此你可以启动成千上万个 Goroutine，而不用担心内存耗尽。



# Go channel

在 Go 中，`channel`（通道）是一种用于 goroutine 之间通信的机制，允许数据在多个 goroutine 之间安全传递。

**基本属性**

1. **类型化**：通道是类型安全的，声明时需要指定通道传递的数据类型，例如：`chan int` 表示传递 `int` 类型的数据。
2. **同步通信**：通道提供了 goroutine 之间的同步机制。当一个 goroutine 向通道发送数据时，另一个 goroutine 需要读取数据，发送和接收操作是阻塞的。
3. 无缓冲和有缓冲
   - **无缓冲通道**：发送和接收操作需要同时发生，否则 goroutine 会被阻塞。
   - **有缓冲通道**：可以在通道中存储一定数量的数据，发送方在通道未满时不会阻塞，接收方在通道非空时不会阻塞。



在 Go 中，channel 是通过 `chan` 关键字声明的。例如：

```go
ch := make(chan int)
```

这个例子声明了一个可以传递整数的 channel。Goroutine 可以通过这个 channel 发送或接收数据，来同步彼此的工作：

```go
ch <- 42  // 发送数据到 channel
value := <- ch  // 从 channel 接收数据
```



特别适用于生产者-消费者模式，协调多个 goroutine 之间的工作，保证线程安全的数据传递。



**select用法**

`select` 语法用于从多个通道（`channel`）中等待数据，可以让代码同时监听多个通道的操作。`select` 语法就像是一个通道的 `switch` 语句。

- 每个 `case` 都是对一个通道操作的描述（接收或发送）。
- `select` 会阻塞，直到某个 `case` 中的通道操作可以进行。
- 如果多个 `case` 可以同时进行，则随机选择一个执行。
- `default` 分支在没有通道准备好时立即执行，不会阻塞。













# Go网盘

github项目地址 https://github.com/GetcharZp/cloud-disk

博客：https://blog.csdn.net/weixin_43734095/article/details/124927942



# miniDB





# Gin

# go-zero

goctl（gocontrol）是go-zero微服务框架下的代码生成工具。

https://go-zero.dev/cn/docs/goctl/goctl
