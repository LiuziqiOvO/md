参考：https://www.yuque.com/aceld/mo95lb/kk9cvo

## 背景

使用Go：Docker，Go1.5以上也使用Go，Kubernetes（构建在Docker之上的容器调度），codis（redis），etcd

以太坊

并发模型——协程Goroutine

内存分配

垃圾回收

静态链接

标准库

工具链





## 环境配置和一些问题

Go有两个环境变量，一个是编译器本身，另一个用来存包和项目啥的。



### go-zero

goctl（gocontrol）是go-zero微服务框架下的代码生成工具。

https://go-zero.dev/cn/docs/goctl/goctl



### Go.mod

Go1.11新引入的包管理方式

报错：

```
$ go get -u github.com/igneous-systems/s3bench 
go: go.mod file not found in current directory or any parent directory.
	'go get' is no longer supported outside a module.
	To build and install a command, use 'go install' with a version,
	like 'go install example.com/cmd@latest'
	For more information, see https://golang.org/doc/go-get-install-deprecation
	or run 'go help get' or 'go help install'.
```

GO111MODULE是G01.11引入的新版模块管理方式。
GO111MODULE环境变量用于开启或关闭Go语言中的模块支特，它有off、on、auto三个可选值，
默认为auto.
1.GO111MODULE=off
无模块支持，go会从$GOPATH文件夹和vendor目录中寻找依赖项。
2.GO111MODULE=on
模块支持，go忽略$GOPATH文件夹，只根据go.mod下载依赖。
3.GO111MODULE=auto
在$GOPATH/src外层且根目录有go.mod文件时，开启模块支持；否者无模块支持。

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



#### 声明新的自定义类型：

```GO
type bucket [bucketSize]fingerprint
```

在Go语言中，方括号（`[]`）用于表示数组和切片。声明新的自定义类型的语法是 `type <名称> <底层类型>`，其中 `<名称>` 是新类型的名称，`<底层类型>` 是它基于的类型。

[bucketSize]` 表示这个数组的长度是 `bucketSize`，而 `fingerprint` 表示数组中每个元素的类型是 `fingerprint



#### errors.New()

```Go
return nil, errors.New("m needs 2^n")
```

在Go语言中，`nil`是一个常量，表示空指针或空值。它可以用于任何类型的变量或表达式，并且通常用于表示某个值不存在或未初始化。



其中`errors.New()`是一个Go标准库中的函数，它会创建一个包含指定错误信息的新error对象。

具体地说，`errors.New("m needs 2^n")`会创建一个新的error对象，并将错误信息设置为"m needs 2^n"。然后，该error对象会作为第二个返回值被传递给构造函数的调用方。

在Go语言中，函数可以返回多个值。如果某个函数需要返回错误信息，通常会将其作为最后一个返回值。调用方可以通过检查返回值中的错误对象来确定函数是否执行成功。如果没有发生错误，则错误对象为nil；否则，错误对象将包含相关的错误信息。



## func

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

# 网盘

github项目地址https://github.com/GetcharZp/cloud-disk

博客：https://blog.csdn.net/weixin_43734095/article/details/124927942

# miniDB

调用libzbd.a

```go
import "C"
```

