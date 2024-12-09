# 概览

### C++ 知识体系大纲

#### 1. **基础语法**

   - 基本数据类型与变量
   - 运算符与表达式
   - 控制结构（条件语句、循环语句）
   - 函数与递归
   - 输入输出（I/O）

#### 2. **数据结构**
   - 数组与字符串
   - 链表
   - 栈与队列
   - 树（包括二叉树、二叉搜索树）
   - 图（包括图的表示、遍历）
   - 哈希表（`unordered_map`, `unordered_set`）

#### 3. **标准模板库（STL）**
   - **容器（Containers）**
     - 顺序容器：`vector`, `deque`, `list`
     - 关联容器：`set`, `map`, `multiset`, `multimap`
     - 无序容器：`unordered_set`, `unordered_map`, `unordered_multiset`, `unordered_multimap`
     - 容器适配器：`stack`, `queue`, `priority_queue`
   - **迭代器（Iterators）**
     - 输入迭代器、输出迭代器
     - 前向迭代器、双向迭代器、随机访问迭代器
   - **算法（Algorithms）**
     - 排序与查找：`sort`, `binary_search`, `find`
     - 其他算法：`accumulate`, `copy`, `transform`
   - **函数对象与谓词（Function Objects and Predicates）**
     - 内建函数对象
     - 自定义函数对象
   - **适配器（Adapters）**
     - 迭代器适配器
     - 函数适配器

#### 4. **面向对象编程（OOP）**
   - 类与对象
   - 继承与多态
   - 封装与访问控制
   - 构造函数与析构函数
   - 运算符重载
   - 虚函数与抽象类

#### 5. **高级特性**
   - 模板编程
     - 函数模板与类模板
     - 模板特化与偏特化
   - 异常处理
     - 异常类
     - `try`, `catch`, `throw`
   - 多线程编程
     - 线程的创建与管理
     - 互斥锁与条件变量
     - 并发容器
   - 智能指针（`unique_ptr`, `shared_ptr`, `weak_ptr`）
   - 移动语义与右值引用

#### 6. **C++11 及以后标准**
   - 新特性
     - 右值引用与移动语义
     - Lambda 表达式
     - `auto` 类型推导
     - `decltype`
     - 强类型枚举（`enum class`）
     - 智能指针
   - 其他改进
     - 容器的新方法与改进
     - 多线程支持
     - 静态断言（`static_assert`）
     - 通用属性（Attributes）

#### 7. **设计模式**
   - 创建型模式：单例、工厂方法、抽象工厂、建造者、原型
   - 结构型模式：适配器、桥接、组合、装饰、外观、享元、代理
   - 行为型模式：责任链、命令、解释器、迭代器、中介者、备忘录、观察者、状态、策略、模板方法、访问者

#### 8. **工具与环境**
   - 编译器与构建工具（如 `g++`, `CMake`）
   - 调试工具（如 `gdb`）
   - 等等



```
C++ 标准库
 ├── 基础组件（C++98/03）
 │   ├── STL
 │   │   ├── 容器（Containers）
 │   │   ├── 迭代器（Iterators）
 │   │   ├── 算法（Algorithms）
 │   │   └── 函数对象（Function Objects）
 │   ├── 字符串库（String Library）
 │   ├── I/O 库（I/O Library）
 │   └── 数学库（Math Library）
 │
 └── 扩展组件（C++11 及以后）
     ├── 新容器（如 `array`, `forward_list`, 无序容器）
     ├── 智能指针（Smart Pointers）
     ├── 多线程支持（Concurrency Support）
     ├── 时间库（Chrono Library）
     ├── 随机数生成器（Random Library）
     ├── 正则表达式（Regex Library）
     ├── 文件系统（Filesystem Library, C++17）
     └── 其他（如 `tuple`, `optional`, `variant` 等）


```

















# string库

   - 数组与字符串
   - 链表
   - 栈与队列
   - 树（包括二叉树、二叉搜索树）
   - 图（包括图的表示、遍历）
   - 哈希表（`unordered_map`, `unordered_set`）



## String

**string和char *的相互转换**

字符数组可以直接赋给string

```cpp
char *p = "123";
string str = p;
```

str.data()是const char *型

```cpp
string str = "abc";
const char *p = str.data();
```



string之间的比较直接使用关系运算符（==、!=、<、<=、>、>=）即可

string之间可以直接:

+ 拼接+
+ 追加+=

也可以**append**追加字符串

```
str1.append(str2);
str1.append("C string");
```



**string.substr()** 

```cpp
string str("Hello,World!");
string subStr = str.substr(3,5);
```

当然可以下标访问



`std::string` 是 C++ 标准库的一部分，具体来说，它属于 C++ 标准库中的字符串库（String Library）。字符串库提供了处理字符串的类和函数。以下是关于 `std::string` 的详细说明以及它在 C++ 标准库中的位置。

### `std::string` 的位置和相关组件

#### 1. **C++ 标准库结构**

