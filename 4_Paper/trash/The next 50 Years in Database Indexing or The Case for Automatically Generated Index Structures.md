# The next 50 Years in Database Indexing or: The Case for Automatically Generated Index Structures
















## Abstract

本文提出了一个新的自动索引生成框架：*Genetic Generic Generation of Index Structures (GENE).*

基于观察，几乎所有索引结构都由三种维度组合而成：

1. 几种结构构建块(eg: 内节点/叶节点)
2. 一组常量(eg: B-tree所有路径都是等长)
3. 节点内部的数据布局

本文提出一个通用的索引框架，可以模拟许多现有的（依据上述三种维度设计的）索引结构。

基于这个框架，提出*a generic genetic index generation algorithm*：给定工作量和优化目标，能够自动组装和变异出新的索引结构。

目标：给定一个具体的workload，GENE能否繁育出一个索引结构，与现有教材和论文推荐的结构水平相当？是否能做的更好？



## Introduction

- **Problem1**：索引被视作统一实体

  本文认为Index应明确分为logical和physical两类。

- **Problem2：**解决类似的问题，采用了两种完全不同的方法

  指的是设计索引结构Index structure和查询计划query plan的方法。索引结构的设计太死板。为什么不能像查询一样，从逻辑和物理层面分别设计，最终自动组装出一个复杂的索引解决方案呢。

- **Problem Statement：**

  1. 如何将多种最为重要的索引结构概括成通用的概念上的索引框架。
  2. 如何使用1来自动生成框架。

- **Contributions**

  1. 一个通用索引框架，明确区分逻辑，物理索引。（受到逻辑算符、物理算符的启发）
  2. 一个通用算法，高效自动生成（繁殖）索引。
  3. 广泛实验评估，证明了我们可以重新发现以前的手工索引以及新型混合索引。

## 通用逻辑索引框架

![image-20220729022543924](The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220729022543924.png)

教科书总是把物理实现(red)，和逻辑功能(black)同时介绍。这违反了索引结构的物理数据的独立性。

我们想要明确分离索引的逻辑、物理两方面。
$$
\begin{align*}
基本定义：&概型[R]:\{[A_1:D_1,...A_n:D_n]\}，[R]具有属性A_i和对应的D_i（D_i是不确定的一维域）\\\\

&\sigma_p(R):表示R上的一个查询.p是定义在关系概型[R]上的函数:[R]\rightarrow\{true,false\}, 
\sigma_p(R)\subseteq R.\\\\

&\sigma_{l\leq A_i\leq h}(R): 表示对[l:h]的区间查询，得到所有的元组 t=（a_1...a_n)\in R，\\
&常量l,h\in D_i,如果\enspace l=h,则为点查.\\
\end{align*}
$$

### 逻辑节点和逻辑索引

$$
\begin{align*}
定义2.1：&逻辑节点(p,RI,DT),其中\\
&p:划分函数[R]\rightarrow D\\
&RI: 路由信息函数D\rightarrow\mathcal{P}(N)(点集N的幂集)\\
&DT = data，是在关系概型[R]下的元组的集合 \\
&\\
\end{align*}
$$

注意：RI不暗示任何物理实现。p可能未定义，RI，DT可能为空集。

也就是说，D中每一个元素（即划分函数的计算结果）都映射到点集N的某子集。RI所映射到的点集记作nodes(RI)。





用上述定义，实现多种结构，举例：

1. B-tree with ISAM

   <img src="The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220729032812970.png" alt="image-20220729032812970"  />

