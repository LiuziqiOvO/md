---
marp: true
---



# ZNS+

ZNS+: Advanced Zoned Namespace Interface for Supporting InStorage Zone Compaction(https://www.usenix.org/system/files/osdi21-han.pdf)

https://blog.csdn.net/marlos/article/details/130234764

## Abstract

ZNS+: Advanced Zoned Namespace Interface for Supporting In-Storage Zone Compaction

-本文提出了一种名为ZNS+的新型支持LFS的ZNS接口及其实现，该接口允许主机将数据复制操作卸载到固态硬盘，以加快分段压缩。为此提出了两种文件系统技术：copyback感知块分配和混合分段回收。

-经实验，提出的 ZNS+ 存储系统的性能比基于 ZNS 的普通存储系统的性能好 1.33-2.91 倍。

## 1 Intro

段压缩：(也称为段清理或垃圾收集)

略

## 2 Backgroud

#### 2.1 SSD一些名词

parallel flash controllers (channels)

flash chips (ways)

chunk：由于现在的flash产品的flash页面大小通常大于逻辑块大小(例4 KB)，在本文中，我们将映射到flash页面的逻辑连续块称为chunk。（chunk指的是SSD中真实的一个page单元，但目前工艺已经大于4 KB了）

貌似这篇文章:chip = plane

一个memory chip通常支持：read, program, erase, and copyback 命令。

copyback指的是chip内的数据复制，单位是chunk。由于chip内的转移不能检查ECC，所以闪存控制器会在拷贝操作的同时检查错误。

#### 2.2 Zone Mapping

FBG(Flash Block Group)：一个zone映射到的一串物理块组。为了提高并行性，要放在不同的chip上，并行的chip数称为交错度（$D_{zone}$）。跨chip的连续块称为条带（stripe），以交错度为除数分成chip组（FCG），如下图：

Flash Chip Group,FCG

Flash Block Group,FBG

![image-20230828102735073](ZNS.assets/image-20230828102735073.png)

以上设计使得SSD只需要维护 Zone-FBG 映射。

一个zone的reset命令：分配新的FBG（更改对应的映射），写指针（WP）指向新的位置。等旧FBG擦除完可以给其他zone重新使用。

#### 2.3 F2FS 

>F2FS是Flash Friendly File System的简称。该文件系统是由韩国[三星](https://www.elecfans.com/tags/三星/)[电子](https://www.hqchip.com/ask/)公司于2012年研发，只提供给运行[Linux](https://www.elecfans.com/v/tag/538/)内核的系统使用，这种文件系统对于NAND闪存类存储介质是非常友好的。并且F2FS是专门为基于 NAND 的存储设备设计的新型开源 flash 文件系统。特别针对NAND 闪存存储介质做了友好设计。F2FS 于2012年12月进入Linux 3.8 内核。目前，F2FS仅支持Linux[操作系统](https://m.elecfans.com/v/tag/527/)。

F2FS：

- 包含6种类型的数据段（2M），同类段一次只能打开一个；//将冷热数据分割成不同的数据段，压缩时冷块会被放入冷段。

- 多头日志策略；//?

- 同时支持append logging，threaded logging。既可以严格顺序写， 也可以写入脏块的废弃空间。

- **日志写入自适应**：如果空闲段足够多，优先追加写入；空闲段不足，将数据写入dirty segment的无效块上。然而， 实际上后者在ZNS中是被禁用的，所以F2FS for ZNS会经常触发压缩。

- 前后台压缩机制：空间不足，先前台压缩（造成少量IO延迟）；闲时后台压缩（无法及时回收，尤其是在空间占用高，突发写请求时）

  本文主要关注前台压缩的性能

![image-20230829135007905](ZNS.assets/image-20230829135007905.png)

## 3 ZNS+ Interface and File System Support

### 3.1 动机

**普通的端压缩**

朴素的LFS端压缩包括四个步骤：

1. 受害者段（victim segment）选择
2. 目标块分配
3. 有效数据复制
4. 元数据更新

![image-20230829143324993](ZNS.assets/image-20230829143324993.png)

其中，SSD的空闲间隔很长（idle）

read phase、write phase、metadata update ~？？

**基于IZC的段压缩方案**

![image-20230829160053722](ZNS.assets/image-20230829160053722.png)

引入了copy offloading操作，sends zone_compaction commands to transfer the block copy information 

### 3.2 LFS-aware ZNS+ Interface

三个新命令：zone_compaction, TL_open, and identify_mapping.

zone_compaction用于请求IZC操作（区内压缩）：现有的simple copy命令要求目标地址单一、连续；ZNS+下，可以指定多个目标LBAs

TL_open：打开区域，准备threaded logging。接下来这个区域可以不经reset就覆写。

identify_mapping：主机使用这个命令确定各个chunk所在的flash chip

##### 3.2.1 IZC(Internal Zone Compaction)

ZNS+的压缩流程：

###### （1）Cached Page Handling：

检查victim段各个可用块对应的page是否被主机DRAMcache。If Cacheed page dirty：必须被写入目的段，并排除在IZC操作外；If clean：既可以通过写请求从主机传输写入，也可以从SSD内部复制。

//ZNS一般使用TLCorQLC，内部复制没有主机来得快。然而，最新的ZNAND有极短的读延迟，对于ZNAND SSD，in-storage copy也可能更快。

###### （2）Copy Offloading：

zone_compaction(sourceLBAs, destination LBAs)

###### （3）处理 IZC

ZNS+ SSD处理压缩指令，其中定义了copybackable chunks（如果其中所有块都是复制来的）。其他不可回拷的正常读写。

**异步**

zone_compaction请求的处理是异步的，主机请求进入请求队列后不会等待命令完成。LFS有自己的checkpoint，异步不会影响文件系统一致性。

ZNS+对后续的普通请求重新排序，避免zone compaction操作的长延迟的影响：放行与压缩地址无关的普通请求；甚至包括对正在压缩的区域的读请求，如果写指针WP已经经过了要读取的目标块地址，那么也可以放行。

##### 3.2.2 Sparse Sequential Overwrite 

**Ineternal Plugging**

为了支持 F2FS的threaded logging，ZNS+需要做少量顺序覆写。

尽管二者有冲突，但是：threaded logging访问的脏段的块地址的闲置空间时，也是从低地址端向高地址端的，虽然不连续但是也递增。因此说他的访问模式是 Sparse Sequential Overwrite （即——WP不减小）

如果固态硬盘固件读取请求之间跳过的数据块，并将其合并到主机发送的数据块中。那就变成了密集的连续写入请求——这种技术被称为internal Plugging。

![image-20230829172811964](ZNS.assets/image-20230829172811964.png)



上图是一个Plugging操作的例子：chunk0中的AB，是有效块（跳过块），PQ是无效块，需要回收。

**Opening Zone for Threaded Logging** 

SSD必须知道目标段的跳过块：通过对比写请求首个LBA和当前WP（维护的是上次写的位置？），SSD确定哪些是跳过块。然而，必须要等到写请求到达才能确定跳过块，产生了延迟。

因此，增加了TL_open这个特殊命令，TL_open(openzones, valid bitmap)。它会提前发送一个bitmap，SSD可以在thread logging的写请求到达之前确定那些块要跳过。

**LogFBG Allocation**

原有的被"TL_opened"的zone要被重写，新分配一个FBG叫LogFBG（图中， original FBG (FBG 6) and the LogFBG (FBG 15)）

由于静态映射机制，这个新分配的LogFBG也是在同一个chip上的，所以可以使用copyback快速完成；TL_opened的区域最终关闭时，LogFBG替换了原始的FBG，原始LGB被释放以供重用。



//以上内容应该对应图中的chip0的情况。

![image-20230829172811964](ZNS.assets/image-20230829172811964.png)

**LBA-ordered plugging**

按地址有序插入，如图中2-p、3-p、4-p的情况。

**PPA-ordered plugging**

比如说chunk3可以在chun0、chunk2中的写请求到来之前就进行复制。

physical page address (PPA)   即只考虑物理地址的顺序写入约束。可以检查并让后续的完整chunk提前copy。

但是，过多提前的plug会干扰用户IO请求，所以只有目标chip空闲时才会进行。

**为什么Threaded Logging能提升性能**

二者copy的块的数量是相同的。但是，threaded logging减少了重定位时元数据的修改（?）；调用空闲的chip，internal plug的开销部分隐藏了；最小化写入请求的平均延迟



### 3.3 ZNS+-aware LFS Optimization

#### 3.3.1 copyback-aware的块分配机制

**现有LFS未充分利用copyback：**

![image-20230831170443421](./ZNS.assets/image-20230831170443421.png)



对于identify_mapping 命令，ZNS+SSD会返回FCG ID和chip ID

#### 3.3.2 混合式段回收

虽然threaded logging减少了回收开销，但其效率依然低于端压缩，两大原因：

**回收成本不均衡**

段压缩可以直接选取压缩成本最低的受害者段（例如，选有效数据最少的）。但threaded logging只能从同类型的脏数据段中为某写入请求选择目标数据段，以防止不同类型的数据混杂在一个数据段中。

**预失效块问题**

如果长时间使用稀疏到的线性日志写而不进行检查点处理，它的回收效率将进一步下降:
这是由于某些块虽已经失效，但仍被存储元数据引用，因此不可回收。当一个逻辑块被文件系统操作作废，但新的检查点仍未记录时，该逻辑块就会成为预作废块(预失效块)，不得覆盖，因为崩溃恢复需要恢复它。

预无效块会随着threaded logging的继续而累积，而它们可以通过段压缩来回收，因为段压缩伴随着检查点更新。

***

**定期检查点**
为了解决预无效块问题，我们使用定期检查点，每当累积的预无效块达到一定数量，触发检查点。这需要文件系统进行监测，元数据块上的写入流量就会增加，如果过于频繁地调用检查点，固态硬盘的闪存耐用性就会受到损害。因此需要一个合适的阈值——128 MB
**回收成本模型**
我们提出了混合段回收（HSR）技术，通过比较线程日志和段压缩的回收成本来选择回收策略。
Threaded Logging 的开销：
$$C_{TL} = f_{plugging}(N_{pre-inv}+N_{valid})$$

段压缩的开销：
$$C_{SC} = f_{copy}(N_{valid})+ f_{write}(N_{node}+N_{meta}) - B_{cold}$$

B_cold 表示冷数据块迁移的未来预测收益。

(感觉这部分有点随意)

## 4 实验

**一些配置信息：**
模拟器：基于FEMU 
2 GB of DRAM, 16 GB of NVMe SSD for user workloads, and a 128 GB disk for the OS image 
Host interface: PCIe Gen2 2x lanes (max B/W: 1.2 GB/s)
SSD： 默认存储介质是MLC,  The data transmission
默认的ZNS+ SSD zone size=32 MB, 包含16 flash blocks分布在16 flash chips.
（注：The copyback operation is approximately 6–10% faster than the normal copy operation）
**两种不同版本的ZNS+**
IZC：不包含threaded logging
ZNS+： 混合式

### 段压缩表现：

ZNS与IZC在不同负载下的段压缩表现（模拟器）

![image-20230913060105924](image-20230913060105924.png)

与 ZNS 相比，IZC 通过移除主机级复制，将区域压缩时间减少了约 28.2%- 51.7%。IZC存储内复制操作减轻了用户 IO 请求对主机资源和主机到设备 DMA 总线的干扰。但IZC技术增加了检查点延迟。

### threaded logging

in-storage zone compaction 与 threaded logging 下的效果
注： IZC(w/o cpbk) 和 ZNS+(w/o cpbk)即禁用回拷的版本

![image-20230913061344093](./ZNS.assets/image-20230913061344093.png)

***

##### 元数据开销对比：

![image-20230913061910497](./ZNS.assets/image-20230913061910497.png)

***

##### 性能对比、WAF

(ZNS的WAF呢？)
![image-20230913062424226](./ZNS.assets/image-20230913062424226.png)



### 在真实SSD上的性能表现

![image-20230913062808434](./ZNS.assets/image-20230913062808434.png)



















## ZNS SSD的结构

> Zoned Namespace (ZNS) SSD 
>
> https://blog.csdn.net/Z_Stand/article/details/120933188

粗粒度单位——zone，每个zone管理一段LBA（Logic block adr），只允许顺序写，可以随即读；如果想覆盖写，就要reset整段LBA

End-To-End？绕过I/O stack（内核文件系统，驱动等等），通过Zenfs直接与ZNS-SSD交互

> ZNS+: Advanced Zoned Namespace Interface for Supporting InStorage Zone Compaction(https://www.usenix.org/system/files/osdi21-han.pdf)
>
> https://blog.csdn.net/marlos/article/details/130234764

<img src="ZNS.assets/image-20230808174737502.png" alt="image-20230808174737502" style="zoom:110%;" />



Flash Chip Group,FCG

Flash Block Group,FBG





















## SSD 各层级



![img](ZNS.assets/v2-bff1882898e377ce9ed29911fcea4a0d_b.jpg)



https://zhuanlan.zhihu.com/p/26944064

![image-20230807135849852](./ZNS.assets/image-20230807135849852.png)





1. DIE/LUN是接收和执行闪存命令的基本单元
   但在一个LUN当中，一次只能独立执行一个命令，你不能对其中某个Page写的同时，又对其他Page进行读访问。

2. 每个Plane都有自己独立的Cache Register和Page Register，其大小等于一个Page的大小。

3. Multi-Plane（或者Dual-Plane），主控先把数据写入第一个Plane的Cache Register当中，数据保持在那里，并不立即写入闪存介质，等主控把同一个LUN上的另外一个或者几个Plane上的数据传输到相应的Cache Register当中，再统一写入闪存介质。

4. 闪存的擦除是以Block为单位的
   那是因为在组织结构上，一个Block当中的所有存储单元是共用一个衬底的（Substrate）



**Read Disturb 读干扰**
读干扰影响的是同一个block中的其他page，而非读取的闪存页本身。
当你读取一个闪存页（Page）的时候，闪存块当中未被选取的闪存页的控制极都会加一个正电压，以保证未被选中的MOS管是导通的。这样问题就来了，频繁地在一个MOS管控制极加正电压，就可能导致电子被吸进浮栅极，形成轻微写，从而最终导致比特翻转
**Program Disturb 写干扰**
轻微写导致的，既影响当前的page也影响同一个block的其他page。
**存储单元之间的耦合**
导体之间的耦合电容

一个存储单元存储1bit数据的闪存，我们叫它为SLC（Single Level Cell），存储2bit数据的闪存为MLC（Multiple Level Cell），存储3bit数据的闪存为TLC（Triple Level Cell），如表3-1所示。


![在这里插入图片描述](ZNS.assets/2021050713384842.jpg)



>F2FS文件系统

三星开源，但是没有什么应用

https://blog.csdn.net/weixin_39886929/article/details/111679671



https://blog.csdn.net/weixin_44465434/article/details/113374562

EROFS







# eZNS: 

### An Elastic Zoned Namespace for Commodity ZNS **SSDs**

https://www.usenix.org/system/files/osdi23-min.pdf

## 0 Abstract

新兴的分区命名空间（ZNS）固态硬盘提供了粗粒度的分区抽象，有望显著提高未来存储基础设施的成本效益，并降低性能的不可预测性。（作者对ZNS的总结评价）

现有的ZNS SSDs 采用静态分区接口（zoned interface），它们无法适应工作负载的运行时行为；无法根据底层硬件能力进行扩展；共用区域相互干扰。

eZNS——这是一个弹性分区命名空间接口，可提供性能可预测的自适应分区，主要包含两个组件：

- zone arbiter，区域仲裁器，负责管理Zone的分配和激活plane里的资源。

- I/O scheduler，分层I/O调度器，具有读取拥塞控制和写入接纳控制。


eZNS实现了对ZNS SSD的透明使用，并弥合了应用程序要求和区域接口属性之间的差距。在 RocksDB 上进行的评估表明，eZNS 在吞吐量和尾部延迟方面分别比静态分区接口高出 17.7% 和 80.3%（at most）

## 1 intro

通过划分为Zone ，实现“从设备端隐式垃圾收集 (GC) 迁移到主机端显式回收” ，消除了随机写，解决写放大（WAF）问题。

要在ZNS上构建高效的I/O stack，我们应该了解：

1. 底层固态盘如何暴露接口并强制实现它的限制（怎么顺序写？）
2. 设备内部机制如何权衡成本与性能。（代价是什么？）

文章详细调研了一款ZNS产品，在zone striping, zone alloation, and zone
interference三个方面进行对比分析。旨在了解商用 ZNS 固态硬盘的特性。

提出eZNS，新的接口层，它为主机系统提供了一个与设备无关的分区命名空间。

- 减少了区域内/外的干扰（？）
- 改善了设备带宽（通过分配激活资源，基于应用优化的负载配置）

***

eZNS对上层应用和存储栈透明，包含两个组件：

- **区域仲裁器**

维护 “设备影子视图” （device shadow view，该视图本质上是SSD的虚拟表示，仲裁者使用它来跟踪当前正在使用哪些区域以及哪些区域可供分配。）

基于该视图来实现 “动态资源分配” 策略，这意味着它可以根据当前的工作量和其他因素调整分配给每个区域的资源量。

- **分层 I/O 调度器**

充分利用ZNS SSD没有硬件隐藏信息的特性，读取 I/O 的可预测性变得更强，可以直接利用这一特性来检查区域间的干扰。

此外，由于固态存在写入缓存，所有应用的写入操作共享一个性能域，所有zone都激活的时候会堵塞。因此对读进行本地拥塞控制，对写入全局准入控制。



## 2 背景&动机

#### 2.2 Zoned Namespace SSDs

namespace：类似硬盘的分区，但是被NVMe设备主控管理（而不是OS）

zone：多个blcok的集合

ZNS能为主机应用提供可控的垃圾回收；消除了设备内部I/O行为（主要指消除写放大）

三种命令：read, sequential write, and append.

**与上一篇文章有出入的地方：**与普通写入相比，区域追加命令不会在 I/O 提交请求中指定 LBA，而固态硬盘会在处理时确定 LBA 并在响应中返回地址。

因此，用户应用程序可以同时提交多个未完成操作，而不会违反顺序写入的限制。

#### 2.3 Small-zone and Large-zone ZNS SSDs

*physical zone*：最小的区分配单元，由同一个die上的一个或多个块组成。

*logical zone*：由多个物理区组成的条带区域

**区域划分大小的影响：**

*Small zone ZNS SSD*：提供粗粒度的大型逻辑区域，采用固定的条带化配置，跨越所有内部通道的多个die，不灵活，适用于zone需求少的情况。

*Large zone ZNS SSD*：每个区域都包含在单个die中，最小为一个擦除块。灵活，同时可激活的资源更多。最近有研究认为越小越好，可以减少区回收延迟造成的干扰，所以这个区域划分有待探究。

#### 2.4 The Problem: Lack of an Elastic Interface

ZNS SSDs带来的问题：在zone被分配、初始化之后，他的性能就已经固定了

1. 分区的性能只取决于分区位置的放置和stripe的配置。（但我们希望它的性能符合应用的需求）虽然，用户定义的逻辑分区已经带来了灵活性，但是应用不了解正在共享设备的其他应用的状态。目前，只能实现“次优”的性能表现。
2. 现有的接口不能适应负载的变化。专门开发一个应用来捕获I/O执行时的数据是不现实的。用户使用时，不得不以最坏的情况来配置分区。（over-provision）
3. 共用一块位置的区域互相影响，尤其当固态硬盘被过度占用时，其性能会按比例下降。



## 3 ZNS SSD的性能

(用测试说明现有的ZNS太固化，不灵活)

#### **3.1 Set up**

>SPDK

本文使用在 SPDK 框架上运行的 Fio 基准测试工具来生成合成工作负载。作者在 SPDK 中添加了一个薄层，以实现逻辑区域概念并实现不同的区域配置。

- 写入负载默认为单个逻辑区域上的顺序访问
- 读取负载默认为随即访问

![image-20230926214021627](image-20230926214021627.png)

#### **3.2 System Model**

<img src="ZNS.assets/image-20230807161309156.png" alt="image-20230807161309156" style="zoom:67%;" />

一个tenant=某个存储应用；它拥有一个或多个namespece；其中包含逻辑区域；一个逻辑区包含了多个物理区；物理区下面管理通道、die

/* 应用与NVME驱动之间存在一个 zoned block device (ZBD) layer

1. 在命名空间/逻辑区域管理方面与应用程序互动管理；
2. 考虑到应用需求，协调逻辑区到物理区的映射
3. 安排 I/O 序列，大限度地提高设备利用率并避免行头阻塞。*/

#### 3.3 Zone Striping

区域条带化是一种用于实现更高吞吐量的技术，尤其是大型 I/O。包含参数：

1. 条带大小：条带中最小的数据放置单位。 
2. 条带宽度：定义了同时激活的物理区域数量并控制写入带宽。

观察：当条带大小（stripe size）与 NAND 操作单元（这里是16KB）相匹配时，可以实现较好分条效率。

![image-20231004051937708](ZNS.assets/image-20231004051937708.png)

**Challenge #1: Application-agnostic   Striping**

stripe 最好与用户I/O匹配，太小了影响设备I/O效率，太大了浪费性能（单个zone性能变好了，但是可并行的zone总数低，影响其他应用）

（但是搞来搞去还是在等于pagesize时最好，动态调整的点在stripe width上）

#### 3.4 Zone Allocation and Placement

现有分配机制：找到下一个可用die，在这个die内根据磨损均衡等各种策略选择最好的块

图5：stripe size = 16KB，每个逻辑区包含N个物理区（横坐标）

![image-20231004035828330](ZNS.assets/image-20231004035828330.png)

图5中 由上至下分析

1. PCIe gen3带宽跑满了
2. 应用发出的请求不足，因为请求队列深度只有1。(1,2对比可以体现出QD的差异)
3. 每个物理芯片80MB/s的读取和40MB/s的带宽，需要更多的物理区域(大约40~80)来充分利用通道或PCIe带宽（这部分做的很迷惑？）

**Challenge #2: Device-agnostic Placement**

理想的分配过程应该向应用充分利用ZNS SSD的所有内部I/O并行性。现有分配机制完全不考虑应用程序先前的分配历史，以及应用之间的交互关系，这会导致不平衡的区域放置，损害I/O并行性，并危及性能。

两种类型的低效放置：

- Channel-overlapped placement
- Die-overlapped placement

Observation：

在不知道设备内部规格的情况下推断区域的物理位置很困难的，我们需要建立一个设备抽象层

(1)依赖于设备的一般分配模型;
(2)维护底层物理设备的阴影视图;
(3)分析其在不同物理通道和模具上的放置平衡水平

#### 3.5 I/O Execution under ZNS SSDs

/* 当读取拥塞时，观察到die/channel争用下的延迟峰值。这是因为 ZNS SSD 没有任何物理资源分区。在namespace内或namespace之间，干扰都会比传统固态硬盘更严重。（感觉ZNS分配更混乱？因为跨物理区的分配？）*/

与物理配置的SSD作对比，128 Zone 16KB stripe size, 70% filled：（可以看到传统SSD因为垃圾回收损失之大）

![image-20230816064000631](ZNS.assets/image-20230816064000631.png)

**Challenge #3: Tenant-agnostic Scheduling**

无论部署的工作负载如何，现有的ZNS ssd分区接口对域间情况提供的性能隔离和公平性保证很少。
人们不能忽视在一个die上的读干扰，因为

(1)任意数量的区域可以在die上碰撞，

(2)单个die的带宽很差，因此即使在设备上非常低的负载下，干扰也会变得严重，

(3)它会导致严重的线路阻塞问题并降低逻辑区域的性能。

Observation:

在多租户场景中使用ZNS ssd时，首先应该了解不同的命名空间和逻辑区域如何共享底层设备的通道和NAND die，将它们的关系划分为竞争和合作类型，并在区域间场景中采用拥塞避免方案以实现公平性。
由于没有设备簿记操作，因此I/O延迟表示碰撞死亡上的拥塞级别。
此外，写缓存拥塞需要全局解决。因此，一个可能的解决方案：

(1)一个全局中心仲裁器，决定所有活动区域之间的带宽共享;
(2)基于拥塞级别编排读I/O提交的perzone I/O调度器。



总结一下，三个挑战：

1. 条带化参数配置与应用无关
2. 区域放置与硬件无关
3. 调度与租户无关

## 4  eZNS

#### 4.1 Overview

eZNS停留在NVMe驱动程序之上，并提供原始块访问。

实现一个新的弹性的分区接口v-zone以解决上述问题 

![image-20231004061709847](ZNS.assets/image-20231004061709847.png)

**区域仲裁器：**

(1)在硬件抽象层(HAL)中维护设备影子视图，并为区域分配和IO调度提供基础;

(2)执行序列化的区域分配，避免重叠放置; (就是把每个stripe unit分摊到不同的die上)

(3)通过收获机制动态缩放区域硬件资源和I/O配置。

**I/O调度器：**

一种延迟调度机制

一种基于令牌的准入机制

#### 4.2 HAL

约束条件：

- 物理区域由同一个die上的多个可擦除块组成
- ZNS在die上均匀地分配物理区（规定活动区数必须是die总数的倍数等）
- 分配机制遵循磨损均衡需要。连续分配区域不会在一个die上重叠，直至已经遍历所有die（最后一个contract不那么绝对）

eZNS维护一个影子设备视图（我们的机制不需要认识到SSD NAND芯片和通道的二维几何物理视图，也不需要维护精确的区域-芯片映射），暴露区域分配和I/O调度的近似数据位置。
我们的机制只依赖于来自设备规格的三个硬件参数：

**MAR** ，maximum active resources 通常与die数成正比，通过离线校准实验测试得到

**NAND page size** （ for striping ）不成文的标准，例如TLC一般用16KB。stripe size选用page size的倍数。

**physical zone size** 用以构造条带组和逻辑分区

#### 4.3 连续区域分配器

eZNS开发了一个简单的区域分配器，尽可能减少die冲突，具体地：

分配器把每个逻辑区请求缓存进一个队列。由于open命令完成时不能保证物理die已经分配完成，因此在区域打开期间，实现了一个保留机制：刷新一个数据块，强制将一个die绑定到该区域。这样能让写操作立即完成（即使高负载情况下，设备的写缓存也会接收一个块）。

为了加快这个过程， 主动地维护一定数量的块用作保留区。分配完成后，更新分配记录，写入元数据块。

以上的最终目的是避免打开多个逻辑区域时的交错分配，减轻重叠。

#### 4.4 Zone Ballooning

v-zone：一种特殊的逻辑分区，能自动扩展资源，以轻量级的方式匹配不断变化的应用程序需求。

![image-20230816193101212](ZNS.assets/image-20230816193101212.png)

与静态逻辑zone类似，v-zone包含固定数量的物理zone。但与静态逻辑分区不同，它将物理区域划分为一个或多个条带组。当第一次打开v-zone或到达上一个条带组的终点时，它会分配一个新的条带组。当写指针到达前一个分条组的末端时，前一个分条组中的所有物理分区都必须完成。（以stripe group为管理单元）

分条组中物理分区的个数在分配时根据“local overdrive“机制确定，实现分区的灵活分条。

v-zone可以：

1. 在其他命名空间处于低活动资源使用状态时，通过从其他命名空间租用备用空间来扩展其条带宽度;
2. 当它完成I/O、通过写到分条组末尾或显式终止时，返回它们

**初始化：**

具体地，所有可用物理空间被划分为两类：基本分区（$N_{essential}$）、备用分区（$N_{spare}$）。基本分区包含能最大化写入带宽的激活物理分区。

均匀分配：例如，假设ZNS SSD现有$N$个namespace，那它只能独占并激活$N_{essential}/（N*MAR）$个物理区。

**Local Overdrive**：

eZNS 使用“Local Overdrive”操作通过从其命名空间的备用组重新分配备用磁盘空间来增强其写入 I/O 能力。 

该机制估算命名空间内的资源使用情况，检查剩余的备用磁盘，并根据写入活动和打开的 v-zone 数量调整分配给每个 v-zone 的备用磁盘数量。

**Global Overdrive**：

它是根据整个SSD的写入强度触发的。根据非活动命名空间的分配历史进行识别，让备用空间在活动命名空间之间分配。

当备用空间要被原namespace使用时，有一个回召机制。

总结，通过仲裁器和Overdrive操作提高了驱动器的整体性能和效率。

#### 4.5 I/O调度

**Goal：**

旨在在 v -zone 之间提供平等的读/写带宽份额，最大限度地提高设备利用率并缓解队头阻塞。

写：采用基于延迟测量的拥塞控制机制：ezNS 中具有缓存感知能力的写入准入控制，监控写入延迟来调整拥塞窗口大小（1-4 stripe width）

读：并使用基于令牌的准入控制方案来调节写入。它定期生成令牌并允许分批写入 I/O 。

-  eZNS 中的读取调度器和写入准入控制几乎不需要协调，并且使用延迟作为信号来推断带宽容量。
- 当在物理芯片上混合读写I/O时，总聚带宽可能会因NAND干扰而下降，但eZNS可以在没有显著协调的情况下处理这个问题。(?) 
- 用户 I/O 中同一物理区域的条带会合并并作为一个写入 I/O 批量提交，因此较小的条带大小不会降低写入带宽。



### 测试

**Default v-zone Configuration**

4 Namespaces (Each namespace has 64 Active zones)

Each Namespace

- Essential resources :32 (128 / 4) 
- Spare resources :32 (64 - 32)
- Maximum active v-zones :16
- Minimum stripe width : 2 with 32KB stripe size (32 / 16)
- Physical Zones in Logical Zone :16

结合之前的实际硬件参数：

![image-20231004074250020](ZNS.assets/image-20231004074250020.png)



证明 Local Overdrive是有效的

![image-20231004074852711](ZNS.assets/image-20231004074852711.png)

![image-20231004074816719](ZNS.assets/image-20231004074816719.png)



Global Overdrive

NS1 NS2 NS3 两写入， NS4 八写入任务。NS1、NS2 和 NS3 在 t=30 秒时停止写入，并在 t=80 秒时恢复写入活动。当其他三个区域闲置时，来自 NS4 的 v 区域使用全局超速原语从其他命名空间获取多达 3 倍的备用区域，并最大限度地利用其写入带宽（2.3GB/s）。然后，当其他区域再次开始发出写入指令时，它可以迅速释放收获的区域。

![image-20231004075129734](ZNS.assets/image-20231004075129734.png)



A B都是覆写, CD同时执行随机读。

在RocksDB上，eZNS 相较于 static zoned interface 提升了 17.7% 的吞吐量和 80.3% 的尾时延。

![img](ZNS.assets/v2-25511ef9edebdbccdb9edc4b906a31de_1440w.webp)

## 总结

具体而言，ZNS SSD接口的**静态**和**不灵活**体现在三个方面：

**1. Zone Striping：**不同workloads在不同的stripe size和stripe width设置下表现不同

**2. Zone Allocation：**一个logical zone中physical zones越多，性能越好；zone放置时的channel overlap和die overlap都会影响并行度。现有zone放置机制没有考虑这些特性。

**3. Zone Interference：**ZNS内部执行I/O请求、其他用户执行的I/O请求都会互相影响。现有机制任务间隔离性差。

它有两个组件：

- **Zone 仲裁者（Arbiter）**：维护 device shadow view，执行 zone 分配以避免 overlap （解决问题2），通过 zone ballooning 执行动态资源分配 （解决问题1）
- **Zone I/O调度器**：使用**局部拥塞控制机制 (congestion control)** 来调度读请求；使用**全局权限控制机制 (admission control)** 来调度写请求（解决问题3）





> ZenFS——RocksDB on ZNS device
>
> https://zhuanlan.zhihu.com/p/555476626

一个韩国人讲eZNS

https://www.youtube.com/watch?v=q10_ExFD8RA





# ZNSwap

ZNSwap: un-Block your Swap

https://www.usenix.org/system/files/atc22-bergman.pdf

主机端OS内实现垃圾回收机制

## 1 Intro

固态硬盘上的交换不再被视为最后的内存溢出机制，而是有效回收内存和提高系统效率的关键系统组件。但固态硬盘未被作为交换设备广泛应用，其中一个关键限制是：

随着固态硬盘使用率的增加，系统性能会下降，如图。

<img src="ZNS.assets/image-20231114102732571.png" alt="image-20231114102732571" style="zoom:67%;" />

这些性能异常现象没有简单的解决方案——它们源于块接口抽象与闪存介质的内在不匹配。

---

ZNSwap为SSD空间回收提供了一种新颖的、空间高效的主机端机制，我们称之为ZNS Garbage Collector(ZNGC)

与传统固态硬盘的设备侧 GC 不同，ZNGC 与操作系统紧密集成，可直接访问操作系统的数据结构，并利用这些数据结构优化其运行。

然而，问题：空间回收过程自然涉及到设备上逻辑块的迁移，而未与拥有数据的应用程序协调块位置的变化。

这在 SSD 端做 GC 时不是问题，因为用户可见的LBA（逻辑块地址）保持不变。但把设备侧的方案应用于主机侧 ZNGC 会带来不可接受的空间开销，因为在 TB 级设备中，每个 4KiB 块都需要维护反向映射...

>关于上述这个问题：映射表不可以放到主存中吗？ 1TB 级SSD设备也不会把整张页表都存储在DRAM中，因为根本没有这么大的板载DRAM（1 TB Flash needs 1GB DRAM）并且使用很大的DRAM空间是要考虑断电时的落盘速度的 ；（存疑）SSD应该是只加载一小部分映射表到DRAM，其余存在Flash中，类似CPU-主存中的TLB。

ZNSwap 通过将反向映射信息存储到逻辑块元数据中，与被交换的页面内容一起写入，从而避免了主机的这些开销。确保映射在页面生命周期内正确无误。

---

具体地，带来了如下好处：

- 细粒度的空间管理：ZNSwap 可省去 TRIM 命令，实现更高的性能和更好的空间利用率。
- 动态的ZNGC优化：ZNSwap 可动态调整同时存储在交换设备中的交换入页的数量，从而提高多读和读写混合工作负载的性能。操作系统会在交换设备中保存一份未修改的已交换内存页副本以避免这些页面的交换惩罚。此类页面可能占用的磁盘空间由操作系统设置静态上限（Linux 为 50%，不可配置）。然而，这一静态阈值并不适合所有工作负载：较低的阈值会降低以读取为主的工作负载的性能，而较高的阈值则会影响读写混合型工作负载（第 3.1.2 节）。ZNSwap 可监控 WAF，并在必要时通过回收交换页面的 SSD 空间来降低存储占用率。
- 灵活的数据放置和空间回收策略：ZNSwap 允许轻松定制磁盘空间管理策略，使 GC 逻辑符合特定系统的交换要求。例如，策略可以强制将生命周期相近的数据集中到同一区域，这在以前的文献[28, 34, 44, 56]中被证明是有用的；也可以通过专用于处理来自特定租户的交换的单独区域来实现更好的性能隔离。
- 准确的多租户计费：当ZNGC在主机上运行时，zswswap与cgroup计费机制集成，显式地将GC开销归因于不同的租户，从而提高了它们之间的性能隔离。

>TRIM：粗糙地理解一下TRIM指令，操作系统使用TRIMs提示块SSD来释放特定的LBAs，从而减少SSD端GC的负载。在OS执行Swap时，大多禁止使用TRIM，开销比较大

综上所述，主要贡献如下:

- 深入分析传统块ssd用作交换设备时的缺点。
- 一种新机制，通过利用逻辑块元数据进行有效的反向映射，使ZNS ssd能够用于交换，而无需在主机中使用资源昂贵的重定向机制。
- 自定义交换感知SSD存储管理策略，减少WA，提高性能，并在多租户环境中实现更好的隔离。
- 在标准基准测试和实际应用中进行了广泛的评估，证明了zsswap的性能提升，例如，与传统的块SSD交换相比，znswap的99百分位延迟降低了10倍，memcached的吞吐量提高了5倍，WAF降低了2.5倍。

## 2 背景 & 3 动机

**OS swap**

OS swap的初衷——当系统遇到内存压力时，它选择内存页，将其驱逐到交换设备(操作系统从页表中解映射选择要驱逐的页，并交换出该页，将其写入交换设备。)

swap-slots：Linux将交换设备上的空间划分为内存大小的块，称为交换槽。操作系统为每个被换出的页面分配一个新的插槽。

**Block SSD空间管理**

（FTL）维护的是LBA到物理地址的映射。例子：想要更新一个块，找一个新块直接写；改映射表；将原位置上的旧数据标为失效。这样的失效块需要垃圾回收，一方面需要空间上over-provisioning (OP)，另一方面设备端进行的GC会与用户I/O竞争带宽。

> WAF：外部的要写入的数据/ 在CG下的实际写入。OP越小，WAF越高。

**Zoned Namespace SSD(ZNS)**

新兴的“存储接口”，逻辑上的组织方式（每个区域大小在物理上与SSD的擦除块大小对齐），在一个Zone内必须顺序写（write、append，对于append，SSD在完成后才会返回具体写入的位置，这允许对一个Zone同时进行多个写请求）。Zone状态：Empty，Open，Full。要重写Zone，需要显示的清除，转换为Empty状态。

### 3 动机

"Flash的激增《复活》了swap的使用"

Swap不再仅仅是应对内存压力的手段，Swap在适度负载时可以充当内存扩展。（例如，优化文件支持和匿名内存页面之间的内存平衡。）但现有的工作更关注OS内的逻辑，本文将结合交换逻辑与SSD的行为对Linux Swap的性能进行深入分析。

#### 3.1  SSD Swap中的异常

- GC不能感知已释放的交换槽
- 交换缓存不能感知GC
- GC不了解页面访问模式
- GC不了解OS的性能隔离

再次观察图1，这种下降是意料之中的，因为GC开销与主动更新的数据量成比例增长。
然而，当设备几乎为空（仅占其容量的10%）时，不应出现下降。

<img src="ZNS.assets/image-20231114102732571.png" alt="image-20231114102732571" style="zoom:67%;" />

根本原因是设备侧GC没有意识到操作系统丢弃了一些交换出的页面，并没有使其对应的交换插槽无效，操作系统默认情况下不会通知SSD。因此，交换设备的实际占用率远高于操作系统可见的占用率，从而导致更高的GC开销。

为了解决上述问题，大多数SSD都支持了**TRIM**命令。

然而在实践中，流行的Linux发行版（例如Debian、Ubuntu）禁止使用TRIM命令进行交换。原因包括TRIM调度开销、TRIM命令的长延迟以及支持异步TRIM的复杂性。作者简单测试了当显式启用交换的TRIM时的情况（略），Linux优化后的TRIM命令与不启用TRIM效果一致

总之：TRIM开了不如不开。（swapon手册中也是这样注释的）

>在Linux系统中，交换槽（swap slot）是指用于存储交换空间（swap space）中的数据的固定大小的块。

#### 3.2 在ZNS上做Swap的可能

ZNS ssd提供了对物理数据放置的更好控制，从而支持应用程序逻辑和设备管理之间更紧密的耦合，并且已经被证明可以为生产Key-Value-Stores提供新的优化机会。这些结果激发了一种新的GC-swap子系统协同设计，它可以利用这种耦合来缓解上述传统ssd的性能问题。

。。。

## 4 Design

ZNS解决了3个关键的设计目标

**主机端垃圾回收**

在ZNS中回收空间需要一个主机端进程：把碎片化的有效内容合并成一个新区，擦除被释放的旧区域。

主要挑战是最小化开销，因为与设备端GC不同，主机端GC直接与常规应用程序争用主机资源。

从本质上讲，我们需要以最小的成本将GC从设备上加载到CPU上，从而使其与Swap的集成更加紧密。



因为有上述限制，直接移植已有的GC实现不可行，（例如FTL中GC的实现需要维护千分之一大小的映射表）

但是ZNGC不需要维护额外的间接层：

znGC通过将内核的反向映射元数据与交换出的页面一起存储在SSD中，避免了额外的间接层。这意味着在进行垃圾回收时，不需要查找额外的数据结构或表来获取页面的映射信息。相反，这些映射信息直接附加在交换出的页面本身上。

**ZNGC-OS集成**

相对于设备端垃圾回收，集成后通过OS暴露的信息可以优化Swap的性能

例如：ZNGC可以识别操作系统无效的交换槽（swap slot），并避免不必要的复制，而无需使用其他方式。

**数据放置策略**

策略取决于执行环境，提供了几种策略

### 4.1 总览

![image-20231115015514214](ZNS.assets/image-20231115015514214.png)



### 4.2 znGC

znGC集成在kernel virtual memory (VM)中。作为守护进程，当空zone数较低时触发。（或通过zswap策略的明确请求）

相对于块ssd，被ZNGC移动的页面讲被分配一个新的主机可见地址。如果没有额外的转换层，ZNGC必须更新保存原始页面交换槽的页表，以反映新的位置。

为此，ZNGC将相关的反向映射元数据与数据一起存储在ZNS SSD的per-LBA中，以帮助以后更新页表。



哪些信息需要存储在页面元数据中以保证反向映射在其生命周期内保持正确?

——Linux中已实现的反向映射方案

![image-20231115024036963](ZNS.assets/image-20231115024036963.png)





### 4.3 ZNGC-swap一体化

a）物理zone（空间）信息：每个空间与swap-slots的映射相关联，映射存储了每个swap-slot的状态。这样ZNGC和OS就可以立马知道swap-slot的状态转变，不需要TRIM和截断阈值来管理交换缓存。

b）交换空间抽象：可以被用来swap-slot分配的活跃空间通过交换空间抽象进行暴露，从而避免管理物理空间的复杂性。

c）ZNSwap策略：提供一系列接口使得可以定制化空间分配策略和回收策略。

d）接口：本文定义了三个标准api，单核策略、冷热策略和进程策略，分别是对每个核的数据、冷热数据和进程数据进行性能隔离。



## 评估

Ubuntu 20.04  Linux Kernel 5.12 

512G DDR4 

1T 西数ZN540 + 1T SSD

交换空间大小 = 系统内存大小 ，其他剩余的空间填充数据。

**Facebook memcached-ETC**
其中 90% 的请求在 10% 的key上。

![image-20231122174711316](ZNS.assets/image-20231122174711316.png)













# 备注

### Linux Swap

1. 交换页面：当需要将数据页写入Swap空间时，Linux会将这些页面标记为“交换出”。数据页的内容将被写入Swap分区或Swap文件中，以释放内存供其他进程使用。
2. 程序恢复：如果系统需要访问已经被交换出的页面，Linux会将这些页面重新读取到内存中。这将导致其他数据页被交换出，以便为需要的页面腾出空间。
3. Swap空间的管理：Linux会定期检查Swap空间的使用情况，并根据需要进行Swap页面的调度和重新分配。这包括根据页面的活跃性和访问模式来决定哪些页面应该被换入或换出。

### Swap Cache

- Swap Cache是指交换分区中的缓存区域，类似于文件系统中的page cache。
- Swap Cache用于存储匿名页（即没有文件背景的页面）的内容，这些页面在即将被swap-out时会被放进swap cache，但通常只存在很短暂的时间，因为swap-out的目的是为了腾出空闲内存。
- 曾经被swap-out现在又被swap-in的匿名页也会存在于swap cache中，直到页面中的内容发生变化或者原来使用过的交换区空间被回收。

Swap Cache（交换缓存）是Linux操作系统中的一种缓存机制，用于提高对Swap分区的读取性能。它是在内核中实现的一种缓存层，用于存储最近从Swap分区中读取的数据页，以便在需要时可以更快地访问这些页面。

当Linux系统需要将数据页从Swap分区中读取回内存时，数据页会首先被放置到Swap Cache中。这样，如果后续的访问请求需要读取相同的数据页，内核可以直接从Swap Cache中获取数据，而无需再次访问慢速的Swap分区。



## 评估

![image-20231115032938106](ZNS.assets/image-20231115032938106.png)







### 反向映射

匿名页反向映射是Linux内核中的一种机制，用于解除物理页与进程虚拟地址空间之间的映射关系。这个机制主要分为匿名页映射和文件页映射两种类型。下面将详细介绍匿名页反向映射的过程和anon_vma结构的作用。

1. 匿名页反向映射过程：
   - 当内核需要回收一个物理页时，需要先解除该物理页与进程虚拟地址空间的映射关系。
   - 反向映射机制通过查找物理页的映射关系，找到所有映射到该物理页的进程虚拟地址空间。
   - 反向映射过程主要涉及三个关键的数据结构：struct vm_area_struct (VMA)、struct anon_vma (AV)和struct anon_vma_chain (AVC)。
   - VMA用于描述进程的虚拟地址空间，其中的anon_vma_chain成员用于链接VMA和AV。
   - AV用于管理匿名页面映射的所有VMA，物理页的struct page中的mapping成员指向该结构体。
   - AVC是一个链接VMA和AV的桥梁，每个AVC都有一组对应的VMA和AV。AV会将与其关联的所有AVC存储在一个红黑树中。
2. anon_vma结构的作用：
   - anon_vma结构用于管理匿名页面对应的所有VMA。
   - 它可以通过物理页的mapping成员找到与之关联的AV。
   - AV中的rb_root红黑树存储了与该AV关联的所有AVC，通过遍历红黑树可以找到所有映射到该物理页的VMA。

通过匿名页反向映射机制，内核可以有效地解除物理页与进程虚拟地址空间之间的映射关系，并且可以快速找到所有映射到该物理页的VMA。这对于内核的内存管理非常重要。















# 模拟器

### QEMU 

西交实验：https://github.com/MiracleHYH/CS_Exp_ZNS

https://miracle24.site/other/cs-exp-zns-1/

### FEMU(tong)

 https://www.usenix.org/system/files/conference/fast18/fast18-li.pdf

FEMU配置与源码浅析https://blog.xiocs.com/archives/46/

与原生的 Qemu-nvme 相比，Femu 的扩展主要集中在延迟仿真上。

### ConfZNS

https://github.com/DKU-StarLab/ConfZNS ，CCF C

### NVMeVirt

NVMeVirt: A Versatile Software-defined Virtual NVMe Device，FAST 23

ZenFS + RocksDB + nvmevirt 配置ZNS模拟环境:

https://www.notion.so/znsssd/NVMEvirt-NVMEvirt-RockDB-Zenfs-7292a6396ed84fc29010a8d0ed768d9b?pvs=25



上交毕设：实现*ZNS* *SSD*模拟器，然后基于模拟器设计适配的LSM Tree https://github.com/adiamoe/LSM-based-on-ZNS-SSD



# 其他相关项目

### [Dantali0n/OpenCSD](https://github.com/Dantali0n/OpenCSD)

OpenCSD: eBPF Computational Storage Device (CSD) for Zoned Namespace (*ZNS*) *SSDs* in QEMU

### SZD

[SimpleZNSDevice](https://github.com/Krien/SimpleZNSDevice)

基于SPDK做的的ZNS的封装，可以让用户不费吹灰之力就能开发 ZNS 设备。

### **[bpf-f2fs-zonetrace](https://github.com/pingxiang-chen/bpf-f2fs-zonetrace)**

基于eBPF的Zone可视化工具

ZoneTrace是一个基于eBPF的程序，可以在ZNS SSD上的F2FS上实时可视化每个区域的空间管理，而无需任何内核修改。我们相信ZoneTrace可以帮助用户轻松分析F2FS，并开辟几个关于ZNS SSD的有趣研究课题。

### F2FS

(Flash-Friendly File System，三星)

原文，https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf

非官方仓库，https://github.com/unleashed/f2fs-backports

### ZenFS

ZNS文件系统，for RocksDB，西数。 https://github.com/westerndigitalcorporation/zenfs

### zonefs-tools

一个极简的ZNS文件系统，西数。https://github.com/westerndigitalcorporation/zonefs-tools

### OS接口文档

https://zonedstorage.io/docs/introduction

# 设备

znskv中使用的盘

![image-20231208114504674](./ZNS.assets/image-20231208114504674.png)

### 硬件接口

![img](ZNS.assets/v2-1057134427f228d44445ae84730da650_1440w.webp)





U.2 (SFF-8639)https://zhuanlan.zhihu.com/p/568688937?utm_id=0

![img](ZNS.assets/v2-6a9818b238f03d0864210ab4fc8ddc6b_1440w.webp)

### 设备安装记录

https://www.notion.so/znsssd/Disk-2b750be455a2459bb346556567b2553a





# 其他问题

>现在没有了逻辑块地址-虚拟块地址的转换，数据在盘中的真实地址暴露给应用，是否可以（更好地利用空间局部性）使得prefetch的效果更好？

常见的磁盘预取器和开源存储引擎中使用的磁盘预取算法

磁盘预取是一种优化技术，通过提前将数据从磁盘读取到内存中，以减少磁盘I/O操作的等待时间。常见的磁盘预取器和开源存储引擎中使用的磁盘预取算法如下：

1. Linux Page Cache预读：Linux操作系统中的Page Cache是一种内存缓存机制，它可以将磁盘上的数据预先加载到内存中，以提高读取性能。Linux Page Cache预读算法会根据文件的访问模式和访问模式的历史记录来预测下一次可能访问的数据，并提前将这些数据加载到内存中[[2\]](https://xiazemin.github.io/linux/2020/04/01/pagecache.html)。
2. MySQL InnoDB存储引擎的磁盘预取算法：MySQL InnoDB存储引擎使用了一种称为"DoubleWrite Buffer"的技术来提高磁盘写入性能。在写入数据到磁盘之前，InnoDB会将数据先写入到一个内存缓冲区中，然后再将数据从缓冲区写入到磁盘。这种方式可以减少磁盘的随机写入操作，提高写入性能[[2\]](https://xiazemin.github.io/linux/2020/04/01/pagecache.html)。
3. RocksDB存储引擎的磁盘预取算法：RocksDB是一个开源的键值存储引擎，它使用了一种称为"Block-based Table"的存储结构。在读取数据时，RocksDB会根据数据的访问模式和历史记录来预测下一次可能访问的数据块，并提前将这些数据块加载到内存中。这种方式可以减少磁盘的随机读取操作，提高读取性能[[2\]](https://xiazemin.github.io/linux/2020/04/01/pagecache.html)。





>两步编程（Two-step programming）是一种在NAND闪存芯片中使用的编程方法。

这种方法特别设计用于提高数据的写入准确性和闪存芯片的寿命。在传统的闪存编程中，数据以一次性方式写入存储单元，但在两步编程中，这个过程被分成两个阶段：

1. **第一步**：在第一步中，数据被部分地写入存储单元。这通常包括将存储单元设置到一个中间的阈值电平。
2. **第二步**：在第二步中，数据被进一步细化或“调整”到其最终值。这个过程涉及更精细地控制电荷的注入，以确保数据被准确地写入。

两步编程的好处包括：

- **提高精度**：通过这种分阶段方法，可以更精确地控制电荷的流动，减少写入错误。
- **延长寿命**：减少了对闪存单元的应力，从而延长了其使用寿命。

这种技术在多层单元（MLC）和三层单元（TLC）NAND闪存中尤其重要，因为这些类型的闪存在存储多比特信息时需要更高的精确度。不过，两步编程也可能导致写入过程比一步编程更慢，因为需要额外的时间来细化数据的存储。
