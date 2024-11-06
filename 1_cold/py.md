## 正则表达式



```python
import re

text = "The temperature is 25.3°C, the distance is 10.5 km, and the weight is 2.3 kg."

matches = re.findall(r'\d+\.\d+ [a-zA-Z]+', text)

print(matches)
```

严格注意缩进，对大小写敏感

# 字符串

len（）					获取长度
	要储存到的变量名 = len(字符串变量名)		
upper（ ）				所有全大写
	eg:x = x.upper()			
lower（ ）				全小写 
title（ ）					每个单词的首字母大写

strip（ )去掉首尾指定字符，不填去空格。


find（' '）				查找位置

replace（'old'，'new'）

split('分割符')			分割

------------------------------------------------------------------------------------------
# 列表

list = [ ]

list是可变的有序表
“索引” 	就是数组下标	
append() 						尾部追加

insert（位置索引，'元素'）		插入

del 列表名[位置索引] 			定点删除

列表名.pop[位置索引] 			顶点删除，默认末尾

变量名 = pop列表名[位置索引] 	移走删除

remove						指定元素删除

list里面的元素的数据类型也可以不同。
list元素也可以是另一个list。

sort（reverse=Ture） Ture是从大到小排，False或不填是从小到大排

对数字列表的运算
min（）
max（）
sum（）

对一个列表取其部分元素获得一个子序列
list_slice = source_list [start: end : step]
子序列名 = 被切片的名[  ：   ：  ]

source_list：被切片的源列表

list_slice：切片后生成的子序列列表

start：切片起始索引位置，省略则从头开始

end：切片结束索引位置，省略则切至列表末尾

注：切片和range()函数一样，Python会自动到达所指定切片结束索引位置的前面一个元素停止。
即: 左闭右开区间！！！
注：负数索引返回离列表末尾相应间隔的元素。列表末尾元素的索引是从-1开始的。

----------------------------------------------------------------------------------------
# 元组

tuple = （ ）
tuple和list非常类似，但是tuple一旦初始化就不能修改

menu1 = ('meat','fish','chicken')

元组和列表一样，可以使用下标索引来访问元组中的值
元组中的元素值是不可以修改的，如果强行修改会报错

len(tuple)：计算元组中元素个数。

max(tuple)：返回元组中元素的最大值。

min(tuple)：返回元组中元素的最小值。

tuple(seq)：将列表转换为元组。

来看一个“可变的”tuple：
>>>t = ('a', 'b', ['A', 'B'])
>>>t[2][0] = 'X'
>>>t[2][1] = 'Y'
>>>t
>>>('a', 'b', ['X', 'Y'])

---------------------------------------------------------------------------------------
循环
range(下限，上线，step)  		下限默认0，上限必填
	
	list（range（5））		#用range创建列表：从0到5
	for i in range（）		#用range进行for循环

break
continue

---------------------------------------------------------------------------------------
<字典>
dict = {'fish':40, 'pork':30}
使用键-值（key-value）存储，具有极快的查找速度，在其他语言中也称为map
>为什么键值对查找快？
>像查字典一样，在字典的索引表里（比如部首表）查这个字对应的页码，然后直接翻到该页，找到这个字。无论找哪个字，这种查找速度都非常快，不会随着字典大小的增加而变慢。
>所以在放进去的时候，必须能根据key算出value的存放位置，这样，取的时候才能根据key直接拿到value。（这个通过key计算位置的算法称为哈希算法（Hash）。）
>缺点：
>需要占用大量的内存，内存浪费多。
# 字典

创建并初始化menu

menu = {'fish':40, 'pork':30, 'potato':15, 'noodles':10}

### 向menu字典中添加菜名和价格

menu['juice'] = 12
menu['egg'] = 5

### 删除noodles键值对
del menu['noodles']
in：
要避免key不存在的错误，有两种办法，一是通过in判断key是否存在：

>>> 'Thomas' in d
>>> False

get()：
二是通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value：

>>> d.get('Thomas')
>>> d.get('Thomas', -1)
>>> -1

### 利用items()方法遍历输出键和值
for key,value in menu.items():
    print('\nkey:'+key)
    print('value:'+value)

结果
key:fish
value:40
key:pork
value:30
key:potato
value:20
key:lamb
value:50


### 利用keys()方法遍历输出键
for key in menu.keys():
    print(key)


结果
fish
pork
potato
lamb

### 利用values()方法遍历输出值

for value in menu.values():
    print('food_price:'+value)
输出结果：
food_price:40
food_price:30
food_price:20
food_price:50

-----------------------------------------------------------------------------------------
1列表中存储字典

### 创建3个菜单字典，包含菜名和价格
menu1 = {'fish':40, 'pork':30, 'potato':20,'noodles':15}
menu2 = {'chicken':30, 'corn':55, 'lamb':65,'onion':12}
menu3 = {'bacon':36, 'beaf':48, 'crab':72,'eggs':7}
### 将3个菜单字典存储到列表menu_total中
menu_total = [menu1,menu2,menu3]
### 输出列表
print(menu_total)