```
C++ 标准库
 ├── 基础组件（C++98/03）
 │   ├── STL
 │   │   ├── 容器（Containers）
 │   │   ├── 迭代器（Iterators）
 │   │   ├── 算法（Algorithms）
 │   │   └── 函数对象（Function Objects）
 │   ├── 字符串库（String Library）
 │   │   ├── std::string
 │   │   ├── std::wstring
 │   │   └── std::basic_string
 │   ├── I/O 库（I/O Library）
 │   ├── 数学库（Math Library）
 │   └── 其他实用工具（Utility）
 │
 └── 扩展组件（C++11 及以后）
     ├── 新容器（如 `array`, `forward_list`, 无序容器）
     ├── 智能指针（Smart Pointers）
     ├── 多线程支持（Concurrency Support）
     ├── 时间库（Chrono Library）
     ├── 随机数生成器（Random Library）
     ├── 正则表达式（Regex Library）
     ├── 文件系统（Filesystem Library, C++17）
     └── 其他（如 `tuple`, `optional`, `variant` 等）
```

### `std::string` 详解

`std::string` 是 C++ 标准库中的一个类，用于表示和操作可变长度的字符串。它是 `std::basic_string<char>` 的一个特化版本。以下是 `std::string` 的基本用法和主要成员函数。

#### 1. 引入头文件

```cpp
#include <string>
```

#### 2. 声明和初始化

```cpp
std::string str1;             // 默认构造，空字符串
std::string str2("Hello");    // 使用字符串字面值初始化
std::string str3(str2);       // 拷贝构造
std::string str4(10, 'a');    // 初始化为10个字符 'a'
```

#### 3. 基本操作

```cpp
// 连接
std::string str5 = str2 + " World";

// 访问字符
char c = str2[1];

// 修改字符
str2[1] = 'a';

// 获取长度
size_t len = str2.size();

// 子串
std::string substr = str2.substr(1, 3);
```

#### 4. 成员函数

- **大小相关**
  - `size()` 或 `length()`：返回字符串长度
  - `empty()`：检查字符串是否为空
  - `resize(size_t n)`：调整字符串大小
- **修改字符串**
  - `clear()`：清空字符串
  - `append()`：追加字符串
  - `insert(size_t pos, const std::string& str)`：插入字符串
  - `erase(size_t pos, size_t len)`：删除子串
  - `replace(size_t pos, size_t len, const std::string& str)`：替换子串
- **查找**
  - `find(const std::string& str)`：查找子串第一次出现的位置
  - `rfind(const std::string& str)`：查找子串最后一次出现的位置
  - `find_first_of(const std::string& str)`：查找任一字符第一次出现的位置
  - `find_last_of(const std::string& str)`：查找任一字符最后一次出现的位置
- **比较**
  - `compare(const std::string& str)`：比较两个字符串
- **转换**
  - `c_str()`：返回C风格字符串（const char*）

### 示例代码

```cpp
#include <iostream>
#include <string>

int main() {
    // 创建字符串
    std::string str1 = "Hello";
    std::string str2 = "World";

    // 连接字符串
    std::string str3 = str1 + " " + str2;
    std::cout << str3 << std::endl; // 输出：Hello World

    // 获取长度
    std::cout << "Length: " << str3.size() << std::endl; // 输出：Length: 11

    // 访问和修改字符
    char c = str3[1];
    std::cout << "Character at index 1: " << c << std::endl; // 输出：Character at index 1: e
    str3[1] = 'a';
    std::cout << "Modified string: " << str3 << std::endl; // 输出：Modified string: Hallo World

    // 子串
    std::string substr = str3.substr(0, 5);
    std::cout << "Substring: " << substr << std::endl; // 输出：Substring: Hallo

    // 查找
    size_t pos = str3.find("World");
    if (pos != std::string::npos) {
        std::cout << "\"World\" found at position: " << pos << std::endl; // 输出："World" found at position: 6
    }

    return 0;
}
```

### 总结

`std::string` 是 C++ 标准库字符串库的一部分，为处理字符串提供了丰富的功能和接口。它封装了C风格字符串，提供了更安全和方便的操作方式。理解 `std::string` 及其用法是掌握 C++ 标准库的重要一环。



# C++STL

| STL   的组成 | 含义                                                         |
| :----------: | ------------------------------------------------------------ |
|     容器     | 一些封装[数据结构](http://c.biancheng.net/data_structure/)的模板类，例如 vector 向量容器、list 列表容器等。 |
|     算法     | STL 提供了非常多（大约 100 个）的数据结构算法，它们都被设计成一个个的模板函数，这些算法在 std 命名空间中定义，其中大部分算法都包含在头文件 <algorithm> 中，少部分位于头文件 <numeric> 中。 |
|    迭代器    | 在 [C++](http://c.biancheng.net/cplus/) STL 中，对容器中数据的读和写，是通过迭代器完成的，扮演着容器和算法之间的胶合剂。 |
|   函数对象   | 如果一个类将 () 运算符重载为成员函数，这个类就称为函数对象类，这个类的对象就是函数对象（又称仿函数）。 |
|    适配器    | 可以使一个类的接口（模板的参数）适配成用户指定的形式，从而让原本不能在一起工作的两个类工作在一起。值得一提的是，容器、迭代器和函数都有适配器。 |
|  内存分配器  | 为容器类模板提供自定义的内存申请和释放功能，由于往往只有高级用户才有改变内存分配策略的需求，因此内存分配器对于一般用户来说，并不常用。 |

C++标准中共13个头文件

> 遵照 C++ 规范，所有标准头文件使用无扩展名的头文件。

| <iterator> | <functional> | <vector>  | <deque>  |
| ---------- | ------------ | --------- | -------- |
| <list>     | <queue>      | <stack>   | <set>    |
| <map>      | <algorithm>  | <numeric> | <memory> |
| <utility>  |              |           |          |



### 容器

 array、vector、deque、list 和 forward_list 

- 序列容器： vector 向量容器、list 列表容器以及 deque 双端队列容器
- 排序容器：set 集合容器、multiset多重集合容器、map映射容器以及 multimap 多重映射容器。
- 哈希容器：[C++](http://c.biancheng.net/cplus/) 11 新加入 4 种关联式容器，分别是 unordered_set 哈希集合、unordered_multiset 哈希多重集合、unordered_map 哈希映射以及 unordered_multimap 哈希多重映射。和排序容器不同，哈希容器中的元素是未排序的，元素的位置由哈希函数确定。

### 迭代器

1) 前向迭代器（forward iterator）
   假设 p 是一个前向迭代器，则 p 支持 ++p，p++，*p 操作，还可以被复制或赋值，可以用 == 和 != 运算符进行比较。此外，两个正向迭代器可以互相赋值。

2) 双向迭代器（bidirectional iterator）
   双向迭代器具有正向迭代器的全部功能，除此之外还可以进行 --p 或者 p-- 操作（即一次向后移动一个位置）。

3) 随机访问迭代器（random access iterator）//其实是任意访问迭代器
   随机访问迭代器具有双向迭代器的全部功能。除此之外，假设 p 是一个随机访问迭代器，i 是一个整型变量或常量，则 p 还支持以下操作：