2. [RMI](https://zhuanlan.zhihu.com/p/415918824)：(Recursive-model-Index)

   通过，划分函数p和RI配合，把区间[0:12]压缩成[0:4]

   

   ![image-20220721175227515](D:/MyFile/md/50th.assets/image-20220721175227515.png)

3. Extendible hashing动态可拓展哈希表

   ![image-20220721225247784](D:/MyFile/md/50th.assets/image-20220721225247784.png)

   

4. [radix tree](https://ivanzz1001.github.io/records/post/data-structure/2018/11/18/ds-radix-tree)基数树

![image-20220721225133024](D:/MyFile/md/50th.assets/image-20220721225133024.png)

**完全逻辑索引 a complete logical index**

当LN的节点中的所有路由信息都指向LN中的节点，称为完全逻辑索引。

这说明：完整的逻辑索引是一个图。

**Running Example：**

![image-20220722015800213](D:/MyFile/md/50th.assets/image-20220722015800213.png)

示范：他提出的模型可以对传统索引结构进行任意混合（hybrid）

### 逻辑查询

递归遍历查找图中所有符合逻辑的节点。而对于非树状结构，比如更通用的DAG，具体算法实现要防止对同一节点的多次访问。

**逻辑索引的正确性：**在任意的low到high之间的任意查询，结果都正确，则逻辑索引正确。

注：本文所有内容都是在DAG（无环有向图）基础上讨论，并且假定选定了相应的起始节点SN。


## 通用物理索引框架

对于每个逻辑节点，我们最终都要指定如何实现。

make a physical decision：

- search algo
- data layout
- 嵌套，委托这些决策。

任何一个逻辑节点，如果被有效地指定了物理实现，就成为了物理节点。











### 搜索算法

定义了搜索算法，它是用来搜索，RI或者DT中的K-V pair的；一旦找到了符合条件的key就立刻停止；

1. scan	
2. binS    二分
3. intS     [插值查找](https://zhuanlan.zhihu.com/p/133535431) 
4. expS   指数查找
5. hashS  
6. linregS 线性递归查找预测位置
7. hybridS   任何合适的算法，例如上述内容的组合。

### 数据布局

选定数据布局,来组织RI，和DT的数据。

1. col vs row：k-v对采用行或列布局。
2. func：用函数确定RI，（DT）//这里假定DT是一个实际存在的集合，但是实际上也可能被建模成映射
3. unsorted vs sorted：可选是否按key排序
4. comp：压缩情况
5. hybridDL：也可以是混合式的data layout

![image-20220729044422769](The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220729044422769.png)









## 遗传索引生成

介绍遗传算法，能够自动生成索引

### Core Algo

<img src="D:/MyFile/md/50th.assets/image-20220728151132570.png" alt="image-20220728151132570" style="zoom:80%;" />

### 初始化种群

首先，种群的初始大小$S_{init}$，它基本上决定了初始索引集的多样性

第二，要自行决定如何建立DataSet的初始物理索引，有以下选项

1. 从一个单一的不含data的物理节点开始变异，然后逐渐插入data。成本太高，舍弃。
2. 一个单一的包含所有data的物理节点。数据布局、搜索算法随机选定，或根据工作负载手工指定。
3. 自底向上地批量加载，对于所有节点，搜索算法和数据布局都是随机选取的。（目前，不支持hash型作为内节点）这样做返回结果在逻辑上类似于标准B树，但物理节点差别较大。
4. 初始种群包含现有的非常领先的手工索引结构。这样也可以检验我们的遗传算法是否仍能对齐进行优化。

从1~4的过程中，给定的初始条件越来越好，假设移除GENE的负载，使用它更像是作为一个提纯精炼器（一个细化工具）。

已有结构越是有效，我们越希望只发生一些小突变。但实际上，即使给定一个具体的物理实现，（因为有选择各个突变的自由度），结果仍有可能作出一些意想不到的转变。

### 突变和概率分布

介绍一组合适的突变集并示范如何在算法中应用。

**Mutation：**突变是一个函数，Index->Index，输出修正后的Index。
突变中，只保证查询结果的正确。（只考虑树状结构中的突变，这不是框架的限制，而是为了易于理解）



**Mutation distribution：**

MD：突变的概率分布，可以为不同的突变分配不同的概率，可以指定优先某种突变

ND(π_min，m）：确定突变的起始节点

PD（m，N）：怎样物理实现这个节点的突变。

（对于不匹配的数据布局和搜索算法，比如二分查找+unsorted data，在该分布中将概率设为0）



**一些基本的突变：**目标是通过一组尽可能的突变集，来产生各种各样的索引。

1. 改变Data Layout

2. 改变搜索算法

3. 水平合并同级节点

4. 将一个子节点水平拆分为k个节点

   ![image-20220729044800957](The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220729044800957.png)

5. 垂直合并同级节点

6. 将子节点垂直拆分为k个节点

   ![image-20220729044812323](The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220729044812323.png)



### 适应度函数

它是丈量优化程度的指标。

我们已经明确优化索引结构，是要在运行时给定工作量 （由点查，查询范围组成）的情况下进行优化。

适应度函数的实际情况取决于你的优化目标，比如查询时间，占用内存，能效。甚至例如对于索引的复杂度可以设置一个惩罚值...等等，可以对具体需求建模。

## 相关工作

**手工索引**

基于B树的变种和优化，基于基数树的，基于哈希表的工作都已经做的很好了。

**学习型索引**

节点内的布局，搜索算法仍是固定的，即物理结构仍是手工确定的。这是在手工构建的结构中，对参数、权重的学习，而不是结构本身。而本文是在优化整个索引结构。

**Periodic Tables and Data Calculator**

[25] [Design Continuums and the Path Toward Self-Designing Key-Value Stores that Know and Learn](http://cidrdb.org/cidr2019/papers/p143-idreos-cidr19.pdf)

[27] [The Periodic Table of Data Structures](http://sites.computer.org/debull/A18sept/p64.pdf)

[28] [Learning Data Structure Alchemy](http://sites.computer.org/debull/A19june/p47.pdf)

[29] [The Data Calculator : Data Structure Design and Cost Synthesis from First Principles and Learned Cost Models](https://dl.acm.org/doi/pdf/10.1145/3183713.3199671)

这些工作与本文工作类似。其中也实现了混合设计，但这仍是帮助工程师寻找更优索引结构的推理判断工具。与之相比我们的工作：

1. 关注全自动索引构建
2. 逻辑和物理索引组件的清晰分离
3. 在实际系统中对索引结构的全面建模开销太大，无法训练模型，只能选择遗传优化
4. 优化时间没有那么重要，索引结构的创建是离线的（与查询时创建索引实例不同)。因此,应该尽量通过（fitness function）实际观察运行时的测量值，而不是成本模型。

**通用框架**

GIST XXL这些框架希望把不同的索引结构归纳为一个通用的软件框架，这反过来允许架构师实现通用的索引算法，专用索引也可以更容易地调整以适应通用算法。

但这些工作是面向对象层面的，而本篇的工作是概念级的论证。

通过类比分离出逻辑关系，不急于立即物理实现。(ONC, vectorization,SIMD, whatever)



## 实验评估

**环境：**1900X，32GB，on Linux

C++ and compiled with Clang 8.0.1, -O3.

All experiments are run single-threaded and in main-memory.

**Dataset：**data.key  64bit    data.offset  64bit

![image-20220727165751429](D:/MyFile/md/50th.assets/image-20220727165751429.png)

$uni_{dense}$ [0,n) (size=n)

$books$  $osm$ 代表复杂分布的真实数据

根据所需大小，无重复地绘制元素。

**Workload：**

![image-20220727172453834](D:/MyFile/md/50th.assets/image-20220727172453834.png)

三类：点查，范围查询，二者混合。

Point (data，idx_min，idx_max）表示在子域[idx_min，idx_max）中等概率选择索引，进行点查。

Range_sel (data，idx_min，idx_max) 表示在子域[idx_min，idx_max）中等概（不越界地）选择下界，上界是根据数据集大小和sel（区间长度占整个数据集的比例）设置的。

Mix（data，P，R）P，R分别是设置好的点查和范围查询负载。



注：

暂时，只有只读工作负载；（无insert，delete，update语句，但框架是支持插入和删除的，而且update不会改变索引结构，也易于集成进框架中）

如果不指定域，就默认为整个DataSet；

数据集取样无重复，但Workloads可能重复。



**搜索算法与数据布局：**

使用的搜索算法：scan, binS, intS, expS, and hashS

数据布局：

![image-20220727173937837](D:/MyFile/md/50th.assets/image-20220727173937837.png)



### Hyperparameter Tuning

使用100K的$uni_{dense}$对下面五个参数进行调整：

1. 突变次数 S_maxc {10,50}
2. 种群人口上限S_∏ $\in${50,200,1000}
3. 竞争时的采样率 S_T  $\in${10%，50%，100% of  population size}
4. 初始种群大小 $\in${10,50}
5. 人口插入标准：不取竞争期间采样的子集的中值，定义了一个百分数q$\in${0%，50%，100%}，表示“要优于种群中比例为q的个体，该突变体才能加入种群”

![image-20220728150223339](D:/MyFile/md/50th.assets/image-20220728150223339.png)

最终选定：$S_{max} = 10, S_∏= 50, S_T= 25, S_{init} = 10 , q= 50%.$



### Rediscover

证明该遗传算法能再现教科书中各种基本索引结构的性能。

**数据集：**uni~dense~、 books of sizes 100K,1M,10M,100M

**三种工作负载：**  

Point(uni~dense~/books)，Range$_{0.001}$ (uni~dense~/books)，

Mix(uni~dense~/books, P, R)   // 80% point and 20% range queries 

**Baseline：** 

- 点查：simple hash table——单点内哈希表。
- 范围查询和混合查询：B-tree-like structure——具有100个完全填充的叶节点，每个叶子包含1000个元素，并且内节点扇出为10个元素。每个节点都是数据布局都是sorted_col，搜索算法都是binS

**配置GENE：**每个节点最多包含100，000键值对或子分区。初始种群中，采用与上述相同的树结构，但数据布局和搜索算法都是随机的。每个实验执行8000世代。每当找到一个更好的结果，就用与更大的数据集（必要时增加叶结点容量），然后再用完全相同的工作量进行评估。



![image-20220728163020968](D:/MyFile/md/50th.assets/image-20220728163020968.png)

**结果:**

GENE可以迅速达到baseline，因为通过突变可以很容易在一开始时改善那些低效率的节点。达到baseline后，GENE的改善很小。GENE寻找到的索引结构往往和baseline非常相似。

**对于稠密集uni~dense~，**GENE总是返回单节点。仅有点查时返回的是含所有条目的hash node；范围查询和混合查询，返回的都是sorted_col+intS。

**对于books，**点查返回的树有68节点，66个叶子结点。除了一个叶结点通过树节点连接root外，其余都是直接连在root上的子节点。48个节点是hash布局，其余是sorted_col布局，或树(map)布局。在non-hash 节点中，除3个使用expS指数搜索外，其余都是binS；范围查询返回44个节点的树，共三层，多数叶结点在第二层，sorted_col布局，主要搜索算法是binS，2个intS，2个expS；混合查询与范围查询类似。



此外，GENE的执行时间很大程度上取决于DataSet和WorkLoads，最快的执行：uni~dense~ + 点查，找到最后一个改进的时间< 3min。而同一个数据集上的范围查询，需要122min

扩大数据集会进一步影响运行时，最慢的workload是books上的范围查询，30h

### 优化vs启发式

与三种具体索引结构进行对比。（混合查询）

![image-20220728175934874](D:/MyFile/md/50th.assets/image-20220728175934874.png)

为了和上述结构竞争，额外给定了具体的物理结构。

![image-20220728181839095](D:/MyFile/md/50th.assets/image-20220728181839095.png)



![image-20220728180000202](The%20next%2050%20Years%20in%20Database%20Indexing%20or%20The%20Case%20for%20Automatically%20Generated%20Index%20Structures.assets/image-20220728180000202.png)

这证明了，在一些用例下，自动生成的索引很有竞争力，甚至可能性能更优。

## Conclusion and Future Work

**Conclusion：**

为自动索引生成开辟了道路，提出了强大的通用索引框架。通过清晰地分离索引的逻辑和物理维度，可以在通用框架中表示大量现有索引。此外引入了GENE来自动生成索引结构。而且初步试验结果良好。

**Future Work：**

1. 能够直接生成代码
2. Index Farm：开源，让人们在网页上提交工作负载，返回索引结构的源代码。
3. runtime adaptivity：如何在结构上进行变异
4. updates：探索insert，update，delete
5. 可测量性：选择突变节点时，使用成本函数，仅评估突变对子树的影响，以优先考虑一些代价比较高昂的分区。
6. 内节点中，非空DT的影响
7. 扩展GENE以支持更多数据布局、搜索算法和硬件加速（SIMD）。