2字典中存储列表

我们也可以在字典中存储列表，比如我们对于一份菜单，菜名作为键，而值我们想是这道菜的配料，那么我们就可以将这些配料作为列表存储，然后作为值存储在字典中。例如：
### 初始化menu菜单，里面包含配料列表
menu = {'fish':['vinegar','soy','salt'], 'pork':['sugar','wine']}、
### 输出pork这道菜的配料
print('The burding of pork is:',menu['pork'])	

3字典中存储字典

### 创建一个字典menu_sum，里面包含两个子菜单字典menu1和menu2
menu_sum = {
    'menu1':{'fish':40, 'pork':30, 'potato':20,'noodles':15},
    'menu2':{'chicken':30, 'corn':55, 'lamb':65,'onion':12}
}

---------------------------------------------------------------------------------------------
# 元素集

s = set( [1,2,3] )

set和dict类似，但是只存储key

>>> s = set([1, 2, 3])
>>> s
>>> {1, 2, 3}

注意！传入的参数[1, 2, 3]是一个list，而显示的{1, 2, 3}只是告诉你这个set内部有1，2，3这3个元素，显示的顺序也不表示set是有序的。。

add(key)			添加
remove(key)		删除
### set相当于集合，可以进行交集（&）、并集（|）等操作
# 函数

默认参数：
定义默认参数要牢记一点：默认参数必须指向不变对象！

可变参数：
（可变参数就是传入的参数个数是可变的）（实质就是传入list和tuple）
定义和使用都要加个*
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


calc(nums[0], nums[1], nums[2])#太麻烦了

如果已经有了一个list或者tuple：
Python允许你在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去。
关键字参数：
**（就是可以传入字典）
前面加**表示，关键字参数可以扩展函数功能，使传递参数过程更为简便，例如：
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)


>>> person('Michael', 30)
>>> name: Michael age: 30 other: {}

>>> person('Bob', 35, city='Beijing')
>>> name: Bob age: 35 other: {'city': 'Beijing'}

但是注意：
kw获得的dict是一份拷贝，对kw的改动不会影响到函数外的dict。

命名关键字参数
限制关键字参数的名字，就可以用命名关键字参数，例如，只接收city和job作为关键字参数。这种方式定义的函数如下：
def person(name, age, *, city, job):
    print(name, age, city, job)


>>> person('Jack', 24, city='Beijing', job='Engineer')
>>> Jack 24 Beijing Engineer

如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了：
def person(name, age, *args, city, job):
    print(name, age, args, city, job)


>>> person('Jack', 24, city='Beijing', job='Engineer')#命名关键字参数就是必须写参数名字!!!city= job=
>>> Jack 24 Beijing Engineer

参数组合
>它是有顺序的，必选参数     默认参数     可变参数   关键字参数。
>-->def plus(x, y, z=0, *args, **kw):
>关于return
>返回来的未必是一个数字，它是一个盒子，可以是一个元组，一个列表
>甚至可以返回一个函数。eg：uyyy
### 定义求和函数，返回的并不是求和结果，而是计算求和的函数
def lazy_plus(*args):
    def plus():
        s = 0
        for n in args:
            s = s + n
        return s
    return plus

### 调用lazy_plus()时，返回的并不是求和结果，而是求和函数
f = lazy_plus(1,2,3,4,5)
print(f)

输出结果：
<function lazy_plus.<locals>.plus at 0x000001DAC97F9950>


调用函数f时，才真正计算求和的结果：
### 定义求和函数，返回的并不是求和结果，而是计算求和的函数
def lazy_plus(*args):
    def plus():
        s = 0
        for n in args:
            s = s + n
        return s
    return plus
### 调用函数f时，得到真正求和的结果
f = lazy_plus(1,2,3,4,5)
print(f())

输出结果：15

---------------------------------------------------------------------------------
Python的作用域
特殊变量__xxx__
私密变量_xxx（private）注：是“不应该”被直接引用，而不是“不能”被直接引用。

### 私密函数同理
三目运算符：

winner =  x   if  x>y  else y          
	       1                      0