- p+=i：使得 p 往后移动 i 个元素。
- p-=i：使得 p 往前移动 i 个元素。
- p+i：返回 p 后面第 i 个元素的迭代器。
- p-i：返回 p 前面第 i 个元素的迭代器。
- p[i]：返回 p 后面第 i 个元素的引用。

自然而然地，不同的容器有固定对应的迭代器类型。

### 迭代器的定义方式

| 迭代器定义方式 | 具体格式                                   |
| -------------- | ------------------------------------------ |
| 正向迭代器     | 容器类名::iterator 迭代器名;               |
| 常量正向迭代器 | 容器类名::const_iterator 迭代器名;         |
| 反向迭代器     | 容器类名::reverse_iterator 迭代器名;       |
| 常量反向迭代器 | 容器类名::const_reverse_iterator 迭代器名; |



## queue，stack，deque

queue 的基本操作有：

入队，如例：q.push(x); 将x 接到队列的末端。

出队，如例：q.pop(); 弹出队列的第一个元素，注意，并不会返回被弹出元素的值。

访问队首元素，如例：q.front()，即最早被压入队列的元素。

访问队尾元素，如例：q.back()，即最后被压入队列的元素。

判断队列空，如例：q.empty()，当队列空时，返回true。

访问队列中的元素个数，如例：q.size()



堆栈操作:
和其他序列容器相比，stack 是一类存储机制简单、所提供操作较少的容器。下面是 stack 容器可以提供的一套完整操作：

top()：返回一个栈顶元素的引用，类型为 T&。如果栈为空，返回值未定义。
push(const T& obj)：可以将对象副本压入栈顶。这是通过调用底层容器的 push_back() 函数完成的。
push(T&& obj)：以移动对象的方式将对象压入栈顶。这是通过调用底层容器的有右值引用参数的 push_back() 函数完成的。
pop()：弹出栈顶元素。
size()：返回栈中元素的个数。
empty()：在栈中没有元素的情况下返回 true。
swap(stack & other_stack)：将当前栈中的元素和参数中的元素交换。参数所包含元素的类型必须和当前栈的相同。对于 stack 对象有一个特例化的全局函数 swap() 可以使用。



## vector