----------------------------------------------------------------------------------------
generator生成器
创建一个生成器
第一种方法类似创建列表
g = (x * x for x in range(10))
>>> L = [x * x for x in range(10)]
>>> L
>>> [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> g = (x * x for x in range(10))
>>> g
>>> <generator object <genexpr> at 0x1022ef630>

如果要一个一个打印出来，可以通过next()函数获得generator的下一个返回值：
>>> next(g)
>>> 0
>>> next(g)
>>> 1
>>> next(g)
>>> 4
>>> next(g)
>>> ......
>>> next(g)
>>> 81
>>> next(g)
>>> Traceback (most recent call last):
>>> File "<stdin>", line 1, in <module>
>>> StopIteration

generator保存的是算法，每次调用next(g)，就计算出g的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。
正确的方法是使用for循环，因为generator也是可迭代对象。

定义generator的第二种方法。如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
调用该generator时，首先要生成一个generator对象，然后用next()函数不断获得下一个返回值：
>>> o = odd()
>>> next(o)
>>> step 1
>>> 1
>>> next(o)
>>> step 2
>>> 3
>>> next(o)
>>> step 3
>>> 5
>>> next(o)
>>> Traceback (most recent call last):
>>> File "<stdin>", line 1, in <module>
>>> StopIteration

在类似函数的generator中，遇到yield就中断，下次又继续执行。执行3次yield后，已经没有yield可以执行了，所以，第4次调用next(o)就报错。
但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中：
>>> g = fib(6)
>>> while True:
>>> ...     try:
>>> ...         x = next(g)
>>> ...         print('g:', x)
>>> ...     except StopIteration as e:
>>> ...         print('Generator return value:', e.value)
>>> ...         break
>>> ...
>>> g: 1
>>> g: 1
>>> g: 2
>>> g: 3
>>> g: 5
>>> g: 8
>>> Generator return value: done

# Iterator迭代器

可以直接作用于for循环的数据类型有以下几种：
一类是集合数据类型，如list、tuple、dict、set、str等；
一类是generator(生成器），包括生成器和带yield的generator function。
这些直接用于for循环的对象统称为可迭代对象：Iterable。
而像生成器这样可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator
（生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。）
把list、dict、str等Iterable变成Iterator可以使用iter()函数：
为什么这样他们是Iterable 但不是Iterator？？
Iterator：边迭代边计算下一个，但我们却不能提前知道序列的长度。它可以是一个长度未知的数据流。
但list，dict，str肯定是已知长度的序列。
（Python的for循环本质上就是通过不断调用next()函数实现的)。

# 函数式编程

高阶函数
map:

>>> def f(x):
>>> ...     return x * x
>>> ...
>>> r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> list(r)
>>> [1, 4, 9, 16, 25, 36, 49, 64, 81]


reduce:
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)


filter:
filter()把传入的函数依次作用于每个元素，根据返回值是True还是False决定保留还是丢弃该元素。
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))

结果: [1, 5, 9, 15]



## sorted：

Python内置的sorted()函数就可以对list进行排序：

>>> sorted([36, 5, -12, 9, -21])
>>> [-21, -12, 5, 9, 36]

要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True：
>>> sorted([36, 5, -12, 9, -21], key=abs)
>>> [5, 9, -12, -21, 36]

key=str.lower
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
>>> ['Zoo', 'Credit', 'bob', 'about']



函数作为返回值











# 爬虫

## 文件处理，模块:OS

f = open("text.txt","r")    #不填写模式的话，默认为read
content = f.read(10)        #每次读10个字符，指针自动移动
content = f.readline()      #每次读一行，指针自动移动
content = f.readlines()     #文本会被读到内存里，变成列表，每行是一个字符串
print(content)
f.close()

os模块下，还有很多关于文件的操作....
异常处理

```python
try:
    print("hi!")
    open("123.txt","r")
    print("hello!")
except IOError:               #如果捕获到IO异常：
    pass


except (IOError , NameError): #也可以写多个种类的异常
except (IOError , NameError) as result:#把错误信息存进变量result里
    print(result)

except Exception as result:   #Exception包含了所有异常
    print(result)
```

给一个主函数入口，更加清晰：
 if __name__ == "__main__":
#当程序执行时，调用函数

## urllib

伪装成浏览器，发送请求，两种请求方式：

```python
import urllib.request

#*获取一个get请求
response = urllib.request.urlopen("http://httpbin.org/get")#它会返回一个对象
print(response.read().decode("utf-8"))                   #解析，发现这个对象里封装着这个网页的源码


#*获取一个post请求，(带一个表单，存用户名密码等信息)
```

```python
import urllib.parse#解析器
data = bytes(urllib.parse.urlencode( {"hello":"world"} ),encoding="utf-8")
#把字典里的内容，解析，转化成二进制，封装进data里

response = urllib.request.urlopen("http://httpbin.org/post",data=data)  #data作为传的内容，放进去
print(response.read().decode("utf-8"))
```

超时处理：

```python
#超时处理
import urllib.request
try:
    response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.01)
    print(response.read().decode("utf-8"))                
except urllib.error.URLError as e:
    print("time out...QAQ")

HTTP Error 418:(被发现是个爬虫)
因为，这样直接request一个网址，给网站发送请求的时候，headers里的信息，显示你是Python，urllib
url = "http://httpbin.org/post"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
data = bytes(urllib.parse.urlencode({"name":"647"}),encoding = "utf-8")
req = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
```

PS:怎么知道自己浏览器发送的headers是什么呢
chrome浏览器——F12——network——刷新一下网页，开始再暂停

第一个数据流里 ，就包含了request，里面有headers，还有cookie。













# 自动化selecnium

> 浏览器（chrome内核） + 对应版本的Chromedriver.exe