[VectorCSDN](https://blog.csdn.net/zou_albert/article/details/107280534)

vector是一段连续的，动态分配的内存（动态数组）

- 表示的向量长度较长（需要为向量内部保存很多数），容易导致内存泄漏，而且效率会很低。
- vector作为函数的参数或者返回值时，需要注意它的写法：
  double Distance(vector&a, vector&b) 其中的**“&”**绝对不能少！！！

```cpp
include<vector>

vector<vector<Point2f> > points; //定义一个二维数组
points.size();      //求行数
points[0].size();  //求列数

//使用下标访问元素
	vec[0]
    
//尾部插入数字
	vec.push_back(a);

//插入元素
	vec.insert(vec.begin()+i,a);在第i+1个元素前面插入a;

//删除元素
	vec.erase(vec.begin()+2);删除第3个元素

//清空
	vec.clear();

```

#### begin()

```
函数原型:
iterator begin();
const_iterator begin();
功能：返回一个当前vector容器中起始元素的迭代器。
```

#### end()

```
函数原型：
iterator end();
const_iterator end();
功能：返回一个当前vector容器中末尾元素的迭代器。
注意v1.end()指向的是最后一个元素的下一个位置，所以访问最后一个元素
```

#### front()

```
函数原型：
reference front();
const_reference front();
功能：返回当前vector容器中起始元素的引用。
```

#### back()

```
函数原型：
reference back();
const_reference back();
功能：返回当前vector容器中末尾元素的引用。
```

#### insert

```
c.insert(pos,elem) // 在pos位置插入一个elem拷贝，传回新数据位置。
c.insert(pos,n,elem) // 在pos位置插入n个elem数据。无返回值。
c.insert(pos,beg,end) // 在pos位置插入在[beg,end)区间的数据。无返回值。
```

#### sort

bool Comp(const int &a,const int &b)
{
    return a>b;
}
调用时:sort(vec.begin(),vec.end(),Comp)，这样就降序排序。 



在类中定义时会出现问题：

> error: reference to non-static member function must be called

为什么cmp函数在作为类成员函数的时候一定需要static修饰呢？这是因为所有我们在类内定义的非static成员函数在经过编译后隐式的为他们添加了一个this指针参数！变为了：

```
bool cmp(Solution *this, int a, int b)
```


而标准库的sort()函数的第三个cmp函数指针参数中并没有这样this指针参数，因此会出现输入的cmp参数和sort()要求的参数不匹配，从而导致了：
error: reference to non-static member function must be called
而我们知道static静态类成员函数是不需要this指针的，因此改为静态成员函数即可通过！
原文链接：https://blog.csdn.net/weixin_40710708/article/details/111269356

# 哈希表

哈希表（Hash Table）是一种数据结构，它通过使用哈希函数将键（Key）映射到值（Value），从而实现快速的插入、删除和查找操作。在 C++ 中，标准模板库（STL）提供了 `unordered_map` 类来实现哈希表。以下是关于 C++ 中哈希表的基础知识和相关用法的总结：

### 基础知识

1. **哈希函数**：
    - 哈希函数将键映射到一个哈希值（通常是一个整数），这个哈希值用来确定值在哈希表中的位置。
    - 好的哈希函数应尽量避免冲突（不同的键映射到相同的哈希值）。

2. **冲突处理**：
    - 当两个不同的键通过哈希函数映射到相同的位置时，就会发生冲突。
    - 常见的冲突处理方法有链地址法（Separate Chaining）和开放地址法（Open Addressing）。

3. **负载因子**：
    - 负载因子是哈希表中元素数量与桶（bucket）数量的比值。
    - 较高的负载因子会增加冲突的概率，影响性能。哈希表会在必要时自动扩展以保持合理的负载因子。

### `unordered_map` 使用方法

`unordered_map` 是 C++ 标准模板库中提供的哈希表实现。以下是 `unordered_map` 的基本用法：

#### 1. 头文件
要使用 `unordered_map`，需要包含头文件：
```cpp
#include <unordered_map>
```

#### 2. 声明和初始化
```cpp
unordered_map<KeyType, ValueType> map;
```
例如：
```cpp
unordered_map<string, int> ageMap;
```

#### 3. 插入元素
```cpp
map[key] = value;
map.insert({key, value});
```
例如：
```cpp
ageMap["Alice"] = 30;
ageMap.insert({"Bob", 25});
```

#### 4. 访问元素
```cpp
ValueType value = map[key];
```
例如：
```cpp
int age = ageMap["Alice"];
```

#### 5. 查找元素
```cpp
auto it = map.find(key);
if (it != map.end()) {
    // Element found, use it->second for value
}
```
例如：
```cpp
auto it = ageMap.find("Alice");
if (it != ageMap.end()) {
    int age = it->second;
}
```

#### 6. 删除元素
```cpp
map.erase(key);
```
例如：
```cpp
ageMap.erase("Alice");
```

#### 7. 遍历元素
```cpp
for (const auto &pair : map) {
    KeyType key = pair.first;
    ValueType value = pair.second;
}
```
例如：
```cpp
for (const auto &pair : ageMap) {
    string name = pair.first;
    int age = pair.second;
}
```

#### 8. 常用成员函数
- `size()`：返回哈希表中元素的数量。
- `empty()`：检查哈希表是否为空。
- `clear()`：清空哈希表。

### 示例代码

以下是一个完整的示例，展示了 `unordered_map` 的常用操作：

```cpp
#include <iostream>
#include <unordered_map>

using namespace std;

int main() {
    // 创建一个unordered_map
    unordered_map<string, int> ageMap;

    // 插入元素
    ageMap["Alice"] = 30;
    ageMap["Bob"] = 25;
    ageMap.insert({"Charlie", 35});

    // 访问元素
    cout << "Alice's age: " << ageMap["Alice"] << endl;

    // 查找元素
    auto it = ageMap.find("Bob");
    if (it != ageMap.end()) {
        cout << "Bob's age: " << it->second << endl;
    } else {
        cout << "Bob not found" << endl;
    }

    // 删除元素
    ageMap.erase("Alice");

    // 遍历元素
    for (const auto &pair : ageMap) {
        cout << pair.first << "'s age: " << pair.second << endl;
    }

    return 0;
}
```

### 性能特点

- **时间复杂度**：
    - 插入、删除、查找的平均时间复杂度为 \(O(1)\)。
    - 在最坏情况下（所有键都冲突），时间复杂度会退化为 \(O(n)\)，但这种情况极少发生。
- **空间复杂度**：
    - 哈希表需要额外的空间来存储哈希值和指针，空间复杂度为 \(O(n)\)。

`unordered_map` 是处理需要快速插入、删除和查找操作的键值对数据的理想选择。在使用时，需要注意选择合适的哈希函数和负载因子，以确保哈希表的高效运行。













## pair(键值对)

**pair是一个结构体**，主要的两个成员是`first` ，`second`

**make_pair()**

```cpp
 pair <string,double> product1 ("tomatoes",3.25);
 pair <string,double> product2; 
 pair <string,double> product3;
 
 product2.first = "lightbulbs";     // type of first is string
 product2.second = 0.99;            // type of second is double
 
 product3 = make_pair ("shoes",20.0);
```



## map

map中默认按照key的升序排列

pair的集合







## memset()

<cstring >

memset(指针, 初始值, 长度);

eg:memset(f, 0, sizeof(f))

extern void *memset(void *buffer, int c, int count)     	*//buffer：为指针或是数组,*    	*//c：是赋给buffer的值,*    	*//count：是buffer的长度.*

## sort( )

<algorithm>

sort(起始地址, 结束地址, 规则);(默认从小到大排序)

`sort(a+1,a+n+1,comp)`

（1）第一个参数first：是要排序的数组的起始地址。

（2）第二个参数last：是结束的地址（最后一个数据的后一个数据的地址）

（3）第三个参数comp是排序的方法：可以是从升序也可是降序。如果第三个参数不写，则默认的排序方法是从小到大排序。











# **---高级特性---**



# **面向对象编程（OOP）**



### 类与对象

[^菜鸟教程_C++面向对象]: https://www.runoob.com/cplusplus/cpp-classes-objects.html

- **对象 -** 对象具有状态和行为。例如：一只狗的状态 - 颜色、名称、品种，行为 - 摇动、叫唤、吃。对象是类的实例。

- **类 -** 类可以定义为描述对象行为/状态的模板/蓝图。
- **方法 -** 行为,函数
- **即时变量 -** 每个对象都有其独特的即时变量。对象的状态是由这些即时变量的值创建的。

```c++
//类包含属性和行为。
class 类名{ 访问权限：属性/行为; }
//属性就是定义数值、行为就是函数。
```



![img](C&Cpp.assets/cpp-classes-objects-2020-12-10-11.png)



```c++
#include <iostream>
 
using namespace std;
 
class Box
{
   public:
      double length;   // 长度
      double breadth;  // 宽度
      double height;   // 高度
      // 成员函数声明
      double get(void);
      void set( double len, double bre, double hei );
};
// 成员函数定义
double Box::get(void)
{
    return length * breadth * height;
}
 
void Box::set( double len, double bre, double hei)
{
    length = len;
    breadth = bre;
    height = hei;
}
int main( )
{
   Box Box1;        // 声明 Box1，类型为 Box
   Box Box2;        // 声明 Box2，类型为 Box
   Box Box3;        // 声明 Box3，类型为 Box
   double volume = 0.0;     // 用于存储体积
 
   // box 1 详述
   Box1.height = 5.0; 
   Box1.length = 6.0; 
   Box1.breadth = 7.0;
 
   // box 2 详述
   Box2.height = 10.0;
   Box2.length = 12.0;
   Box2.breadth = 13.0;
 
   // box 1 的体积
   volume = Box1.height * Box1.length * Box1.breadth;
   cout << "Box1 的体积：" << volume <<endl;
 
   // box 2 的体积
   volume = Box2.height * Box2.length * Box2.breadth;
   cout << "Box2 的体积：" << volume <<endl;
 
 
   // box 3 详述
   Box3.set(16.0, 8.0, 12.0); 
   volume = Box3.get(); 
   cout << "Box3 的体积：" << volume <<endl;
   return 0;
}
```





### 定义成员函数

成员函数可以定义在类定义内部，或者单独使用**范围解析运算符 ::** ;

在类定义中定义的成员函数声明默认为**内联**的，即便没有使用 inline 标识符。



```c++
class Box
{
   public:
      double length;      // 长度
      double breadth;     // 宽度
      double height;      // 高度
   
      double getVolume(void)
      {
         return length * breadth * height;
      }
};
```

也可以在类的外部使用**范围解析运算符 ::** 定义该函数：

```c++
double Box::getVolume(void) {    
    return length * breadth * height;
}
```



### 访问修饰符

默认访问修饰符是 private。

每个标记区域在下一个标记区域开始之前或者在遇到类主体结束右括号之前都是有效的。

```c++
class Base {
 
   public:
 
  // 公有成员
 
   protected:
 
  // 受保护成员
 
   private:
 
  // 私有成员
 
};
```



没有返回参数，因此不能重载；

```c++
class Person{
public:
  Person(){
cout<<"11"<<endl;
} 
  ~Person(){
cout<<"22";
}

}
```

### 构造函数

类的**构造函数**是类的一种特殊的成员函数，它会在每次创建类的新对象时执行。

1.构造函数，没有返回值也不用写void;
2.构造函数与类名相同；
3.构造函数可以有参数，因此可以重载；
4.对象使用时会自动给调用构造函数，且只会调用一次。



分成两类：有参构造和无参构造；普通构造和拷贝构造；
调试方法：括号法、显示法、隐式转换法。

```c++
//无参（默认）函数
class Person{
      pbulic:
      person(){

      }
      //有参构造
      person(int a){}
      //拷贝构造
      person(const person&p){}
}; 
```

C++中拷贝构造函数调用时机
1、使用一个已经创建完毕的对象初始化一个新对象；
2、值传递的方式给函数参数传值
**深拷贝与浅拷贝**
深拷贝：在堆区重新申请空间，进行拷贝操作；
浅拷贝：简单的赋值拷贝操作。









## 继承：基类，派生类

```cpp
// 派生类
class Rectangle: public Shape
    
class Rectangle: public Shape, public PaintCost
{
   public:
      int getArea()
      { 
         return (width * height); 
      }
};
```

访问权限：

| 访问     | public | protected | private |
| :------- | :----- | :-------- | :------ |
| 同一个类 | yes    | yes       | yes     |
| 派生类   | yes    | yes       | no      |
| 外部的类 | yes    | no        | no      |

继承类型

一般都用 ：public

- **公有继承（public）：**当一个类派生自**公有**基类时，基类的**公有**成员也是派生类的**公有**成员，基类的**保护**成员也是派生类的**保护**成员，基类的**私有**成员不能直接被派生类访问，但是可以通过调用基类的**公有**和**保护**成员来访问。
- **保护继承（protected）：** 当一个类派生自**保护**基类时，基类的**公有**和**保护**成员将成为派生类的**保护**成员。
- **私有继承（private）：**当一个类派生自**私有**基类时，基类的**公有**和**保护**成员将成为派生类的**私有**成员。



一个派生类继承了所有的基类方法，但下列情况除外：

- 基类的构造函数、析构函数和拷贝构造函数。
- 基类的重载运算符。
- 基类的友元函数。



## 多态































# 文件处理



## ifstream类

这是一个输入文件流类，用于从文件中读取数据。`ifstream` 是 "input file stream" 的缩写，允许程序读取文件内容。



1. **std::ifstream用法**

- **创建对象**：`std::ifstream infile(input_csv);`
  - `std::ifstream` 是用于从文件中读取数据的输入文件流类。
  - `infile` 是输入流对象，通过它可以读取 `input_csv` 指定的文件内容。
- **功能**：
  - 打开指定路径的文件，准备读取。
  - 可通过 `infile.is_open()` 检查文件是否成功打开。
  - 

# 多线程thread库

### 常用函数汇总

线程:

- **`std::thread`**: 创建新线程并运行指定函数。
- **`join()`**: 阻塞当前线程，直到被调用的线程完成。
- **`detach()`**: 将线程分离，使其在后台运行。
- **`emplace_back()`**: 向容器添加元素，直接在容器内构造对象。

锁:

- **`std::mutex`**: 用于实现互斥锁。

- **`std::lock_guard`**: 自动管理互斥量的加锁和解锁。

  

```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

// 互斥量
std::mutex mtx;

// 线程函数
void threadFunction(int id) {
    std::lock_guard<std::mutex> lock(mtx); // 自动加锁
    std::cout << "Thread ID: " << id << " is running." << std::endl;
}

int main() {
    std::vector<std::thread> threads;

    // 创建多个线程
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(threadFunction, i); // 使用 emplace_back 添加线程
    }

    // 等待所有线程完成
    for (auto& t : threads) {
        t.join(); // join 函数：等待线程结束
    }

    return 0;
}

```







# C to C++(差异，易忘记， )

不知道怎么分类的

## namespace





## auto



for(auto iter:vec)不改变迭代对象的值，

for(auto &iter:vec)可以改变迭代对象的值。
两者都可以获取到迭代容器中的值，但是使用auto iter时不会对容器对象造成改变，



## 文件I/O



```cpp
void readfile(char * content){//打开File并将其中内容存入content
	fstream fs;
	string filepath="D:/MyFile/code/vs/repos/MyServer/index.html";
	fs.open(filepath);
	if(!fs.is_open()) printf("\nopen failed!\n");
	char buf[105];
	while(fs.getline(buf,100)){
		strcat(content,buf);
	}
	fs.close();
}
```

```
ifstream f;
filebuf* tmp = f.rdbuf();
```

## 引用&

[引用](https://www.cnblogs.com/cthon/p/9169020.html)

引用相当于给变量改一个别名

原则上说引用不占用空间，但实际上编译器一般实现为const 指针

```cpp
1.【值传递】如果形参为非引用的传值方式，则生成局部临时变量接收实参的值
void Swap (int left, int right){   
    //值传递的方式无法实现交换，因为传参时对于参数left和right拷贝一临时副本，交换的是副本值，因为其是临时变量函数退出，变量销毁，并不会影响外部left和right的值。
     int temp = left;
     left = right ;
     right = temp ;
}
 
2.【引用传递】如果形参为引用类型，则形参是实参的别名。
void Swap (int& left, int& right){
    //使用引用的话，不做临时拷贝，&的使用说明此处只是原参数的另一个名字而已，所以修改时直接在原参数的基础上修改变量值，减少了复制的开销，加快程序执行效率。
     int temp = left;
     right = left ;
     left = temp ;
}
 
3.【指针传递】
void Swap (int* pLeft, int* pRight){
    //传入的是地址，因为地址是唯一的，所以指针通过地址的访问进而可修改其内容。但是压入函数参数栈的也是指针变量的副本
     int temp = *pLeft;
     *pLeft = *pRight;
     *pRight = temp;
}
```





## 正则表达式



 `\\` (转义) \ 表示必须有

`[a-z]+ `	匹配 a、aaa、abcd、softwaretestinghelp 等字符串。请注意，它永远不会匹配空白字符串。

`[a-z]*`	将匹配一个空白字符串或任何上面的字符串。



一个文件名匹配的正则表达式

```cpp
char regex_filename[] = “[a-zA-Z_] [a-zA-Z_0-9]*\\.[a-zA-Z0-9]+”;
```

匹配的是：字母+数字或字母+点+数字或字母(非空)



**regex_match()**

**regex_search()**

**regex_replace()**









# 一些idea闲言碎语

void *类型可以接受任意类型指针。

foo/bar是自二战时的俚语FUBAR(Fucked Up Beyond All Repair)，就是坏到无法修缮的意思。

就是无意义的占位符，相当于张三李四。



## **位运算**

|  &   | 与         | 两个位都为1时，结果才为1                                     |
| :--: | ---------- | ------------------------------------------------------------ |
|  \|  | 或         | 两个位都为0时，结果才为0                                     |
|  ^   | 异或(相异) | 两个位相同为0，相异为1                                       |
|  ~   | 取反       | 0变1，1变0                                                   |
|  <<  | 左移       | 各二进位全部左移若干位，高位丢弃，低位补0                    |
|  >>  | 右移       | 各二进位全部右移若干位，对无符号数，高位补0，有符号数，各编译器处理方法不一样，有的补符号位（算术右移），有的补0（逻辑右移） |



对于一个数的负数就等于对这个数取反+1



unsigned型能防止右移补1的情况

多利用mask控制 要取得位

用 ~0制造任意mask

## lowbit(x)

lowbit(x) = x & (-x)

对于一个数的负数就等于对这个数取反+1

以二进制数11010为例:11010的补码为00101,加1后为00110,两者相与便是最低位的1

其实很好理解,补码和原码必然相反,所以原码有0的部位补码全是1,补码再+1之后由于进位那么最末尾的1和原码

最右边的1一定是同一个位置(当遇到第一个1的时候补码此位为0,由于前面会进一位,所以此位会变为1)
所以我们只需要进行a&(-a)就可以取出最低位的1了



## 判断一个数是否为2的

### **2的倍数**

判断一个数是否是2的倍数正常我们会使用n % 2 == 0，但其实编译器会优化成位运算(因为计算机只认识0和1)。

用就可以思考成判断一个二进制数是否是2的倍数就看最后一位，如果是1就不是2的倍数，等于0就是2的倍数。那我们的问题就转成了判断一个数的二进制最后一位是否是1了。

仔细思考之后发现1这个数除了最后一位是1，其他全为0，再用上与(&)符号,
如果结果为1不是2的倍数，为0是的2的倍数。

```c
 n > 0 && (n & 1) == 0;
```

### **2的次幂**

判断一个数是否是2的次幂（2，4，8，16.。。。。），发现这些数二进制都有一个规律，就是最高都为1，其他全为0，那么将这些都减1的话，所有位数刚好反过来，最高为0，其余全为1，那我们就可以使用这个公式：(n & (n-1)) == 0,如果结果是0就是2的次幂。

```c
n > 0 && (n & (n-1)) == 0;
```

## 结构体的存储

不是挨着存的?

 在C语言中，在默认情况下，[编译器](https://so.csdn.net/so/search?q=编译器&spm=1001.2101.3001.7020)规定各成员变量存放的起始地址相对于结构的起始地址的偏移量必须为该变量的类型所占用的字节的倍数。

```c
struct MyStruct {

double ddal;

char dda;

int type;

};
```

大小为 16 !



 所以，在计算结构体变量的大小时：

 ①上面的所有字节数的总和，必须是下一个类型的整数倍数。

 ②总字节数一定是最大类型的整数倍。



## **数据范围**

int最大值2147483647



### 用sizeof()获取数组中元素的个数

```c
for(i = 0;i <  sizeof(arr) / sizeof(arr[0]);   i++)

      {

         printf("arr[%d]=%d\n",i,arr[i]);

      }
```







## 存储类型

1.自动变量（auto）

2.静态变量（static）

3.外部变量（extern）

4.寄存器类型（register）计算速度快，不储存，也没地址

！变量的作用域不同，本质上是由于变量的存储类型不同。

动态存储方式：auto,register

静态存储方式:   static，extern

！生存时间：

自动变量：随着函数的进栈和出栈而创建和销毁

静态变量，外部变量：长期存在静态存储区，直到程序结束

寄存器变量：离开函数值就会消失

全局变量：直接写在main函数外面（甚至是同一程序的其他文件中），就是全局变量了，全局变量用之前要声明写extern

static有两种：	

在外部，叫静态全局变量，其作用域为当前文件

在内部，叫静态局部变量，其作用域为一对{ }内

另外，static只能被初始化赋值一次（在循环里，之后就不再走初始化的那一行了）

## 输入输出

1.printf和scanf    

\>>scanf加取地址符！！！<<

2.putchar和getchar

当您输入一个文本，按下回车键，程序会继续并只会读取一个单一的字符。

3.gets()和puts() 

它会等待您输入一些文本，当您输入一个文本并按下回车键时，程序会继续并读取一整行直到该行结束。（好像包括空格？！？！）

()里面加数组名

如果gets不等你输入就跳：

加一行`fflush(stdin)；`



## 文件的输入与输出

常用文件打开方式：

if((fp=fopen("file1","r"))==NULL)

{ printf("cannot open this file\n");

exit(0);		//退出程序

}

fclose（fp）：要记得关闭文件！！！

在访问磁盘文件时，是逐个字符（字节）进行的，每访问完一个字节后，当前读写位置自动后移。

feof函数

​	可检测文件尾标志是否被读取过，若已读过，返回值为1，否则为0。

​	if(feof(fp))

​                break;	

​       为了知道对文件读写是否完成，即检测文件尾标志是否已被读取过（文件的所有有效字符后有一个文件尾标志，用标识符EOF表示）。

->二进制的输入输出

size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)

参数：

ptr -- 这是指向要被写入的元素数组的指针。

size -- 这是要被写入的每个元素的大小，以字节为单位。

nmemb -- 这是元素的个数，每个元素的大小为 size 字节。

stream -- 这是指向 FILE 对象的指针，该 FILE 对象指定了一个输出流。

size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)

参数：

ptr -- 这是指向带有最小尺寸 size*nmemb 字节的内存块的指针。

size -- 这是要读取的每个元素的大小，以字节为单位。

nmemb -- 这是元素的个数，每个元素的大小为 size 字节。

stream -- 这是指向 FILE 对象的指针，该 FILE 对象指定了一个输入流。



## 指针

**二级指针与二维数组**

`int ** mat`

二级指针是指针的指针。

`int mat\[C][C]`

二维数组名是一级指针。 (这个指针指向了宽度为[C]的数组)

```c
//init mat
    int ** a_mat;
    int ** b_mat;
    a_mat = (int **)malloc(sizeof(int));
    b_mat = (int **)malloc(sizeof(int));
//两个矩阵的二级指针初始化。 再对他们指向的指针初始化
    for(int i=0; i<=MAX; i++)
    {
        *a_mat = (int*)malloc(sizeof(int));
        *b_mat = (int*)malloc(sizeof(int));
    }
```

可以用二维数组(a_mat \[1][1]的形式)  操作这个二级指针	(理解一下:	第一个[]到达一级指针,再[]到达数值)

```c
	(*(a_mat+1))[1] = 6;
    a_mat[1][1] = 2;
    printf("%d ",a_mat[1][1]);
    printf("%d \n",(*(a_mat+1))[1]);
```

但是不可以把一个二维数组名`a_mat`传给`int ** mat`

```c
strassen.c:6:23: note: expected 'int **' but argument is of type 'int (*)[128]'
 void getmatrix(int ** mat, int m, int n)
```

**"一维数组与指针"：**

数组名 就是 数组中第一个元素的地址常量。

"我想把指针当成数组用"——动态内存分配!!!!!

​	memory（内存）allocate（分配）（malloc属于stdlib.h）

​	malloc的返回值是分配字节的首地址。

```c
	char * s1, *s2, *s3;

	s1 = (char *) malloc(100);   //分配了100字节。
```

​		

**"指针运算，移动"**：

​	同一个数组里，指针可以相加减（移动）

​	具体移动几个字节，取决于所指向元素的类型，总之，+1表示移动一个元素，

​	指向int则跳4字节

​	指向char则跳1字节

**"指针占据几个字节"**

​	在硬件中，一个字节就是一个单元，每个单元有一个编号。

​	指针变量占用的内存空间取决于操作系统：32位操作系统中指针变量占用4个字节;64位操作系统中则为8个字节。

​	CPU控制内存的单元，例如，32线程控制一个4G内存条：有2^32种状态，就是4个字节，所以这时，地址就是4个字节。

​	无论所指变量的类型如何，指针只指向第一个字节， 通过变量类型来具体控制 *p的结果。

**"函数指针"**

​	char* (*p)(char * ,const char * );   p = 函数名

​	注意形参严格对应

​	如何赋值：

​	直接p=strcpy;就可以了。

 

​     

## 函数指针数组		

p[1] = 函数名

char* (*p[4])(char * ,const char * );

​        p[1]=strcpy;

​        p[2]=strcat;

​        p[3]=strtok;

建立了数字1-3 与 函数名之间的联系

问：如何用指针一个字节一个字节地读取变量

<命令行>

int main( int argc, char *argv[] ) 

argc     是你键入的参数个数 +1（它的值可以理解为自动计算出来的），  也就是argv里面存的指针的个数

argv[]   这个"指针数组" 中是存放的是你输入的参数的地址

其中，argv[0]是程序名字，你键入的参数是从[1]起的。

"问题来了"

​       现在所有的参数都是char型，键入的数	字也是以char型读的，数字变成了字符串！

可是我想要的是int型，我想要数值！

​	标准库函数（<stdlib.h>）：

​	int atoi(const char *str)把参数 str 所指向的字符串转换为一个整数

\--------------------------------------------------------------------------------------------------

## 链表

链表排序——选择法

交换任意两个指针域：

需要四个工具指针。

声明一个临时的头指针，处理第一个节点需要交换的情况。

交换四步：

 {

​         	temp = p2->next;        //把p2所指节点的下一个节点 先存起来

​                

​                prior1->next = p2;     

​                prior2->next = p1;          // p2->next = p1->next;

​                p2->next = p1->next;    // prior2->next =  p1; 调换这两行，在p1 = prior2时出错了

​                p1->next = temp;        

​                

​                temp = p1;                       //注意：虽然p1,p2所指节点互换了，也连好了

​                p1 = p2;                           //但是p1,p2还指向换完之后的节点

​                p2 = temp;

 }

思考：当p1,p2间只有一个间隔时....到底发生甚么事了

\-----------------------------------------------------------------------------------------------------------



## 提醒：

本地有输出，测试平台没输出：	

可能因为有的变量没初始化！

`runtime error`:多种可能,(不是超时),可能是空间溢出

`presnet error`:答案对了,格式不对

