7.31

nas-conf.org

![image-20240524154533433](C:\Users\26557\AppData\Roaming\Typora\typora-user-images\image-20240524154533433.png)

 

 

 

![image-20240524154533433](C:\Users\26557\AppData\Roaming\Typora\typora-user-images\image-20240524154533433.png)

 

 **题目待定**

**Abstract**

Zoned Namespace (ZNS) solid-state drives (SSDs) employ zone-based management and enforce sequential writes within zones, effectively addressing issues like write amplification and excessive garbage collection overhead found in traditional SSDs. Compared to conventional SSDs, ZNS SSDs offer higher throughput, lower and more stable latency, and longer lifespan. However, existing studies often rely on simulators, potentially leading to conclusions that diverge from real-world performance. Additionally, current adaptation efforts have not fully utilized ZNS capabilities.

This paper proposes an Append-Aware Write-Ahead Log (A2-WAL) mechanism and implements the Zone-Append File System (ZAFS) based on the Storage Performance Development Kit (SPDK) for ZNS SSDs. By leveraging SPDK technology and asynchronous write mechanisms, this solution effectively addresses performance bottlenecks in RocksDB caused by Write-Ahead Log (WAL) serial writes under high-write scenarios.

Experimental results based on ZNS SSD hardware testing are used to discuss design principles, parameter selection, and evaluate the effectiveness of ZAFS. Compared to ZenFS, ZAFS improves throughput by 1.9 to 3.5 times. Furthermore, while enhancements increase WAL file size, data recovery time during disaster recovery can be reduced by up to 6.7 times.

Keywords: Zoned Namespace SSD; Log-Structured Merge-Tree; Write-Ahead Log; Key-Value Storage; File System

 

**Keywords**: Zoned Namespace SSD; Log-Structured Merge-Tree; Write-Ahead Log; Key-Value Storage; File System

------



# Introduction



# Background

### KV Store

键值存储（Key-Value Store）是存储领域的一种非常重要存储模型，在这种存储模型中，数据被简单地组织为键值对（Key-Value Pairs），其中键（Key）是唯一的，用于标识和检索对应的值（Value），值是变长的复杂数据。这种直接映射的方式，使得键值存储在处理大量数据时能够提供快速的数据访问和高效的存储管理。

键值存储的简单性和普适性是其最显著的优势。由于键值对的直接映射关系，键值存储的接口通常非常简单，易于编程和使用。键值对的结构允许存储各种类型的数据，包括但不限于字符串、数字、对象等。利用键值存储结构构建基本的存储引擎，在其上可以开发各种类型的数据库，再供不同场景下的应用使用，这样避免了重复构建基础组件，只需维护一个高效的底层键值存储引擎即可。上述特性使得键值存储可以广泛应用于不同的应用场景，如缓存系统、会话管理、配置存储以及分布式系统等。

具体地，键值存储的概念可以基于内存或磁盘进行不同的实现。内存数据库如Redis，利用高速内存和基于键值的底层设计提供了极其高效的数据访问速度，成为许多实时应用的首选存储解决方案。而磁盘数据库如LevelDB，则通过优化磁盘操作，实现了高效的数据存储和访问。此外，如Cassandra[22]和Riak等等数据库，都基于键值设计实现了高可扩展性，高可靠性高容错性的存储系统。

键值存储涉及的研究领域非常广泛，包括性能优化、数据一致性、容错机制、数据压缩和安全性等多个方面。在性能优化方面，研究者致力于通过各种技术手段，如内存优化、索引结构优化等，提升键值存储的读写性能；数据一致性是分布式系统中的关键，优秀的一致性模型能确保在分布式环境中数据的一致性和高可靠性。容错机制的研究则关注如何在节点故障的情况下，保证系统的稳定运行。数据压缩技术的研究旨在减少存储空间的需求，利用计算开销换取高存储效率。安全性研究则关注如何保护存储在键值存储中的数据，防止未授权访问和数据泄露。

Key-Value Store (KVS) is a fundamental storage model in the storage domain, where data is organized simply as Key-Value Pairs, with each Key being unique and used to identify and retrieve the corresponding Value, which can be variable-length complex data. This direct mapping enables Key-Value Stores to provide fast data access and efficient storage management when dealing with large volumes of data.

The simplicity and versatility of Key-Value Stores are its most prominent advantages. Due to the direct mapping of key-value pairs, the interface of Key-Value Stores is typically straightforward, making it easy to program and use. The structure of key-value pairs allows for the storage of various types of data, including but not limited to strings, numbers, and objects. Building basic storage engines using the Key-Value Store structure allows for the development of various types of databases, which can then be utilized by applications in different scenarios. This approach avoids the duplication of building basic components, requiring only the maintenance of an efficient underlying Key-Value Store engine. These characteristics make Key-Value Stores widely applicable in various scenarios, such as caching systems, session management, configuration storage, and distributed systems.

Specifically, the concept of Key-Value Stores can be implemented based on either memory or disk. In-memory databases like Redis leverage fast memory and key-based underlying designs to provide extremely efficient data access speeds, making them the preferred storage solution for many real-time applications. On the other hand, disk-based databases like LevelDB achieve efficient data storage and access through optimized disk operations. Additionally, databases like Cassandra and Riak, based on key-value designs, have implemented highly scalable, reliable, and fault-tolerant storage systems.

Key-Value Stores involve a wide range of research areas, including performance optimization, data consistency, fault tolerance mechanisms, data compression, and security. In terms of performance optimization, researchers aim to enhance the read and write performance of Key-Value Stores through various techniques such as memory optimization and index structure optimization. Data consistency is crucial in distributed systems, where excellent consistency models ensure data consistency and high reliability in distributed environments. Research on fault tolerance mechanisms focuses on ensuring stable system operation in the event of node failures. Data compression techniques aim to reduce storage space requirements, trading computational overhead for high storage efficiency. Security research focuses on protecting data stored in Key-Value Stores, preventing unauthorized access and data breaches.

### LSM-Tree

LSM-tree（Log-Structured Merge-Tree [21]）模型是一种设计巧妙的数据存储模型，广泛应用于键值型数据存储引擎。LSM-tree模型旨在解决传统数据库在处理写入操作时所面临的性能瓶颈。其设计理念是不进行原地更新，而是通过日志式的追加写入和层次化设计，将随机写转换为高效的顺序写，从而优化整体性能。但代价是读性能差，写放大效应显著，垃圾回收开销高。

具体而言，LSM-tree不是树的一种，也不是某种具体的数据结构。而是一种存储架构设计模型，在LSM-tree模型中，数据在一个或多个树状结构中首先被写入最顶层。最顶层写满后，刷新到下一层（通常是持久化设备），该过程通常伴随着数据排序，以便后续的读取和合并操作。随着数据的累积，当某层中的数据达到一定大小时，会被合并并下压至下一层。合并过程减少了数据数量，删除了过时或重复的数据，释放了空间。合并策略的设计直接影响LSM-tree的性能，包括写入放大因子和读取性能。

尽管LSM-tree模型在提高写入性能方面表现出色，但是仍存在一些问题。例如，写入放大因子可能导致实际写入磁盘的数据量远大于原始数据量，在存储资源受限的环境中可能成为问题。此外，LSM-tree将随机写转换为顺序写，是以牺牲读性能为代价的。随着数据积累，读取性能可能受到影响。为解决这些问题，研究者也提出了多种优化策略和技术，如布隆过滤器、层级合并策略、缓存机制和数据压缩技术。

LSM-tree模型以其在写入密集型应用中的优异性能成为现代数据库系统的关键组成部分，是最常见的存储引擎模型之一。并且随着各大公司对LSM-tree的广泛使用，大大促进了该技术的进步，未来，对LSM-tree模型的研究和优化将继续深入，以满足不断增长的数据存储和管理需求。

在谷歌基于LSM-tree结构推出开源键值存储引擎LevelDB后，LSM-tree名声大噪。对照LSM-Tree的设计与LevelDB的实现，如图2-1所示。

以LSM-tree模型构建的存储引擎还有RocksDB等等。RocksDB是基于LevelDB优化的工程性实现，做了进一步优化，广泛用于各大互联网公司。



The LSM-tree (Log-Structured Merge-Tree [21]) model is a cleverly designed data storage model widely utilized in key-value data storage engines. The LSM-tree model aims to address the performance bottlenecks encountered by traditional databases when handling write operations. Its design philosophy lies in transforming random writes into efficient sequential writes through log-structured appending and hierarchical structuring to optimize overall performance. However, this optimization comes at the cost of reduced read performance, significant write amplification effects, and high garbage collection overhead.

Specifically, LSM-tree is not a specific tree structure but rather a storage architecture design model. In the LSM-tree model, data is initially written to one or multiple tree-like structures at the top level. When the top level is filled, data is flushed to the next level (usually a persistent device), often accompanied by sorting for subsequent read and merge operations. As data accumulates, when the data in a certain level reaches a certain size, it is merged and pushed down to the next level. The merge process helps reduce data volume, remove obsolete or duplicate data, and free up space. The design of merge strategies directly influences the performance of LSM-tree, including write amplification factor and read performance.

Despite the excellent performance of LSM-tree model in improving write performance, there are still some issues. For example, the write amplification factor may lead to the actual data written to disk being much larger than the original data volume, which may become a problem in storage-constrained environments. Furthermore, while LSM-tree converts random writes into sequential writes, it does so at the expense of read performance. As data accumulates, read performance may be affected. To address these issues, researchers have proposed various optimization strategies and techniques, such as Bloom filters, tiered merge policies, caching mechanisms, and data compression technologies.

LSM-tree model has become a key component of modern database systems due to its outstanding performance in write-intensive applications, making it one of the most common storage engine models. With the widespread adoption of LSM-tree by major companies, the advancement of this technology has been greatly accelerated. In the future, research and optimization of the LSM-tree model will continue to deepen to meet the growing demands of data storage and management.

Since Google introduced the open-source key-value storage engine LevelDB based on the LSM-tree structure, LSM-tree has gained significant attention. Comparisons between the design of LSM-tree and the implementation of LevelDB are shown in Figure 2-1.In addition to LevelDB, other storage engines built on the LSM-tree model include RocksDB. RocksDB is an engineering implementation optimized based on LevelDB and widely used by major internet companies.

![img](file:///C:/Users/26557/AppData/Local/Temp/msohtmlclip1/01/clip_image002.gif)

图2-1 LSM-Tree设计及实现的架构图

### Write-Ahead Log

写前日志（Write-Ahead Logging，WAL）是计算机科学中一种用于确保数据库系统原子性和持久性的技术。是指在应用修改之前将所有修改记录在日志中，为崩溃和事务恢复提供机制。现代文件系统通常使用WAL的变体，例如日志记录，用于元数据更新。

而对于LSM-Tree型存储引擎，使用WAL的具体情形如下：在写入易失性的MemTable时，如果发生电源故障，则无法保留数据。为解决这种由于断电等原因造成的数据丢失问题，存储引擎往往会在持久化存储设备中维护一个预写日志（WAL）。首先，将put（写入）请求的记录存储在WAL中，然后将其写入到内存的MemTable中。在需要进行数据恢复的时候，按顺序读取所有WAL数据，依次执行对应操作来恢复内存中的memtable。因为，在LSM-Tree中，只有对键值对的最新更改是有效的，所以WAL中的记录必须按顺序保存。

然而，这种设计可能导致频繁的小文件写入操作，成为性能瓶颈，因此，WAL对于实现高写入吞吐量至关重要。一方面，因为LSM树通常部署在快速且高度并行的NVMe闪存SSD上，使用NVMe时，SSD会发出内部管理操作，这些操作与LSM树竞争存储资源。这种竞争导致吞吐量不稳定。另一方面，在多线程环境中，还会发生锁争用，导致写入延迟。

Write-Ahead Logging (WAL) is a technique in computer science used to ensure the atomicity and durability of database systems. It involves recording all modifications in a log before applying them to the database, providing a mechanism for crash and transaction recovery. Modern file systems typically employ variations of WAL, such as journaling, for metadata updates.

For LSM-Tree-based storage engines, the specific use of WAL is as follows: when writing to the volatile MemTable, data cannot be preserved in the event of a power failure. To address the risk of data loss due to power failure or other reasons, storage engines often maintain a Write-Ahead Log (WAL) in persistent storage. Initially, records of put (write) requests are stored in the WAL before being written to the MemTable in memory. During data recovery, all WAL data is sequentially read, and corresponding operations are executed to restore the MemTable in memory. Because, in LSM-Tree, only the latest changes to key-value pairs are valid, the records in the WAL must be saved in order.

However, this design can lead to frequent small file write operations, becoming a performance bottleneck. Therefore, WAL is crucial for achieving high write throughput. On one hand, since LSM trees are typically deployed on fast and highly parallel NVMe flash SSDs, when using NVMe, the SSD issues internal management operations that compete for storage resources with the LSM tree. This competition results in unstable throughput. On the other hand, in a multi-threaded environment, there may be lock contention, leading to write latency.

**WAL Batch-write**

解决上述问题的一种流行的方法是批量写入，RocksDB中也实现了这一技术，具体如图3-2所示。该过程动态选择多个具有待处理 put 请求的工作线程中的一个领导线程，收集所有剩余的记录，并让领导线程代表其他工作线程一次性写入它们。然而，这种技术并没有改善（甚至加剧了）尾延迟问题。在收集和写入这些记录的过程中，批处理中的所有记录共享写入时间，可能会增加单个写入的等待时间，尤其是当该条记录较大时。

One popular approach to address the mentioned issues is batched writing, which has also been implemented in RocksDB, as illustrated in Figure 3-2. This process dynamically selects one leading thread from multiple worker threads with pending put requests, collects all remaining records, and delegates the leading thread to write them all at once on behalf of other worker threads. However, this technique has not improved (and in some cases exacerbated) the tail latency issue. During the collection and writing of these records, all records in the batch share the same write time, potentially increasing the wait time for individual writes, especially when a particular record is large.

![image-20240524160902725](C:\Users\26557\AppData\Roaming\Typora\typora-user-images\image-20240524160902725.png)

​												图3-2  RocksDB的批量写入时序图

**在ZNS中遇到的问题**

ZNS虽然能改善了LSM树吞吐量，使得延迟更稳定，但它对LSM树的WAL组件等其他组件造成了严重的写入效率挑战。主要原因是ZNS严格禁止随机写，禁止应用程序同时向同一区域发出写入I/O。且WAL往往集中存储在单一区域内，这导致WAL的写入操作是串行化的，仅有一个写入操作同时处理这限制了WAL的吞吐量，进而影响了整个存储引擎的并发写入效率。另一方面，批量写入的解决方案本身带来的长尾延迟效应，削减了ZNS带来的延迟降低效果。因此，ZNS没有展现出应有的性能优势。

While ZNS improves the throughput of LSM trees, making latency more stable, it poses significant challenges to the write efficiency of LSM tree components such as the WAL. The primary reason is that ZNS strictly prohibits random writes and prohibits applications from issuing simultaneous write I/O to the same zone. Additionally, WAL is often concentrated in a single zone, resulting in serialized WAL write operations where only one write operation is processed at a time. This limitation on WAL throughput affects the overall storage engine's concurrent write efficiency. Furthermore, the long tail latency effect inherent in the batched writing solution itself reduces the latency reduction effect of ZNS. As a result, ZNS has not demonstrated the expected performance advantage.



### Zone Append

The addition of the zone append command to the ZNS SSD specifications offers a significant advantage. Unlike the conventional NVMe interface, which lacks guaranteed write ordering among requests in the submission queue and may not process them in the pre-specified LBA order, the append command addresses this challenge. Serialization of writes is typically achieved by limiting the queue depth to one, which adversely affects write throughput. However, the append command introduces an efficient solution by allowing an increase in queue depth while preserving the write order. Unlike the conventional write command, the append command specifies the data and a designated zone (instead of a specific LBA), storing it in the zone and returning the start location of the appended data to the host via a field called Assigned LBA (ALBA) . Since the exact LBA location is determined by the device, efficient synchronization is achieved within the ZNS SSD even with increased queue depth, eliminating restrictions on the host-side queue depth. This enhancement significantly boosts write throughput, mitigates scalability issues, and consequently improves tail latency.

**write VS append ?**





# Design of  ？FS





# 







# 绪论

本章我们首先分析传统固态硬盘设计上存在的局限和发展中遇到的瓶颈，然后介绍新兴的固态硬盘技术及其国内外研究发展现状，并深入分析其优势和存在的风险与挑战，最后对本文的主要研究内容及工作意义作了具体说明。

##  课题背景、目的与意义

随着数据中心对存储性能与效率的需求日益增长，传统的存储解决方案已经无法满足这些日益增长的需求。这种背景下，Zoned Namespace (ZNS) SSD作为一种新兴的存储技术，因其独特的数据管理方式和对存储效率的显著提升而受到学术界和工业界的广泛关注。ZNS SSD通过引入分区的概念来优化数据的写入过程，从而减少写入放大效应，提高存储设备的寿命和性能。本课题来源于实验室与浪潮等企业联合申请的“面向新型计算模式的分布式存储系统”重点专项，尝试利用ZNS SSD等新兴硬件重新设计存储系统。本课题作为此专项的先行性研究，准备基于多块实际的ZNS SSD盘做ZNS SSD的数据访问特征以及性能优化方面的研究。

### 研究背景与趋势

传统固态硬盘设计上存在的局限性，例如，闪存转换层和垃圾回收机制带来的写放大问题，因此兴起了一系列在软件层面对固态硬盘进行优化的研究工作，然而，这些技术并不能彻底解决固态硬盘内部硬件设计上的问题，因此，研究向底层深入，关注与硬件上进行改良和创新，旨在从根本上解决这些问题。

####  基于传统SSD的写放大优化研究

写放大（Write Amplification，WA）是评价SSD性能的关键指标之一，它直接影响了SSD的寿命和性能。传统SSD由于”黑盒”式的内部数据管理机制，很难有效利用主机端的数据热度信息进行优化。目前的研究主要集中在以下几个方面：

（1）文件系统优化：通过优化日志结构文件系统（Log-structured File System，LFS[1]）的数据管理策略，利用追加写的方式减少数据的原地更新，从而降低垃圾回收的频率。例如F2FS[2]、BetrFS[3]等，这些工作的核心点在于分离冷热数据，尽可能将冷热程度相同的数据块放置于同一区域，使其能在相近的时间内失效，从而降低写放大。

（2）SSD内部的数据放置策略优化： 研究如何在SSD内部有效区分冷热数据，将相同热度的数据存放在一起，以减少垃圾回收时的数据迁移，降低写放大。例如Yang 等人[5]提出的一种通过预测数据块温度来放置数据的方案, 其使用K-Means 算法进行聚类，将温度相近的数据分发到相同的NAND 块。ML-DT[6]根据I/O 大小、逻辑地址、历史块寿命等特征生成预测模型，对数据块的未来寿命进行预测，从而实现冷热数据分离。

（3）垃圾回收算法优化：当SSD 内部失效数据占比超过一定的阈值后，控制器会触发垃圾回收操作。现有的垃圾回收算法旨在根据不同的指标，在候选区域中选择最合适的部分进行回收开发更高效的垃圾回收算法，通过优化数据回收顺序和时机，减少写放大。例如Windowed Greedy[7]，Random-Greedy[8]，d-choices[9]等。

然而，上述这些研究工作只能在操作系统、应用级别一定程度地缓解主机侧的工作负载导致的写放大。但在固态硬盘内部仍存在写放大现象，这一方面是由于闪存转换层（Flash Translation Layer, FTL）的管理策略，另一方面是固态硬盘中NAND闪存颗粒的擦写粒度不一致的特性导致的。

FTL作为固态硬盘的核心组件之一，负责在逻辑地址和物理地址之间进行映射，以支持块设备的随机访问特性。然而，FTL的管理策略往往需要在提高性能和减少写放大之间做出权衡。例如，为了提高随机写入的性能，FTL可能采用过度映射（Over-Provisioning）和垃圾回收算法，这两种方法都可能导致额外的数据搬移操作，从而增加写放大。

此外，固态硬盘的擦写特性也是导致写放大的重要因素。由于NAND闪存的擦写操作是以块为单位进行的，而块的大小通常远大于页面（即数据写入的最小单位），这就意味着即使是对单个页面的小范围修改，也可能导致整个块的擦写和重写，进而产生写放大。

#### 新硬件技术

近年来，一系列新型固态硬盘技术兴起，比如，Multi-Stream SSD，Open-Channel SSD (OC SSD)，KV SSD等等。其中最具有潜力的是分区命名空间固态硬盘。

ZNS SSD（NVMe Zoned Namespace SSD）是一种新型的固态硬盘，它采用了分区命名空间（ZNS）接口技术规范。与传统的固态硬盘不同，ZNS SSD 将数据放置和垃圾回收等操作从设备内部转移到主机端，使主机能够更优化地管理数据放置和可预测地处理垃圾回收，同时降低设备的写放大，延长闪存介质的寿命。因此，ZNS SSD 在研究界引起了广泛关注。

具体地，ZNS的设计理念在于通过区域化管理数据，定义区域容量、活动区域限制和区域追加命令等新概念，并向主机暴露更多的存储器内部信息。这些设计直接减少写放大现象，优化了数据管理粒度，从而提高SSD性能和寿命。如今，经过SSD制造商、软件开发者和标准化机构之间的合作努力，ZNS SSD技术已有稳定的硬件标准和基础软件库。

在标准化方面**，**NVMe组织已发布了ZNS的规范，这有助于标准化这些设备的管理和访问方式，促进更广泛的采用和兼容性。在软件生态方面**，**开源社区正在推动将对ZNS SSD的支持集成到操作系统、数据库和存储系统中，以充分利用其优势。社区对ZNS SSD技术的支持不断增强，已开发了多种针对ZNS优化的文件系统和工具，帮助开发者和企业更好地理解和利用该技术。例如，像F2FS[2]等为闪存设计的文件系统已经开始支持ZNS，另外也有专门为数据库存储引擎适配ZNS而设计的文件系统ZenFS[10]，这些工作显示了ZNS技术的实际应用潜力。

综上，ZNS是一种使用Zone语义的新型SSD技术，其优势有：

- 更高的性能：ZNS SSD通过将数据放置和垃圾回收操作交由主机处理，可以实现更优化的数据放置和更可预测的垃圾回收，从而提高性能。
- 更低的写放大：ZNS SSD的数据写入方式与闪存的操作特性相契合，可以降低写放大现象，延长闪存介质的寿命。
- 更低的成本：由于ZNS SSD不需要复杂的设备控制器算法，可以简化硬件设计，降低成本。
- 更高的容量利用率：ZNS SSD使用更大的管理粒度，并且节省了OP（Over-provision）空间，可以更有效地利用存储容量。

目前在ZNS上的研究可以大致分为两类，硬件方面，已有领先的SSD制造商，例如三星和西部数据，开始发布ZNS产品并展开研究，例如ZNS+[11] 、eZNS[12]等；相关应用方面，基于ZNS的应用主要集中在键值存储领域，尤其是基于LSM-tree的键值存储优化：考虑到ZNS SSD和LSM-tree都遵循严格的顺序写约束，其软硬件特征高度重合， 可以将一些应用移植到ZNS SSD上获得更好的性能。典型案例如基于ZenFS[10]的RocksDB[13]



###  面临的问题和挑战

ZNS SSD技术的推广和实施虽然带来了显著的性能优势，但也面临着若干重要的问题和挑战。以下将详细分析这些挑战及其对存储系统设计和实际应用的影响。

首先是技术适应性和兼容性问题，由于ZNS SSD采用了与传统SSD不同的数据管理策略，这要求现有的操作系统和应用软件必须进行相应的调整以充分利用ZNS SSD的性能优势。此外，ZNS SSD的引入可能需要修改现有的文件系统或开发新的存储协议，以支持其区域化的特性。这些问题可能导致在初期实施过程中为使用者带来兼容性成本和技术学习成本。

其次，是管理复杂性增加。尽管ZNS SSD提供了更高效的数据管理方式，但同时也增加了存储管理的复杂性。例如，操作系统或数据库需要智能地将数据分配到不同的区域，并管理每个区域的状态和性能。这就需要更精细的资源调度算法和更高级的系统监控工具，然而，目前适配ZNS的工程实现比较简陋，管理效率较低。

### 课题的目的与意义

本课题旨在深入分析基于Zoned Namespace (ZNS) SSD的数据访问特征，并通过研究针对这些特性的性能优化策略，探索提升基于ZNS SSD的存储系统的性能的有效方法。相较于已有的在QEMU[1]、FEMU[2]等模拟器上的工作，此项工作不仅能够为理解ZNS SSD在不同的真实应用场景下的性能表现提供理论和数据基础，而且通过性能优化实验，能够为数据中心的存储系统设计提供实验参考，从而在实际应用中提升存储系统的效率和可靠性。此外，随着数据中心对存储解决方案效率和性能要求的不断提升，该方向的研究有望降低SSD成本，推动SSD的大规模使用，满足未来数据中心更为复杂和高效的存储需求。

##  国内外研究现状

目前，关于ZNS已经有了一些初步的研究。主要是集中在底层设计，如硬件优化，文件系统优化等，并且有一些在特定应用场景下的适配优化和探索性工作。

在ZNS上的研究可以大致分为三个层级：在硬件方面，已有领先的SSD制造商，例如三星和西部数据，开始发布ZNS产品并展开研究，例如ZNS+、eZNS[12]等；在系统方面，已经有支持ZNS的文件系统如：F2FS，ZoneFS等， 也有一些基于Linux系统的创新性工作，如利用将ZNS盘用作交换分区。在相关应用方面，现有的基于ZNS的应用主要集中在键值存储领域，尤其是基于LSM-tree的键值存储优化，考虑到ZNS SSD和LSM-tree都遵循严格的顺序写约束，其软硬件特征高度重合， 将一些应用移植到ZNS SSD上会获得更好的性能。典型案例如基于ZenFS[10]的RocksDB[13]。下面简要介绍三篇ZNS相关论文及其核心思想。

### ZNS+

ZNS+是一种高级的区域命名空间接口（Zoned Namespace Interface），它支持在存储设备内部进行区域压缩（In-Storage Zone Compaction）。ZNS+是为了解决日志文件系统（LFS）在执行段压缩时的高消耗问题而提出的。它允许主机将数据复制行为下放到SSD存储器层面异步处理，从而提高效率。

**ZNS+的关键设计：**

- **设备内区块压缩**：ZNS+支持在SSD内部执行数据复制，以此加速段压缩过程3。
- **异步处理**：ZNS+的区域压缩命令是异步执行的，主机不需要等待命令完成即可继续执行后续的IO请求，这有助于提高整体性能3。
- **稀疏顺序覆写**：ZNS+支持稀疏顺序覆写，允许在不复位的情况下对区域进行覆写，提高了效率。

具体地，ZNS+引入了新的命令`zone_compaction`和`TL_open`，其中`zone_compaction`用于请求设备级区块压缩，而`TL_open`允许在不复位的情况下对区域进行覆写。这些命令的引入，以及ZNS+的异步处理能力，使得主机不需要等待命令完成即可继续执行后续的IO请求，从而提高整体性能。

此外，ZNS+的设计考虑了与日志文件系统的兼容性，并旨在减少主机端的计算资源和带宽占用。ZNS+的实现在SSD模拟器和真实的SSD上都进行了，并通过修改文件系统（如F2FS）来充分利用ZNS+的特性。性能提升的研究表明，ZNS+存储系统在文件系统性能上比传统ZNS有显著提升。

ZNS+的映射机制利用逻辑地址空间的划分和映射，通过Zone ID、StripeID、ChipID和块内偏移实现数据的精确定位。这种设计允许ZNS+利用SSD的内部并行性，同时将存储维护的很多责任从SSD本身转移到了主机系统。

总的来说，ZNS+通过其先进的接口设计和特性，为提高SSD存储设备的性能和效率提供了有效的解决方案，尤其是在需要高并行写入性能等对存储有特别需求的应用场景中。



### eZNS

**概述：**eZNS（Elastic Zoned Namespace）是一种为提高ZNS SSD（Zoned Namespace SSD）性能而设计的弹性分区命名空间接口。在现有的 ZNS SSD基础上，eZNS 旨在提供一个应用透明的、灵活高效的逻辑分区抽象层，以适应工作负载运行时行为、并充分利用SSD的闪存并行性和激活的分区资源，并减少多租户间性能干扰。



**提出背景**：随着SSD取代机械硬盘成为主流存储设备，传统的块接口与SSD的闪存介质特性不匹配，导致性能波动和成本增加。因此，NVM Express提出了基于 Zoned Namespace（ZNS）的新存储接口。ZNS接口技术因此被提出，将逻辑地址空间分为固定大小的分区每个分区必须顺序写入，以适应闪存的特性。ZNS 接口可以提高写入吞吐量、降低访问延迟、减少写入放大和过量预配，从而提高存储系统的性能和成本效率。然而，ZNS 设计也存在一些局限，例如分区接口的静态和不灵活，导致分区资源利用率低下或过量预配，以及不可控的 I/O 延迟。

旨在解决 ZNS的接口设计的一些局限性，例如区域被分配后不能灵活调整资源。

**eZNS的关键技术**：

- **串行的物理分区条带分配策略**（Serial Zone Allocator）：避免物理分区分配时的重叠，提高并行性。
- **动态的物理分区条带膨胀策略**（Zone Ballooning）：根据负载需求动态调整条带宽度，优化写带宽和资源分配的公平性2。
- **阻塞感知的分区读写请求调度器**（Zone I/O Scheduler）：通过拥塞控制和写缓存准入策略，减少多租户场景下的性能干扰。

该工作进行了系统、真实的评估。实验结果显示eZNS在吞吐量和尾部延迟方面取得了显著改善，eZNS可以实现对ZNS SSD的透明使用，并弥合了应用程序需求与区域接口特性之间的差距。具体来说，与静态区域接口相比，eZNS在吞吐量方面提高了17.7%，在尾延迟方面提高了80.3%。这表明eZNS在提高性能和降低延迟方面具有显著效果，可能对各种应用场景都有积极影响。



### ZNSwap

ZNSwap是一种针对最新的Zoned Namespace (ZNS) SSDs进行优化的交换子系统。该工作探索了ZNS作为内存交换设备的应用可能，一方面利用了 ZNS SSDs 提供的粗粒度分区抽象来增强成本效率；另一方面，它利用ZNS在驱动器上对数据管理的显式控制，引入了一个集成于操作系统内存交换逻辑共同设计的高效主机端垃圾回收器（GC）来优化内存交换。此外，ZNSwap实现了跨层优化，例如GC直接访问Linux内核中的交换使用统计信息，以实现细粒度的交换存储管理，并在操作系统资源隔离机制中正确计算GC带宽使用情况，以提高多租户环境中的性能隔离。

具体地，ZNSwap 的核心设计思路是利用 ZNS SSD的特性，将每个区域（zone）配置为一个交换分区（swap partition）。传统的交换设备通常是基于块设备的，而 ZNS SSD 则是基于区域的。因此，利用 ZNS SSD 作为交换设备需要重新设计交换系统以适应 ZNS SSD 的特性。于是，ZNSwap 引入主机端的垃圾回收器（Garbage Collector, GC）集成进Linux Swap的交换逻辑中，从而提高了在主机端对数据管理的控制，实现了一个高效的交换分区设备，适用于大规模的内存扩展。

通过使用标准的Linux交换基准测试和两个生产级键值存储系统的评估，ZNSwap展示了与传统SSD上的Linux交换相比的显著性能优势，例如在不同内存访问模式下具有稳定的吞吐量，并在实际使用场景下，99th百分位延迟降低了10倍，吞吐量提高了5倍。



## 论文的主要内容与结构

>待补充

# 相关技术基础

在本章节中，我们首先介绍在ZNS SSD出现之前的几种新型SSD技术，随后我们介绍一种非常广泛的应用场景——键值存储与LSM-Tree模型，最后我们将自顶向下地介绍本文将涉及到的Linux I/O栈中的关键概念和技术，并讨论传统I/O栈存在的问题。

## 几种新兴SSD技术

### Multi-Stream SSD

Multi-Stream SSD是另一种针对提高SSD性能而设计的技术。它通过引入多个活跃的写入通道（即数据流），允许操作系统根据数据的不同特性和预期寿命，将数据分散存储在SSD的不同区域。每个数据流可以独立管理，减少了不同数据类型之间的相互干扰，从而降低了写入放大效应，并提高了SSD的耐久性和性能。

Multi-Stream SSD技术特别适用于那些具有高写入负载和数据生命周期差异显著的应用场景。例如，在数据库和日志记录系统中，某些数据可能会频繁更新，而其他数据则可能长时间保持不变。通过将这些数据分配到不同的数据流，Multi-Stream SSD可以减少不必要的数据迁移，提高整体性能。

尽管Multi-Stream SSD提供了诸多优势，但它同样需要操作系统和SSD固件的支持，以充分利用其特性。此外，由于需要正确预测数据的生命周期并有效管理不同数据流，使用该技术也为操作系统和应用开发者带来了额外的工作和挑战。

### Open-Channel SSD (OC SSD)

开放通道固态硬盘（Open-Channel SSD）是一种新型的存储设备，它在传统固态硬盘的基础上进行了重要的改进。与传统SSD相比，OC SSD的最显著特点是取消了传统的Flash Translation Layer（FTL），将数据管理的责任转移到了主机端。这意味着操作系统可以直接管理SSD的闪存资源，从而实现更灵活、更精细的数据管理和优化。

OC SSD的主要优势在于其允许操作系统更精确地控制数据的放置和回收过程，以适应特定的工作负载。通过优化垃圾回收过程，OC SSD可以有效减少写入放大效应（Write Amplification），从而延长SSD的寿命。此外，OC SSD还可以实现I/O隔离，减少不同用户数据之间的相互干扰，特别是在多租户环境中。

然而，OC SSD也带来了新的挑战。操作系统需要承担更多的责任，包括数据管理、磨损均衡和错误恢复等。这不仅增加了操作系统的复杂性，还可能对系统的整体性能产生影响。此外，OC SSD的实现与应用需要操作系统、文件系统和SSD固件之间的紧密协作。

### ZNS SSD与前置技术的关系

Zoned Namespace SSD（ZNS SSD）代表了对现有固态存储技术的一种进一步的优化与发展。在传统的SSD技术如Open-Channel SSD和Multi-Stream SSD中，已经实现了对数据管理更深层次的优化，这些技术主要关注于改进数据的写入效率和减少写入放大现象。Open-Channel SSD通过取消传统的Flash Translation Layer（FTL）并将数据管理的责任转移到主机端，使得数据存储过程更加透明，允许操作系统执行更精细的数据放置和回收策略。而Multi-Stream SSD通过引入多数据流的概念，允许系统根据数据的特性进行分区管理，有效地降低了数据干扰和写入放大。

ZNS SSD在这些技术的基础上进一步引入了基于区域的存储模型，通过物理上将SSD存储空间划分为多个独立的区域，每个区域维护自己的写入队列。这种设计有效地管理了写入操作的局部性，进一步减少了写入放大效应并提高了写入操作的预测性和效率。此外，ZNS SSD的区域化管理降低了垃圾回收的复杂性和频率，显著提升了SSD的整体性能和耐用性。

ZNS SSD与OC SSD和Multi-Stream SSD共同向着减少写入放大、提高数据写入效率和扩展设备使用寿命的目标迈进。上述技术都通过不同的机制改善了存储系统的性能，而ZNS SSD的引入可视为对这一系列技术革新的延续和补充。在设计面向未来的高效能数据中心和高性能计算环境时，这些技术的综合应用能够提供更为灵活和高效的解决方案。

## 键值存储与LSM-Tree模型

### 键值存储

键值存储（Key-Value Store）是数据库领域的一种重要存储模型，在这种存储模型中，数据被组织为简单的键值对（Key-Value Pairs），其中键（Key）是唯一的，用于标识和检索对应的值（Value）。这种直接映射的方式，使得键值存储在处理大量数据时能够提供快速的数据访问和高效的存储管理。
键值存储的简单性是其最显著的特点之一。由于键值对的直接映射关系，键值存储的接口通常非常简单，易于编程和使用。同时，这种简单性也使得键值存储能够快速地进行数据的读写操作，满足现代应用对于性能的高要求。此外，键值存储的灵活性也不容忽视。键值对的结构允许存储各种类型的数据，包括但不限于字符串、数字、对象等，这使得键值存储可以广泛应用于不同的应用场景，如缓存系统、会话管理、配置存储以及分布式系统等。
在技术实现方面，键值存储可以基于内存或磁盘进行数据存储。内存数据库如Redis，利用内存的高速特性，提供了极高的数据访问速度，成为许多实时应用的首选存储解决方案。而磁盘数据库如LevelDB，则通过优化磁盘操作，实现了高效的数据存储和访问。此外，分布式键值存储如Cassandra和Riak，通过在多个节点上分布数据，不仅提高了系统的可扩展性，还增强了数据的可靠性和容错性。
键值存储的研究领域广泛，涉及性能优化、数据一致性、容错机制、数据压缩和安全性等多个方面。在性能优化方面，研究者致力于通过各种技术手段，如内存优化、索引结构优化等，进一步提升键值存储的读写性能。数据一致性是分布式系统中的关键问题，研究者探讨了多种一致性模型，以确保在分布式环境中数据的一致性和可靠性。容错机制的研究则关注如何在节点故障的情况下，保证系统的稳定运行。数据压缩技术的研究旨在减少存储空间的需求，提高存储效率。安全性研究则关注如何保护存储在键值存储中的数据，防止未授权访问和数据泄露。
综上所述，键值存储作为一种高效的数据存储解决方案，在现代信息技术领域扮演着越来越重要的角色。随着技术的发展和应用需求的不断变化，键值存储的研究和应用将持续深化，为解决新的数据存储挑战提供更多的解决方案。

### LSM-Tree模型

LSM-tree（Log-Structured Merge-Tree）模型是一种数据存储模型，广泛应用于键值型数据存储引擎。LSM-tree模型旨在解决传统数据库在处理大规模写入操作时所面临的性能瓶颈。其设计理念是将数据按层次结构存储，将频繁的写入操作与相对较少的读取操作分离，从而优化整体性能。

在LSM-tree模型中，数据首先被写入内存中的结构，称为memtable。由于内存访问速度远高于磁盘，这一步骤确保了极高的写入效率。随着数据的累积，当memtable达到一定大小时，会被刷新到磁盘上，形成不可变的SSTable。刷新过程通常伴随着数据排序，以便后续的读取和合并操作。

磁盘上的SSTable以层次结构组织，新的SSTable位于顶层。随着时间的推移，SSTable通过合并过程合并成更大的表。合并过程不仅减少了SSTable的数量，还删除了过时或重复的数据，优化了存储空间的利用。合并策略的设计直接影响LSM-tree的性能，包括写入放大因子和读取性能。

LSM-tree模型在写入性能上具有显著优势，但读取性能取决于SSTable的结构和合并策略。系统在读取数据时首先在memtable中查找，如果不成功，则在磁盘上的多个SSTable中进行查找。为提高读取效率，LSM-tree通常采用布隆过滤器等数据结构来减少对磁盘的无效访问。

尽管LSM-tree模型在提高写入性能方面表现出色，但是仍存在一些问题。例如，写入放大因子可能导致实际写入磁盘的数据量远大于原始数据量，在存储资源受限的环境中可能成为问题。此外，LSM-tree将随机写转换为顺序写，是以牺牲读性能为代价的。随着SSTable数量增加，读取性能可能受到影响。为解决这些问题，研究者也提出了多种优化策略和技术，如布隆过滤器、层级合并策略、缓存机制和数据压缩技术。

LSM-tree模型以其在写入密集型应用中的优异性能成为现代数据库系统的关键组成部分，是最常见的存储引擎模型之一。并且随着各大公司对LSM-tree的广泛使用，大大促进了该技术的进步，未来，对LSM-tree模型的研究和优化将继续深入，以满足不断增长的数据存储和管理需求。

LSM树已被应用于诸如RocksDB、LevelDB、BigTable、Cassandra和HBase等流行的键值存储中。LevelDB是谷歌开源的经典的基于LSM-Tree的开源键值存储引擎。RocksDB是基于LevelDB优化的工程性实现，广泛用于各大互联网公司。

## 传统Linux I/O栈

### Linux I/O简介

I/O（输入/输出）是在主存和外部设备（磁盘驱动器、网络、终端）之间复制数据的过程。输入是从外部设备复制到主存，输出是从主存复制到外部设备。在Linux系统中所有的I/O设备都被映射称为文件，所有的输入输出都被当做相应文件的读和写来执行，所以内核提供了系统级的I/O函数接口，使得所有输入输出都以统一且一致的方式来执行。Linux I/O栈（I/O Stack）是指在Linux操作系统中，从用户空间到内核空间，再到硬件设备，整个数据输入输出过程中所涉及的一系列组件和操作的集合。这个栈涵盖了从应用程序发起I/O请求开始，到数据实际在硬件上进行读写的完整流程。下面我们将自上而下地介绍Linux I/O栈的各个层次中的关键概念或组件：

用户空间（User Space）：用户空间是应用程序运行的地方。当应用程序需要进行I/O操作时（如读写文件、网络通信等），它会通过系统调用（system call）向操作系统内核发出请求。系统调用是用户空间与内核空间之间通信的桥梁。

系统调用接口（System Call Interface）：系统调用接口是内核提供给用户空间的一组函数，用于执行各种I/O操作。这些函数封装了复杂的内核操作，对用户空间透明。常见的系统调用包括`read()`、`write()`、`open()`、`close()`等。

内核空间（Kernel Space）：内核空间是操作系统内核运行的地方，负责管理计算机的资源和提供各种服务。当收到系统调用请求后，内核会进行相应的处理，包括权限检查、资源分配等。

文件系统抽象层（VFS - Virtual File System）：VFS是Linux内核的一个组件，它提供了一个统一的文件系统抽象层。无论底层是何种类型的存储设备或文件系统，VFS都能以统一的方式处理I/O请求，简化了内核和应用程序的设计。

设备驱动（Device Driver）：设备驱动是内核的一部分，用于管理特定类型的硬件设备。它负责将内核的通用I/O请求转换为特定硬件能够理解的命令。设备驱动还处理硬件的特性和限制，如缓冲管理、错误处理等。

I/O调度器（I/O Scheduler）：I/O调度器是内核中的一个组件，用于优化磁盘I/O请求的执行顺序。它通过算法（如完全公平队列CFQ、Deadline等）来减少磁盘寻址时间，提高I/O效率。

硬件抽象层（HAL - Hardware Abstraction Layer）：HAL是内核与硬件之间的中间层，它提供了一组通用的硬件访问接口。HAL隐藏了硬件的具体细节，使得内核和设备驱动可以以统一的方式与硬件交互。

中断处理（Interrupt Handling）：当I/O操作完成时，硬件设备会通过中断信号通知CPU。内核中的中断处理程序会响应这些中断，完成I/O操作的收尾工作，如更新缓冲区状态、唤醒等待的进程等。

硬件设备（Hardware Devices）：硬件设备是I/O栈的最底层，包括磁盘、网络接口卡等。硬件设备负责实际的数据存储和传输工作。

依托上述组件，Linux I/O主要有如下几大逻辑功能：

- **系统调用**：提供了用户空间与内核空间之间的接口。
- **VFS**：提供了统一的文件系统抽象。
- **设备驱动**：管理硬件设备，将I/O请求转换为硬件命令。
- **I/O调度器**：优化磁盘I/O请求的执行顺序。
- **中断处理**：响应硬件设备的中断信号，完成I/O操作。

Linux I/O栈是操作系统中处理数据输入输出的核心机制。它通过一系列层次化的组件，从用户空间到硬件设备，管理着数据的流动。



### LinuxI/O架构图

![image-20240513033213069](%E6%AF%95%E8%AE%BE.assets/image-20240513033213069.png)

> 
>
> linux I/O栈 结构图
>
> ![img](%E6%AF%95%E8%AE%BE.assets/Linux-storage-stack-diagram_v6.2.png)
>
> LinuxIO栈的复杂程度

### 传统I/O栈存在的问题

整个I/O路径涉及了很多层次，并且面对应用的需求越来越繁杂，后续提出的针对某特定场景的优化越来越多，最终使得现行的I/O栈非常冗杂。并且I/O栈仍面临非常多的问题，严重影响了存储系统的性能：

1. **性能瓶颈**：传统I/O栈设计之初并未考虑到SSD的高吞吐量和低延迟特性，因此在处理高速数据传输时，I/O栈可能成为整个系统的性能瓶颈67。
2. **高延迟**：由于传统I/O栈在数据传输过程中涉及多次上下文切换和缓冲，导致整体延迟增加，这在对延迟敏感的应用中尤为突出。
3. **IOPS限制**：传统I/O栈可能无法充分利用SSD的高IOPS（每秒输入/输出操作数）能力，限制了其性能表现。
4. **资源消耗**：在处理大量并发I/O请求时，传统I/O栈可能会消耗大量CPU和内存资源，尤其是在进行大量随机读写操作时25。
5. **扩展性问题**：随着存储设备容量的增加和分布式系统的普及，传统I/O栈在扩展性上存在限制，难以适应大规模存储系统的需求。
6. **写入放大（Write Amplification）**：传统I/O栈在进行垃圾回收（Garbage Collection, GC）和数据迁移时，可能会多次擦写同一物理块，导致写入放大现象，缩短SSD的使用寿命。
7. **数据管理效率**：传统I/O栈对于数据的放置和管理可能不如针对SSD优化的存储栈来得高效，导致存储空间利用率不高。
8. **缺乏硬件特性利用**：现代SSD具有一些能够提升性能的硬件特性（如NVMe的队列特性），传统I/O栈未能充分利用这些特性，从而无法发挥SSD的全部性能12。
9. **I/O调度问题**：在高负载情况下，传统I/O栈的调度算法可能导致I/O请求的不公平等待，影响整体性能。

## 本章小节

在本章中，我们介绍了与Zoned Namespace SSD（ZNS SSD）相关的一些关键技术基础。首先，我们探讨了几种新兴的SSD技术，包括Multi-Stream SSD和Open-Channel SSD（OC SSD）。这些技术在提高SSD性能、降低写入放大效应和提升设备寿命等方面发挥了重要作用。

接着，我们介绍了键值存储与LSM-Tree模型，这两者是现代存储系统中常见的重要组成部分。键值存储模型简单而灵活，适用于各种应用场景，而LSM-Tree模型则在处理大规模写入操作时表现出色，成为许多数据库系统的存储引擎之一。

最后，我们深入探讨了传统Linux I/O栈存在的问 题，包括性能瓶颈、高延迟、资源消耗等。这些问题严重影响了存储系统的性能和可扩展性，需要通过优化和改进来解决。 ZNS SSD作为对传统SSD技术的进一步优化和发展，为解决这些问题提供了新的思路和可能性。

 





# ZNS SSD性能分析与写入优化

在本章节中，前半部分进行ZNS的基本测试环境的搭建与实验设计，包括介绍使用ZNS依赖的软硬件环境，硬件环境包括，模拟器，真实设备，软件环境包括相关框架、工具库，以及基于这些软硬件环境的性能实验设计与分析。后半部分，阐述现有的RocksDB实现及其对ZNS设备的适配，并详细介绍基于RocksDB的专为ZNS设计的文件系统ZNFS的架构和优化策略。

## ZNS SSD硬件基准测试

###  ZNS的硬件环境

由于ZNS使用Zone接口语义，导致其不再与传统SSD通用，并且由于其配套的文件系统与应用刚刚起步，目前不能做到即插即用，下面将详细介绍本工作所基于的ZNS的模拟及真实设备的工作环境，并对初期调研的结果进行总结并讨论。

#### 模拟环境——NVMeVirt

本小节基于对ZNS模拟环境的广泛调研，包含QEMU，FEMU等模拟器以及最新的NVMeVirt模拟器。

**QEMU**

QEMU（Quick EMUlator）是一种开源的、性能优异的模拟器和虚拟机软件，它能够模拟多种处理器架构和硬件设备。QEMU通过动态二进制翻译技术，提供对客户操作系统的高效模拟，使其能够在宿主机上运行。在存储设备模拟方面，QEMU能够模拟传统的硬盘驱动器（HDD）以及固态硬盘（SSD）的行为。QEMU模拟的SSD设备可以配置不同的特性，如存储容量、I/O模式和性能参数，从而为研究人员和开发人员提供一个灵活的平台，用以开发和测试针对SSD优化的操作系统、文件系统和存储协议。此外，QEMU还能够模拟SSD的随机读写、 TRIM操作和垃圾回收等复杂行为，为存储系统的研究提供了一个功能丰富的实验环境。

**FEMU**

FEMU（Flexible EMUlator）是一种灵活的模拟器框架，它允许用户自定义和扩展硬件模型，以满足特定的模拟需求。FEMU在模拟SSD设备方面，提供了更细致的控制和更高的灵活性。通过FEMU，研究人员可以精确地模拟SSD的内部操作，包括页面管理、块擦写、FTL（闪存转换层）算法和磨损均衡策略等。FEMU还能够模拟SSD在不同负载和工作条件下的性能表现，以及其对宿主机系统行为的影响。此外，FEMU支持多种SSD特性和配置，包括不同的闪存类型、接口标准和性能参数，使得研究人员能够在一个受控且可重复的环境中，对SSD存储系统进行深入分析和优化。FEMU的这些特点使其成为研究新型存储技术和评估存储系统性能的理想工具。

**NVMeVirt**

然而，QEMU作为一种通用模拟器，在模拟SSD设备时存在一些局限性。尽管其设计初衷是提供对多种硬件设备的模拟，但在复现SSD的真实性能特性，如IOPS和延迟方面，QEMU可能无法完全达到预期效果。此外，QEMU在模拟SSD的特定硬件特性，如NVMe接口的高级功能时，未能充分捕捉其性能和功能优势。写入放大效应和垃圾回收过程是SSD中重要的性能和寿命影响因素，QEMU无法这些方面对SSD设备进行模拟。FEMU是在QEMU基础上针对SSD设计的模拟器，提供了相对更高的准确性和可扩展性，但在模拟过程中也存在一些缺陷。由于FEMU仍是基于QEMU的工作，其作为虚拟机运行时会引入很多额外的性能开销，且会出现设备性能表现不稳定的情况。而且，FEMU的安装和配置过程比较复杂，总体而言比较笨重。此外，FEMU在模拟大型SSD或高负载场景时对计算资源的需求较高，一方面对实验平台要求更高，另一方面这也限制了可模拟的规模。尽管FEMU在模拟SSD方面表现出色，但在模拟其他新型的存储设备或更复杂的存储系统时存在局限性。

NVMeVirt 是一款新型的轻量级 SSD 仿真器，与前两者的显著区别是，它通过内核模块来模拟各种类型的 NVMe 设备，包括传统 SSD、低延迟高带宽 NVM SSD、分区命名空间 SSD（ZNS SSD）以及键值 SSD。NVMeVirt 的设计目标是促进软件定义的 NVMe 设备，允许用户使用自定义功能来定义任何 NVMe 设备类型，并在软件中桥接主机 I/O 堆栈和虚拟 NVMe 设备之间的差距。与传统的QEMU和FEMU模拟器相比，NVMeVirt提供了更高的灵活性和可定制性，允许用户定义具有特定特性的NVMe设备类型。作为一个内核模块，NVMeVirt与系统的集成度更高，能够提供更接近真实硬件的性能模拟。此外，NVMeVirt支持模拟包括传统SSD、ZNS SSD和键值SSD在内的多种高级存储配置，这些是现有模拟器不支持的功能。NVMeVirt的设计使其成为存储系统研究的有力工具，可以用于研究数据库引擎的性能特性，以及扩展NVMe规范以提高键值SSD性能等研究工作。因此，NVMeVirt模拟器特别适合于需要定制化和高性能模拟的研究和开发场景。本工作的虚拟环境基于NVMeVirt实现。

#### 物理设备——inspur ZNS SSD



目前，研制ZNS SSD设备的公司主要有西部数据，三星等。西数已推出ZNS SSD产品——ZN540，其各版本的部分参数如下表所示

Capacity    1024GB 2048GB 4096GB 8192GB

Form Factor 	U.2

Interface  PCle 3.0 1x4 or 2x2

Read (max MB/s, Seg 128KiB) 3200  3200  3200  3200

Write (max MB/s, seg 128KiB)1200 1000 2000 2000

Read lOPs (max, Rnd 4KiB) 406K390K 442K 486K

Read Latency (us, avg.)  73 80 80 90





本实验基于浪潮ZNS SSD完成。其关键参数见第四章实验部分。



### ZNS的软件环境

本小节的介绍包含几个重要的软件框架和依赖库。

#### libzbd库

**libzbd** 是由 Western Digital Corporation 开发并维护的一个开源项目，旨在为 Linux 内核提供对 Zoned Block Devices (ZBD) 的支持。ZBD 是一种新兴的存储设备规范，它与传统的随机访问块设备不同，ZBD 设备采用分区（zone）的概念来组织数据，每个分区支持顺序写入和批量擦除操作，这与传统的块设备（每个块都可以独立读写）有所不同。这种设计特别适合于固态存储技术，尤其是对于那些使用 NAND 闪存作为存储介质的设备，ZNS SSD就是其中最新最典型的一种。

具体地，libzbd库作为内核模块实现，libzbd 的编译产物是一个 `.ko` 文件，它可以被加载到 Linux 内核中，从而扩展内核的功能集。在操作系统的架构中，libzbd 属于内核空间，它需要执行与硬件直接交互的任务，如I/O操作、设备状态管理等。内核模块提供了一种机制，允许操作系统内核在运行时动态加载和卸载功能模块，这为系统带来了更高的灵活性和可扩展性。我们可以通过引用libzbd.a使用该库中的函数以操作ZNS SSD设备。以下是对libzbd库中部分主要函数及其功能的简要介绍：

1. **zbd_device_is_zoned()**: 用于测试一个块设备是否为分区块设备。这个函数可以帮助用户确定一个设备是否支持分区管理。
2. **zbd_open()** 和 **zbd_close()**: 分别用于打开和关闭一个分区块设备。在使用该库进行操作之前，需要先打开设备，并在操作完成后关闭设备。
3. **zbd_get_info()**: 获取一个已打开分区块设备的信息，包括设备的基本属性和分区的状态信息。
4. **zbd_report_zones()** 和 **zbd_list_zones()**: 用于获取分区块设备的分区信息。可以获取所有分区的详细信息，包括分区类型、状态、起始位置、大小等。
5. **zbd_report_nr_zones()**: 获取分区块设备的分区数量。这对于确定设备的容量和空间分布非常有用。
6. **zbd_zone_operation()**: 执行分区管理操作，如重置写指针、显式打开或关闭分区等。
7. **zbd_reset_zones()**, **zbd_open_zones()**, **zbd_close_zones()**, **zbd_finish_zones()**: 分别用于重置、显式打开、关闭和完成分区操作，以实现对分区的灵活管理。

此外，还定义了一系列用于操作分区描述符信息的宏定义和实用工具函数，例如获取分区类型、状态、起始位置、大小、容量等信息，以及设置日志级别、获取设备模型、获取分区类型和状态的字符串描述等。

然而该库也有一些不足，在使用libzbd库时，需要注意线程安全性，因为该库不维护任何打开分区块设备的内部状态，因此需要由应用程序确保对分区的操作正确进行互斥。可以通过多线程应用程序中的同步机制来实现对分区的正确操作。

总的来说，libzbd库提供了一组功能丰富的函数和数据结构，简化了对分区块设备的管理和使用，为分区存储设备的开发和应用提供了便利，大多数适配ZNS的应用程序和文件系统都是基于该库实现的。libzbd库是对标盘进行测试工作的基础的依赖库之一。

#### FIO for ZNS

FIO（Flexible I/O Tester）是一款功能强大的开源测试工具，广泛应用于评估存储和网络系统的性能。它通过提供高度可定制的测试选项，允许用户模拟各种工作负载，从而深入理解存储介质的读写性能、IOPS、延迟等关键指标。
FIO的设计注重灵活性和可扩展性，支持多线程和多进程运行，有效利用多核处理器的能力。它能够针对文件和块设备执行测试，覆盖从单个存储设备到复杂存储系统的广泛场景。FIO的测试工作负载可以模拟真实应用的I/O模式，包括顺序操作、随机访问以及混合读写等，使其成为数据库、文件服务器、Web服务器等应用性能测试的理想选择。
该工具还具备实时监控功能，可以在测试执行期间提供性能反馈，并生成详尽的日志记录，便于后续的性能分析和结果验证。FIO支持多种操作系统，包括Linux、Windows和macOS，使其成为跨平台性能测试的通用解决方案。
使用FIO时，用户通过编写配置文件来定义测试参数，然后通过FIO命令行工具执行测试。测试完成后，FIO将提供包含丰富统计信息的结果文件，为性能评估和系统优化提供数据支持。
因其强大的功能和易于使用的特点，FIO已成为存储和系统管理员、开发人员以及性能工程师进行存储性能评估、配置优化和故障排除的重要工具。在学术研究和工程实践中，FIO常被用于生成可复现的实验数据，支持对存储系统性能的深入分析。

从版本3.30开始，FIO扩展了其功能，以支持Zoned Namespace (ZNS) SSD的测试。在使用FIO对ZNS SSD进行测试时，用户可以利用多种参数来定制测试案例，以便更准确地模拟和评估设备的性能。以下是一些关键的参数：

1. **ioengine**：指定用于数据传输的后台引擎。对于ZNS SSD，可以选择`psync` ioengine，它支持与zone的顺序写入约束兼容的数据同步。
2. **--offset_increment**：这个参数用于定义每个作业（job）的起始偏移量增量。在ZNS SSD的上下文中，它通常与zone的大小相对应，确保每个作业都在不同的zone上操作。
3. **--size**：定义测试中使用的总数据大小。这个参数应与ZNS SSD的zone大小和测试需求相匹配，以避免跨zone的写入。
4. **--numjobs**：指定并行运行的作业数量。这个参数可以用于模拟多线程或多进程访问ZNS SSD的场景。
5. **--job_max_open_zones**：为每个作业设置最大的开放zone数。这个参数有助于控制每个作业可以同时访问的zone数量，以符合ZNS SSD的使用模式。

除了这些参数，FIO还允许用户选择测试的I/O模式（如读写、随机/顺序）、块大小、以及是否启用直接I/O等。此外，FIO的灵活性还体现在可以结合使用多个参数来模拟复杂的工作负载模式，如混合读写操作或特定的I/O深度（iodepth）。

为了简化测试过程，并为常见的测试场景提供预设的配置，ZBDBench存储库提供了一系列的FIO作业文件和基准测试脚本。这些预设可以根据特定的测试需求进行调整，使得用户可以快速开始测试，并获取有关ZNS SSD性能的洞察。

在实际使用中，用户可以根据自己的测试目标和ZNS SSD的特性，选择合适的ioengine和参数，执行定制化的测试。通过分析FIO生成的详细测试报告，用户可以了解ZNS SSD在不同工作负载下的性能表现，包括吞吐量、延迟、IOPS等关键指标。

## RocksDB

本小节介绍RocksDB的基本架构，读写流程，以及已有的对ZNS的适配工作——ZenFS

### RocksDB简介

**RocksDB** 是一个高性能的持久化键值存储引擎，由 Facebook 基于 Google 的 LevelDB 代码库于 2012 年开发。该引擎专为固态硬盘（SSD）优化，设计用于满足大规模分布式系统的存储需求，并作为库组件嵌入到高级应用程序中。

RocksDB 沿用了LevelDB的 Log-Structured Merge-Tree（LSM-Tree）结构，与 LevelDB 相比，RocksDB 引入了多项优化和改进，尤其是在高并发写入需求的场景下。关键改进之一是降低了写入幅度，即每次写入操作引起的额外磁盘写入量，另一个关键改进是通过优化的压缩过程，RocksDB 有效提高了写入效率。RocksDB在处理大规模数据时表现出色，特别适用于需要高写入吞吐量和低延迟的场景。其特点包括：

1. **高性能写入**：优化写入路径以降低写入延迟，并处理高并发写入请求。
2. **低写入幅度**：通过压缩算法和数据结构设计减少磁盘写入影响。
3. **灵活的配置选项**：提供丰富的配置选项以适应不同需求。
4. **丰富的功能**：支持事务、压缩、备份和迭代器等高级功能。

RocksDB自发布以来，被长期广泛地使用，并且保持着很高的更新优化频率。例如，在 Facebook 被广泛应用于超过 30 个不同的应用程序，存储着数 PB 的生产数据。除了作为数据库存储引擎，RocksDB 也被用于流处理、日志/排队服务、索引服务和 SSD 缓存等多种服务。其可定制性使其能够适应各种工作负载，用户可以根据自己的需求进行针对性调优，无论是为读性能、写性能、空间使用率，还是它们之间的平衡点。综上所述，RocksDB 以其高性能的写入、低写入幅度、灵活的配置选项和丰富的功能而成为多种应用场景的首选存储引擎之一。

### 基于固态硬盘的嵌入式存储

> ZNS的典型应用RocksDB with  ZenFS(现有ZenFS存在的问题)
>
> ZenFS做了啥。
>
> ZenFS在WAL批量写入时的问题。

过去十年间，我们见证了基于固态硬盘的SSD在在线数据服务中的广泛应用。低延迟和高吞吐量的设备不仅挑战了软件充分利用其全部功能的能力，还改变了许多有状态服务的实现方式。SSD为读/写操作提供了每秒数十万次的IOPS，这是传统磁盘的数千倍，同时支持数百MB/s的带宽。然而，由于编程/擦除周期的限制，高写入带宽无法持续。这些因素为重新思考存储引擎的数据结构提供了机会。

SSD的高性能在许多情况下将性能瓶颈从设备I/O转移到了网络，无论是在延迟还是吞吐量上。对于应用程序来说，更倾向于设计其架构以将数据存储在本地SSD上，而不是使用远程数据存储服务。这增加了对嵌入在应用程序中的键值存储引擎的需求。

具体地，RocksDB 实例负责管理单个服务器节点上的存储设备数据，不涉及主机间操作，如复制和负载均衡，也不执行高级操作，如检查点等。这种统一的存储引擎相较于针对每个应用单独搭建自己的存储子系统，带来了显著的优势：它避免了重复处理数据损坏、异常恢复、文件系统错误处理等问题；不同系统间可以共用一套基础设施，如监控系统、运维工具、调试工具等；底层的统一性也使得调试经验在不同应用间可以复用。

另一方面，RocksDB 是高度可定制的，因此它作为一个核心 KV 存储引擎能适应各种工作负载，用户可以根据自己的需要对它进行针对性调优，如为读性能优化，为写性能优化，为空间使用率优化，或它们之间的某个平衡点。正是因为如此灵活的可配置性，RocksDB 可以作为很多不同数据库的存储引擎使用，如 MySQL，CockroachDB，MongoDB，TiDB 等，也可以满足流式计算（Stream processing），日志服务（Logging/queuing services），索引服务（Index services），缓存服务（Caching on SSD）等多种特性完全不同的业务需求。

### RocksDB的架构

我们按照读写流程来剖析RocksDB的架构，这也有助于后续解释ZNS在写入流程中发挥的重要作用。

#### 写入流程

数据写入过程首先涉及将数据添加到内存中的写缓冲区，即MemTable，同时为了数据恢复，所有更新也会记录到磁盘上的预写式日志（WAL）。MemTable通常由跳表（SkipList）实现，**如图所示**，跳表以 O(log n) 的时间复杂度维护数据的有序性，从而支持高效的插入和搜索操作。当MemTable达到预设大小限制时，它会被标记为不可变（immutable），并从 MemTable 的角色转换为一个准备持久化到磁盘的阶段。MemTable中的内容被持久化（flush）到磁盘上的“排序字符串表”（Sorted String Table ，SSTable）数据文件中。此过程中，相关的WAL也会被丢弃。每个SSTable由多个均匀大小的数据块组成，每个数据块都配有索引块，以便进行高效的二分搜索。

![在这里插入图片描述](%E6%AF%95%E8%AE%BE.assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1pfU3RhbmQ=,size_16,color_FFFFFF,t_70.png)

RocksDB采用多层级的LSM树结构，**如图所示**，其中MemTable刷新生成的SSTable最初存放在Level-0。随着时间的推移，SSTable通过一个称为压实（Compaction）的过程被合并和优化，从而创建出更高级别的SSTable。压实操作移除冗余数据，如已删除或被覆盖的键值对，同时提高读取性能和空间效率。压实过程实际涉及垃圾回收，RockDB在这方面做了很多改进，下一个小节我们会详细讨论。

#### 读取流程

读取操作从MemTable开始，逐步检查每个级别的SSTable，直至Level-0以外的更高层级。在每个层级，RocksDB利用二分搜索算法查找指定的键。为了提高搜索效率，RocksDB使用布隆过滤器来排除那些不必要搜索的SSTable文件。如果需要执行范围扫描，则必须搜索所有层级的SSTable。

#### 压缩

由于LSM树中存在多个层级的SSTable文件（如Level-0、Level-1等），不同层级的SSTable文件可能存在重叠的键范围，而且随着写入操作的进行，会产生大量的过时和重复的数据。为了优化存储和提高查询效率，需要对这些SSTable文件进行合并和清理，这就是compaction的作用。

具体地，在RocksDB中，compaction是指将多个SSTable文件合并为更少且更大的文件，同时删除重复和过时的数据，并将数据重新组织以提高读取性能。具体来说，compaction过程包括以下几个步骤：

1. **选择合并的SSTable文件**：根据预设的合并策略和条件，选择需要合并的SSTable文件。通常是选择相邻层级的SSTable文件进行合并。
2. **合并数据**：将选定的SSTable文件中的数据合并为一个新的SSTable文件。在合并过程中，会删除重复的键，并根据需要执行数据压缩。
3. **重新组织数据**：重新组织合并后的SSTable文件，以便提高读取性能。通常会对数据进行排序和分块，以便进行更高效的查询。
4. **清理过时数据**：删除已合并的SSTable文件以及其中包含的过时数据，释放磁盘空间。

通过以上步骤，compaction过程可以优化存储布局，减少数据重复和过时数据，提高查询效率，并释放磁盘空间。这对于处理大规模数据和提高系统性能至关重要。因此，RocksDB对压缩过程做了很多优化。RocksDB在compaction方面的改进相比LevelDB主要体现在以下几个方面：

1. **并行化压缩任务**：RocksDB引入了并行化压缩任务的技术，使得多个压缩任务可以同时进行，充分利用多核CPU资源，提高了压缩效率。相比之下，LevelDB的压缩任务是串行执行的，一次只能处理一个任务，导致压缩过程耗时较长。
2. **整批处理压缩数据**：RocksDB采用了整批处理压缩数据的策略，通过批量读写整个文件，实现了高效的I/O操作。这种方式减少了磁盘访问次数，降低了系统的资源消耗。而LevelDB在压缩过程中采用的是逐个处理每个数据块的方式，导致了频繁的磁盘读写操作，性能相对较低。
3. **级别化的压缩目标**：RocksDB采用了级别化的压缩目标，即不同级别的SSTables具有不同的大小目标。这样可以根据数据特点和访问模式动态调整压缩策略，使得系统能够在不同场景下实现最佳的压缩效果和性能表现。而LevelDB在这方面的优化不如RocksDB灵活，缺乏动态调整压缩策略的能力。

综上所述，RocksDB在compaction方面的改进包括并行化压缩任务、整批处理压缩数据以及级别化的压缩目标等方面，这些改进使得RocksDB在处理大规模数据时表现更为出色，具有更高的存储效率和更好的性能表现。

### RocksDB与LevelDB的区别

RocksDB基于 LevelDB 并对其进行了多项改进和扩展。二者在架构设计上大同小异，但是LevelDB是机械硬盘时代的产物，而RocksDB针对固态硬盘做了优化，并且在其他方面进行了完善，对其进行的多项改进和扩展具体包括：

列簇（Column Family）：RocksDB 引入了列簇的概念，允许开发者将相关的键值对分组存储在不同的列簇中。这使得数据的管理和访问更加灵活，同时可以对每个列簇独立地进行压缩和读取操作。

不可变内存表（Immutable Memtable）：RocksDB 维护多个不可变内存表，当一个内存表满了之后，它会被写入磁盘，而新的写入操作则在新的内存表中进行。这种机制避免了 LevelDB 中可能出现的写停顿问题。

多线程压缩（Multi-threaded Compaction）：RocksDB 支持多线程进行数据压缩，这可以显著提高压缩操作的效率，尤其是在多核处理器上。

TTL（Time-to-Live）机制：RocksDB 提供了数据过期机制，允许开发者为键值对设置生存时间，过期的数据将被自动清理。

分离的线程池：RocksDB 将数据的刷新（flush）操作和压缩（compaction）操作分配到不同的线程池中，并且刷新操作具有更高的优先级。这种设计可以减少写入延迟，提高写入性能。

SSD优化：RocksDB 针对固态硬盘（SSD）进行了优化，减少了磁盘随机访问的次数，提高了整体性能。

Write-Ahead Log（WAL）管理：RocksDB 改进了 WAL 的管理机制，WAL 用于确保数据的持久性。RocksDB 允许在崩溃恢复时更有效地使用 WAL。

多样化的压缩策略：RocksDB 支持多种压缩算法，包括 Snappy、LZ4、Zlib 和 ZSTD 等，允许开发者根据数据特性和性能需求选择最合适的压缩策略。

自定义的压缩库和表格式：RocksDB 允许开发者使用自定义的压缩库和表格式，提供了更高的灵活性。

细粒度的控制和调整：RocksDB 提供了大量的配置选项，允许开发者针对不同的工作负载和硬件环境进行细致的调整。

支持二进制和压缩的索引：RocksDB 支持二进制和压缩的索引，这可以减少索引的存储空间需求，提高查询效率。

事务和检查点：RocksDB 提供了对事务的支持，允许进行原子写入操作，并且可以创建数据的检查点。

通用的文件系统接口：RocksDB 抽象了底层存储，允许在不同的文件系统上运行，包括本地文件系统、HDFS 等。

跨平台支持：RocksDB 可以在多种操作系统上运行，包括 Linux、macOS 和 Windows。

通过这些改进，RocksDB 成为了一个适用于各种场景的高性能键值存储解决方案，特别适用于需要高吞吐量和低延迟的应用。

### RocksDB对ZNS的支持

RocksDB 提供了一个灵活的插件机制，允许开发者根据自己的需求扩展数据库的功能。并且，RocksDB 通过其文件系统包装器 API 提供对独立存储后端的支持，该 API 是 RocksDB 访问其磁盘数据的统一抽象。从本质上讲，包装器 API 通过唯一标识符（例如文件名）识别数据单元，例如 SST 文件或预写日志 (WAL)，该标识符映射到一个可按字节寻址的线性地址空间（例如文件）。每个标识符除了随机访问和仅顺序的可按字节寻址的读写语义之外，还支持一组操作（例如，添加、删除、当前大小、利用率）。这些操作与文件系统语义密切相关，其中标识符和数据可通过文件访问，这是 RocksDB 的主要存储后端。通过使用管理文件和目录的文件系统，RocksDB 避免了管理文件范围、缓冲和空闲空间管理。

因此，RocksDB 的存储插件架构和文件系统包装器 API使得适应不同的存储后端成为可能。

ZenFS实现了对 zoned 块设备的支持并集成到 RocksDB 中。ZenFS是为RocksDB设计的，专门用于在分区存储设备（例如ZNS SSD）上高效存储数据的文件系统。它充分利用了RocksDB的LSM树结构及其不可变的、仅顺序压实过程，为分区存储设备提供了一种优化的数据管理方法。ZenFS作为一个存储后端，实现了一个最小化的磁盘文件系统。它使用RocksDB的文件包装器API进行集成，该API是RocksDB访问磁盘数据的统一抽象层。ZenFS适配分区存储设备的访问约束，并将数据放置到特定分区，与设备端分区元数据协作，以减少耐久性相关的复杂性。

具体地，它使用 RocksDB FileSystem接口，将文件放置到原始zoned块设备上的zones中。extent是ZenFS中的最小管理单元，一个文件可以由一个或多个 extents 组成，所有extents 构成的文件可以存储在设备的同一zone（或不同zones）中，但一个extent从不跨越多个zones。 当区域中的所有file extents都无效时，可以重置该zone，然后重新使用以存储新的file extents。(*即：一个文件由于1个或多个extents组成，该文件可以存储在1个和多个zones中，1个extent不可以出现在多个zones中*)

**数据放置：**ZenFS 根据 RocksDB 库提供的**“write lifetime hints”（WLTH）** 将file extents 放置到zones中。 当 WLTH 相似时，ZenFS 总是尝试将file extents 放在相同的 zone 中，来共同定位相似生命周期的数据，与传统块设备上的常规文件系统相比。

**垃圾回收：**在 ZenFS 中，数据垃圾收集仅由 RocksDB 在启动 LSM-tree 表压缩过程时执行。 ZenFS 不执行垃圾回收，ZNS 设备控制器也不执行垃圾回收。(*ZenFS和ZNS SSD 控制器 本身都不提供GC机制。垃圾回收是由于KV Compaction执行的*)

基于ZenFSD的RocksDB能够利用ZNS降低系统写入放大，并且确保文件系统或设备上没有后台垃圾收集，从而提高了吞吐量、尾部延迟和寿命方面的性能。

**ZenFS的主要组件**：

**日志和数据分区的管理**

ZenFS定义了两种类型的分区：日志分区和数据分区。日志分区用于维护文件系统的状态，包括超级块数据结构和WAL。数据分区则用于存储文件内容，它们被映射到一系列连续的区域，这些区域是按顺序写入的。

**超级块的作用与恢复**

超级块是ZenFS从磁盘初始化和恢复状态的关键。它包含了文件系统实例的唯一标识符、魔术值和用户定义的选项。在系统启动或文件系统挂载时，超级块提供了恢复所需的基本信息。

**日志状态的维护与恢复**

ZenFS的日志负责维护超级块和WAL及数据文件到分区的映射。日志状态存储在专用的日志分区上，并使用特定的区域进行更新。恢复日志状态需要确定活动日志区域、读取日志头和应用日志更新。

**数据区域的智能选择与分配**

ZenFS采用“write lifetime hints”（WLTH）算法选择最佳的区域来存储RocksDB数据文件。它考虑了文件的生命周期和区域内存储数据的最大生命周期，以优化数据的放置和设备的写入性能。

**完成数据区域的限制与性能优化**

ZenFS允许用户配置数据区域写满的阈值，即指定区域剩余容量的百分比。这为用户提供了控制文件大小和优化空间利用率的能力。此外，ZenFS通过直接I/O和缓冲写入技术，进一步提高了数据写入的效率。

通过ZenFS架构，RocksDB能够在分区存储设备上实现高效的数据放置，同时保持RocksDB的高性能特性和灵活性。ZenFS的设计考虑了与RocksDB的紧密集成，优化了数据的存储和访问过程，提高了整体系统的性能。



> 我们基于SPDK重构了ZenFS，引入SPDK可以绕过Linux kernel以直接管理ZNS SSD，可以降低延迟；并且提出了一种区域追加友好型WAL解决方案——ZoneWAL；最后，实现了一个基于生命周期的区域分组分配策略，优化了ZenFS的空间占用。

## 问题分析

RocksDB通过ZenFS作为存储后端引入ZNS后，在吞吐量，延迟稳定性，寿命等诸多方面都取得了一定的进展，然而，RocksDB+ZenFS的实现仍存在一些问题和缺点。

### WAL

写前日志（Write-Ahead Logging，WAL）是计算机科学中一种用于确保数据库系统原子性和持久性的技术。是指在应用修改之前将所有修改记录在日志中，为崩溃和事务恢复提供机制。现代文件系统通常使用WAL的变体，例如日志记录，用于元数据更新。

而对于LSM-Tree型存储引擎，使用WAL的具体情形如下：在写入易失性的MemTable时，如果发生电源故障，则无法保留数据。为解决这种由于断电等原因造成的一致性问题，存储引擎往往会在持久化存储设备中维护一个预写日志（WAL）。首先，将put（写入）请求的记录存储在WAL中，然后将其写入到内存的MemTable中。在需要进行数据恢复的时候，按顺序读取所有WAL数据，依次执行对应操作来恢复内存中的memtable。因为，在LSM-Tree中，只有对KV对的最新更改是有效的，WAL中的记录必须按顺序执行。

然而，这种设计可能导致频繁的小写入操作，成为性能瓶颈，因此，WAL对于实现高写入吞吐量至关重要。一方面，因为LSM树通常部署在快速且高度并行的NVMe闪存SSD上，使用NVMe时，SSD会发出内部管理操作，这些操作与LSM树竞争存储资源。这种竞争导致吞吐量不稳定。另一方面，在多线程环境中，还会发生锁争用，导致写入延迟。

解决上述问题的一种流行的方法是批量写入，RocksDB中也是这样做的。该过程动态选择多个具有待处理 put 请求的工作线程中的一个领导线程，收集所有剩余的记录，并让领导线程代表其他工作线程一次性写入它们。然而，这种技术并没有改善（甚至加剧了）尾延迟问题。在收集和写入这些记录的过程中，批处理中的所有记录共享写入时间，可能会增加单个写入的等待时间，尤其是当该条记录较大时。

ZNS虽然能改善了LSM树吞吐量，使得延迟更稳定，但它对LSM树的WAL组件等其他组件造成了重大的写入吞吐量挑战。主要原因是ZNS严格禁止随机写，禁止应用程序同时向同一区域发出写入I/O。因此，对WAL的PUT操作是串行化的，仅有1个PUT可以同时处理，从而限制了WAL的吞吐量。另一方面，批量写入的解决方案本身带来的长尾延迟效应，削减了ZNS带来的延迟降低效果。因此，ZNS没有展现出应有的性能优势。

### Zone Append命令

为了解决写入I/O的吞吐量限制，ZNS引入了一种称为区追加的操作。Zone Append命令允许主机系统将数据附加到指定区域（Zone）的末尾，而无需在写入之前执行擦除操作。这与传统的随机写入方式不同，后者通常需要先擦除闪存单元，然后才能写入新的数据。Append命令最大的特点在于，不会在 I/O 提交请求中指定 LBA，而固态硬盘会在处理时确定 LBA 并在响应中返回地址。也就是说Zone Append命令通常是异步执行的，即应用程序在发送数据追加请求后可以立即继续执行其他操作，而不需要等待数据写入完成。

因此，Zone Append命令有很好的并发性，使其成为WAL的良好替代方案，能有效增强了小文件顺序写入的吞吐量。有希望能够解决高并发小文件（例如上文的WAL）的写入瓶颈问题。然而，使用Append命令仍需克服一个问题，由于Append需要在响应中才返回地址，也就是说，同时到达的写入命令的实际写入顺序是由设备决定的，可能与命令实际发出的顺序相违背，实际存储的是乱序结果。当系统崩溃，需要根据WAL恢复数据时，读取到的是无效的乱序结果。于是，我们通过为每个追加操作添加标识符以及一种新颖的恢复技术来解决WAL乱序写入问题。

##  ZAFS架构概览

我们基于SPDK重构了ZenFS，引入SPDK可以绕过Linux kernel以直接管理ZNS SSD，可以降低延迟；并且提出了一种区域追加友好型WAL解决方案——ZoneWAL；最后，实现了一个基于生命周期的区域分组分配策略，优化了ZenFS的空间占用。

> 图



## Zone-Friendly WAL

在ZAFS中，我们设计了一种适用于ZNS SSD的新型WAL——Zone-Friendly WAL。当然，这种针对WAL的优化设计不仅限于LSM-Tree型的存储引擎。对于其他使用Zone语义存储WAL的数据库，Zone-Friendly WAL都能发挥作用，如SQLite，HBase等等。但是这些数据库对ZNS SSD的支持不够完善，因此，我们将讨论限制在ZNS上的LSM树存储引擎，并使用ZenFS作为参考模型，以解释我们为什么以及如何为ZNS更改现有的WAL设计。后续，我们仍基于RocksDB的场景下进行讨论，我实现Zone-Friendly WAL集成在我们的ZAFS中；最后与ZenFS进行对比测试。

首先，我们的Zone-Friendly WAL设计的出发点，是基于对WAL特性的三点观察：

（1）WALs是写入密集型的，并主要发出小型写入；

（2）WALs仅在数据库恢复期间读取；

（3）WALs通常很小（即，64 MiB ）

WAL的写入操作非常频繁，且写入操作时，由于存储设备对小写入的限制，遇到了性能瓶颈；但是读取操作的发生频率很低，往往在数据库异常关闭，在下次启动时，才会发生数据恢复，进行WAL的读取。因此，我们认为以降低读取性能为代价来增加写入性能是可以接受的。我们的设计目标是提高WAL写入性能与并发性，充分利用区追加指令的峰值性能。消除WAL只能串行写入带来的性能瓶颈，从而提高存储引擎Put操作的效率。

在WAL中，有四个主要操作：**写入，恢复，分配，删除**。

> 图 Zone-Friendly WAL 的字段结构

### **WAL写入**

在ZenFS的实现中，WAL在写入时，PUT请求的数据被写入WAL的末尾，然后触发向Zone写指针进行I/O操作。如果同时发出了另一个PUT操作，则必须等待前一个PUT完成。在 ZNFS 中，为了增加并发性，ZWALs会向区域（的头部？）发出区追加，而不等待区追加完成。这样，多个PUT操作可以同时写入WAL，但是并发的区域追加写会导致乱序，无法保证PUT请求的顺序。

**WAL Header **所以， Zone-Friendly WAL通过在每个WAL写入之前添加一个报头（128位的header）来帮助重排序。我们将WAL数据和头部（黄色）组合成一个WAL entry。这个报头由64位序列号和WAL entry的大小组成。序列号以原子方式增加，并表示绝对数据顺序。每个WAL维护自己的序列号以避免翻转的风险（WAL不太可能是2的64次方页）；条目的大小用于推断后续追加的 WAL 条目（如果有）的位置。为啥要保存entry的大小？如果使用区域追加返回的地址来确定数据存储的位置，这个返回地址是易失的，还需要另一个写操作将此地址存储到存储器中。

**WAL Buffer** 由于追加操作的理想请求大小可能与页面大小不同，并且 KV 对可能明显小于page size。因此，ZWAL 的允许进行缓冲（类似于 ZenFS）。在写入 WAL 时，WAL 首先将数据复制到缓冲区。一旦缓冲区满了或者 WAL 已经同步（例如，fsync、close），我们使用区域追加将数据写入 SSD。

### WAL恢复

WAL 恢复。在 WAL 恢复过程中，LSM 树会顺序扫描其 WAL，并将读取的数据应用到其内存表中。LSM 树每次读取几 KB 数据。然而，ZWAL 存储在 SSD 上是无序的；ZWAL 需要恢复其原始顺序。ZWAL 通过创建从逻辑地址（即偏移量）到物理地址的映射来实现这一点。

在读取时，它首先找到与逻辑地址对应的 WAL 条目。它使用 WAL 报头中的信息找到这个条目。由于序列号是单调递增的，并且数据只追加到 WAL 中，具有更高序列号的 WAL 条目具有严格更高的逻辑地址。具体来说，具有序列号 x 的 WAL 条目的逻辑地址等于序列号为 x-1 的 WAL 条目的逻辑地址加上其大小。例如，具有序列号 1 的 PUT 存储在 PUT 0 的逻辑地址加上 PUT 0 的大小处。在对 WAL 进行读取时，ZWAL 会读取具有相应逻辑地址的条目。

然而，检索WAL头部是具有挑战性的。因为每个WAL条目的大小可能不同，ZWAL无法预先确定WAL头部的位置，除非是第一个请求。因此，ZWAL需要顺序扫描整个WAL，逐个条目地查找WAL头部。一种替代解决方案是仅读取一次WAL并在内存中保持逻辑地址的映射，但这需要与WAL大小成比例的内存。因此，ZWAL采用了一种更高效的方案：使用屏障。ZWAL在预定义的页面间隔（称为Pbarrier）插入屏障。在屏障处，ZWAL同步所有区域追加操作（即等待所有操作完成）。请求在连续的屏障之间进行排序，即屏障之后的追加操作的物理地址严格高于屏障之前的追加操作。在读取过程中，ZWAL首先找到最近的屏障，然后读取两个屏障之间的所有数据。然后，ZWAL根据序列号创建WAL条目的映射，并根据序列号对映射进行排序。通过这种设计，ZWAL每次只需要读取和维护一个页面间隔的映射，从而将I/O和内存占用限制在可配置的上限内。此外，该映射还可以进行缓存，因为读取是顺序的，并且后续读取很可能出现在同一个屏障内。根据设计，预期ZWAL的恢复成本略高于传统WAL，并且与屏障大小成比例（对于排序为O（n log n））

### WAL分配与删除

在ZenFS中，这涉及将一个区域（zone）分配给WAL。这个区域并不专门用于WAL，而是可以与其他LSM-tree组件共享。但是，ZWAL有更严格的限制，它需要为WAL专门分配区域。

这是因为两个原因：首先，为了防止其他LSM-tree组件向与区域追加（zone appends）相同的区域发出写入请求，因为这会导致区域追加需要等待写入完成，从而失去了优势。其次，ZWAL的恢复过程要求所有WAL数据都要连续存储，因此需要专门的区域来确保数据的连续性。

关于WAL的删除（deletion），在ZenFS和ZWAL中都将其视为释放存储资源的操作，与其他数据删除并无不同。由于ZWAL有专用的区域集合，因此可以随时安全地重置（标记为删除的特定区域），而不会影响其他数据。删除可以是主动的（即立即执行）或者是延迟的（即在需要释放存储资源时执行）。



## ZNFS的实现

因为Linux的块层不支持区域追加。因此，ZNFS直接基于SPDK开发，直通ZNS SSD来发起区域追加操作。ZNFS依托spdk/nvme_zns.h中的函数完成对ZNS SSD的高效交互。

### SPDK技术

在第二章“相关技术基础”部分，我们已经讨论了Linux I/O栈的冗杂低效已经成为存储系统的瓶颈。为了解决这个问题。Linux I/O栈涉及多个层次的抽象和处理，包括用户空间和内核空间之间的交互、设备驱动程序、文件系统、块设备管理等，并不能在全场景下保证很高的效率，尤其是在高性能存储系统中。在这种情况下，SPDK（Storage Performance Development Kit）技术的出现为解决高性能存储系统的设计与实现提供了一种全新的思路。SPDK技术的核心理念是尽可能地减少软件层面对I/O操作的干预，通过将数据的传输和处理任务尽可能地移到用户空间，以最小化对内核的依赖性。这种基于用户空间的I/O处理方式可以显著降低系统中断的频率，减少了CPU的上下文切换开销，并且提供了更直接、更高效的I/O通道。

具体地，SPDK是基于DPDK（Data Plane Development Kit）的。DPDK是一个开源项目，旨在提供高性能的数据包处理框架，特别适用于网络和存储领域的应用。SPDK利用了DPDK提供的高性能数据包处理能力，并在其基础上构建了一个专注于存储性能优化的软件栈。在SPDK技术中，采用了一系列优化策略，包括零拷贝数据传输、基于事件驱动的异步I/O模型、与硬件的紧密协作等，以进一步提升存储系统的性能和吞吐量。此外，SPDK技术还提供了丰富的API和工具集，方便开发人员快速构建高性能、低延迟的存储应用程序。总的来说，SPDK技术在存储领域的应用前景广阔，为构建高效、可扩展的存储系统提供了一种创新的解决方案。

**SPDK_NVMe**

在SPDK中，针对NVMe（Non-Volatile Memory Express）设备的优化是其关键特点之一，旨在充分发挥NVMe设备的高性能和低延迟特性，从而提供高效的存储解决方案。NVMe是一种专为固态存储设备设计的接口协议，相较于传统的SATA和SAS接口，具有更高的带宽和更低的延迟。SPDK在NVMe方面的优化体现在以下几个关键方面：

首先，SPDK提供了针对NVMe设备的用户态驱动程序，使得应用程序可以直接与NVMe设备进行交互，无需经过操作系统内核的介入。这种用户态驱动程序的设计可以显著降低存储操作的延迟，并提高系统的响应速度。

其次，SPDK通过一组API实现了对NVMe命名空间的管理。NVMe协议允许将物理存储空间划分为多个逻辑分区，即命名空间（Namespace）。SPDK提供了丰富的命名空间管理功能，包括命名空间的创建、删除和查询等操作，使得用户可以灵活地管理存储空间。

第三，SPDK针对NVMe命令的处理实现了异步事件驱动的机制。这意味着应用程序可以并行发送和处理多个NVMe命令，而不会阻塞主线程，从而提高了存储操作的吞吐量和并发性能。

最后，NVMe设备支持多个命令队列，SPDK充分利用了这一特性，实现了多队列并发处理机制。这种设计可以最大限度地发挥NVMe设备的并行性能，进一步提升了存储操作的并行处理能力。

综上所述，SPDK在NVMe方面的优化设计使得其能够充分利用NVMe设备的性能特性，为用户提供了高效、低延迟的存储解决方案，从而满足了现代数据中心和云计算环境对高性能存储的需求。

**SPDK_NVMe_ZNS**

NVMe协议规范已经定义了对ZNS的支持，包括命令集和数据传输方式等方面的规范。SPDK作为一个存储性能优化的软件栈，在支持NVMe设备时，直接利用了NVMe协议规范中对ZNS的定义，将其集成到SPDK中，从而实现了对NVMe ZNS SSD的支持。这是本文工作的关键支撑之一，ZNFS依托次工具库完成对ZNS SSD的高效交互，整个代码实现中出现调用该库接口300余次。

在SPDK（Storage Performance Development Kit）中，针对Zoned Namespace（ZNS）的典型函数主要用于处理与zone相关的操作，例如读取、写入、重置zone等。以下是一些典型的SPDK中与ZNS相关的函数及其详细说明：

1. spdk_nvme_zns_report_zones() 

   功能：这个函数用于获取特定命名空间中的zone报告。它可以列出所有的zones以及它们的属性，包括每个zone的状态、大小和写入指针等。

   参数：需要提供命名空间（ns）、队列对（qpair）、用于存储报告的缓冲区（buf）、缓冲区大小（bufsize）、起始zone的LBA（start_lba）、要报告的zone数量（num_zones）、报告类型（report_type），以及完成回调函数（cpl_cb_fn）。

2. spdk_nvme_zns_reset_zone() 

   功能：此函数用于重置一个zone，使其回到可写状态。这通常在zone完全写满之后进行。

   参数：包括命名空间（ns）、队列对（qpair）、zone的起始LBA（start_lba）、是否重置所有zones的标志（reset_all_zones）、完成回调函数（cpl_cb_fn）和回调参数（arg）。

3. spdk_nvme_zns_zone_append() 

   功能：这个函数用于向zone中追加数据。在ZNS设备上，数据通常是以zone为单位进行写入的，而追加操作是zone写入的基本形式。

   参数：需要指定命名空间（ns）、队列对（qpair）、数据缓冲区（buf）、zone的起始LBA（zslba）、要写入的LBA数量（num_lbas）、完成回调函数（cpl_cb_fn）、回调参数（arg）和附加的标志（flags）。

4. spdk_nvme_ns_cmd_read() 

   功能：虽然这个函数不是专门用于ZNS，但它可以用于读取ZNS设备中的数据。它负责从指定的命名空间和LBA位置读取数据到提供的缓冲区。

   参数：包括命名空间（ns）、队列对（qpair）、数据缓冲区（buf）、起始LBA（lba）、要读取的LBA数量（lba_count）、完成回调函数（cpl_cb_fn）和回调参数（arg）。

5. spdk_nvme_zns_close_zone() 

   功能：此函数用于关闭一个zone，使其变为不可写状态。关闭zone是一个重要的步骤，它允许垃圾回收机制后续回收并重用zone。

   参数：包括命名空间（ns）、队列对（qpair）、zone的ID（zone_id）和完成回调（cpl_cb_fn）。

6. spdk_nvme_zns_zone_appendv() 

   功能：这是一个向量变体的zone append函数，允许一次性发送多个数据块到zone中。这可以提高写入效率，因为它减少了单个write命令的数量。

   参数：与spdk_nvme_zns_zone_append()类似，但接受额外的参数来处理多个数据块。

7. spdk_nvme_zns_open_zone

   功能：打开zone

   参数：命名空间句柄，队列对，zone的ID等。

8. spdk_nvme_zns_finish_zone

   功能：完成zone

   参数：命名空间句柄，队列对，zone的ID等。

9. spdk_nvme_zns_get_zone_info

   功能：获取指定zone信息

   参数：命名空间句柄，zone索引，用于存储zone信息的结构体等。

10. spdk_nvme_zmalloc

    功能：分配一块对DMA传输安全的内存，并初始化为零。

    参数:

    - `size`：要分配的内存大小。
    - `align`：内存对齐的字节数，通常为64字节。
    - `ctx`：分配上下文，可用于跟踪或状态管理。
    - `socket_id`：指定内存应该分配在哪个CPU插槽的内存上。
    - `flags`：指定分配特性的标志，如`SPDK_MALLOC_DMA`。

    `spdk_nvme_zmalloc` 是SPDK中用于分配内存的函数，它确保了分配的内存适用于DMA操作，这意味着NVMe设备可以直接通过DMA读取或写入这块内存。该函数还会将分配的内存初始化为零，这对于初始化缓冲区或避免遗留数据非常重要。使用`spdk_nvme_zmalloc` 分配的内存通常需要与`spdk_dma_free` 配对使用来释放，确保内存被正确管理，避免内存泄漏。

### 独立的WAL Zone

原本ZenFS的设计中，Zone分为两类，即元数据Zone和数据Zone，并没有对RocksDB的其他组件产生的数据作单独隔离。为了优化WAL的写入，

因此，为了将数据与WAL区域分离开，作者在ZenFS的元数据和数据区域之间预留了一组专用的区域，用于存储WAL。在示意图中，用“W”表示WAL，用“M”表示元数据，用“D”表示数据。WAL区域的数量可以在格式化时进行配置。

### 与RocksDB的兼容性

为了支持ZWALs在RocksDB中的使用，我们修改了一个函数。在删除WAL时，RocksDB首先将WAL移动到归档目录，并在稍后的时间点才物理删除它们。但由于WAL使用的区域数量有限，这可能会导致空间不足的错误，因此我们强制RocksDB立即删除旧的WAL。

RocksDB提供了各种WAL过滤器，这些过滤器在ZNFS的WAL上有同样的功能，因此，仍可以将现有的WAL过滤器直接应用于ZNFS的WAL。

### 代码结构简介

保持了原有ZenFS的目录结构。

主要分为三个文件：

1. **第一个文件**（`io_zenfs.h`）：   - 它定义了用于 RocksDB 的 ZenFS 插件中的 I/O 相关的类和接口，这是一个专门为 Zoned Namespaces (ZNS) 设备设计的文件系统。   - 它包含了如 `ZoneExtent` 和 `ZoneFile` 等类的定义，这些类表示文件系统中的区域和文件，并且负责编码和解码数据，以及处理数据的读写。   - 还包括一些全局变量和 `extern` 声明，用于跟踪写日志和与底层环境交互。 

   组件：

   1. **ZenFS 类**: 代表文件系统本身，包含挂载、从元数据日志中恢复、创建文件系统、列出文件系统、获取区域快照等方法。
   2. **ZoneFile 类**: 表示文件系统中的文件。
   3. **ZenMetaLog 类**: 处理文件系统的元数据日志记录。
   4. **Superblock 类**: 表示文件系统的超级块。
   5. **FactoryFunc**: 一个工厂函数，根据 URI 创建文件系统的实例。

   功能：

   1. **挂载**: `Mount` 函数通过从最新的有效元数据区域中恢复来挂载文件系统。
   2. **恢复**: `RecoverFrom` 函数从元数据日志中恢复文件系统。
   3. **创建文件系统**: `MkFS` 函数创建具有指定辅助文件系统路径和完成阈值的新文件系统。
   4. **列出文件系统**: `ListZenFileSystems` 函数列出现有的 ZenFS 文件系统。
   5. **区域快照**: `GetZoneSnapshot` 和 `GetZoneFileSnapshot` 等函数获取区域和区域文件的快照。

2. **第二个文件**（`io_zenfs.cc`）：   - 它包含了第一个文件中声明的类和接口的具体实现。   - 主要实现了 `ZoneExtent` 和 `ZoneFile` 类的方法，如数据编码解码、JSON 序列化、以及与 Zoned Block Device (ZBD) 进行读写等操作。   - 还实现了一些用于管理文件和文件区域的功能，如合并文件更新、文件重命名等。 

3. **第三个文件**（`zbd_zenfs.cc`）：   - 此文件实现了 Zoned Block Device (ZBD) 的相关操作，它提供了管理 ZNS 设备区域的方法。   - 它定义了 `ZonedBlockDevice` 类，这个类负责打开和关闭设备、分配和释放区域、以及管理区域的状态等。   - 文件中包括了一些底层的 NVMe ZNS（Non-Volatile Memory express Zoned Namespaces）操作，例如区域重置、追加写、同步等。   - 也有一些 SPDK（Storage Performance Development Kit）相关的代码，这些代码允许直接与 NVMe 设备进行交互，避免操作系统的存储堆栈，从而实现更高的性能。

> 数据放置策略，就是ZoneKV，如果内容够了感觉可以不写了

![image-20240513033322894](%E6%AF%95%E8%AE%BE.assets/image-20240513033322894.png)



### 基于生命周期的数据放置策略

1. **获取块寿命**：计算从最后一次写入到当前的时间差，以此作为块寿命的估计。
2. **写入类型判断**：根据当前写入操作是用户写入还是垃圾回收（GC）写入，执行相应的更新函数。
3. **初始块热度值计算**：基于用户写入频率和GC写入频率，以及一个默认热度值C，计算出初始的块热度值。
4. **热度值界限检查**：确保计算出的块热度值不会低于0或超过分区最大数量N。
5. **热度值确认**：利用块寿命和判定阈值对热度值进行最终确认，如果块热度值低于默认热度值C，并且块寿命超过了该热度值对应的分区寿命平均值，则将热度值增加1。 此外，我们还设计了设备管理模块和元数据管理模块，以及垃圾回收模块。设备管理模块负责ZNS SSD的分区管理，包括分区的状态转换和数据写入方式。元数据管理模块则采用了页级映射（L2P）来维护逻辑块和物理地址之间的映射关系，以支持更细粒度的数据管理。 垃圾回收模块采用了优化后的成本-效益算法（CBE），该算法通过考虑待回收分区的无效数据占比和存在时间，来计算每个分区的收益值，并选择收益值最高的分区进行回收。CBE算法能够有效解决传统CB算法中的误判问题和负收益现象，从而提高垃圾回收的效率。 通过实验评估，我们证明了BHB-DP策略在提高写入性能、降低尾部延迟以及减少垃圾回收写入量方面的有效性。BHB-DP策略为ZNS SSD上的数据管理提供了一种新的优化方法，对于提高存储系统的性能具有重要的实际应用价值。

> 数据放置策略，就是ZoneKV，如果内容够了感觉可以不写了

# 实验结果分析

## 模拟设备与真实设备的对比

## FIO基准测试

### 设备信息

> 查看参数的一些方法

```
sudo nvme id-ctrl /dev/nvme0
```

查看，NVME Identify Controller

```bash
sudo nvme zns id-ns /dev/nvme0n1                                                                                     
ZNS Command Set Identify Namespace:                                                                                    
zoc     : 0                                                                                                            
ozcs    : 2                                                                                                            
mar     : 0xf                                                                                                          
mor     : 0xf                                                                                                          
rrl     : 3600                                                                                                         
frl     : 3600                                                                                                         
rrl1    : 7200                                                                                                         
rrl2    : 14400                                                                                                        
rrl3    : 21600                                                                                                        
frl1    : 3600                                                                                                         
frl2    : 3600                                                                                                         
frl3    : 3600                                                                                                         
lbafe  0: zsze:0x200000 zdes:2 (in use)                                                                                
lbafe  1: zsze:0x200000 zdes:2                                                                                         
lbafe  2: zsze:0x200000 zdes: 2 

```



```
lsblk -d -o NAME,SIZE,PHY-SEC,LOG-SEC,ZONED /dev/nvme0n1                                   
NAME     SIZE PHY-SEC LOG-SEC ZONED                                                                               
nvme0n1 11.4T    4096    4096 host-managed 
```

这个路径下有SSD的配置信息:`/sys/block/nvme1n1/queue/...`

```bash
for file in /sys/block/nvme0n1/queue/*; do echo "$file: $(cat $file)"; done

/sys/block/nvme0n1/queue/add_random: 0                                                                                                                    
/sys/block/nvme0n1/queue/chunk_sectors: 16777216                                                                                                            
/sys/block/nvme0n1/queue/dax: 0                                                                                                                             
/sys/block/nvme0n1/queue/discard_granularity: 4096                                                                                                          
/sys/block/nvme0n1/queue/discard_max_bytes: 2199023255040                                                                                                   
/sys/block/nvme0n1/queue/discard_max_hw_bytes: 2199023255040                                                                                                
/sys/block/nvme0n1/queue/discard_zeroes_data: 0                                                                                                             
/sys/block/nvme0n1/queue/fua: 0                                                                                                                             
/sys/block/nvme0n1/queue/hw_sector_size: 4096                                                                                                               
/sys/block/nvme0n1/queue/io_poll: 0                                                                                                                         
/sys/block/nvme0n1/queue/io_poll_delay: -1                                                                                                                  
/sys/block/nvme0n1/queue/iostats: 1                                                                                                                         
/sys/block/nvme0n1/queue/io_timeout: 30000                                                                                                                  
/sys/block/nvme0n1/queue/logical_block_size: 4096                                                                                                           
/sys/block/nvme0n1/queue/max_active_zones: 16                                                                                                               
/sys/block/nvme0n1/queue/max_discard_segments: 256                                                                                                          
/sys/block/nvme0n1/queue/max_hw_sectors_kb: 256                                                                                                             
/sys/block/nvme0n1/queue/max_integrity_segments: 0                                                                                                          
/sys/block/nvme0n1/queue/max_open_zones: 16                                                                                                                 
/sys/block/nvme0n1/queue/max_sectors_kb: 256                                                                                                                
/sys/block/nvme0n1/queue/max_segments: 65                                                                                                                   
/sys/block/nvme0n1/queue/max_segment_size: 4294967295                                                                                                       
/sys/block/nvme0n1/queue/minimum_io_size: 4096                                                                                                              
/sys/block/nvme0n1/queue/nomerges: 0                                                                                                                        
/sys/block/nvme0n1/queue/nr_requests: 1023                                                                                                                  
/sys/block/nvme0n1/queue/nr_zones: 1465                                                                                                                     
/sys/block/nvme0n1/queue/optimal_io_size: 0                                                                                                                 
/sys/block/nvme0n1/queue/physical_block_size: 4096                                                                                                          
/sys/block/nvme0n1/queue/read_ahead_kb: 128                                                                                                                 
/sys/block/nvme0n1/queue/rotational: 0                                                                                                                      
/sys/block/nvme0n1/queue/rq_affinity: 1                                                                                                                     
/sys/block/nvme0n1/queue/scheduler: [none] mq-deadline                                                                                                      
/sys/block/nvme0n1/queue/stable_writes: 0                                                                                                                   
/sys/block/nvme0n1/queue/virt_boundary_mask: 4095                                                                                                           
/sys/block/nvme0n1/queue/wbt_lat_usec: 2000                                                                                                                 
/sys/block/nvme0n1/queue/write_cache: write through                                                                                                         
/sys/block/nvme0n1/queue/write_same_max_bytes: 0                                                                                                            
/sys/block/nvme0n1/queue/write_zeroes_max_bytes: 0                                                                                                          
/sys/block/nvme0n1/queue/zone_append_max_bytes: 262144                                                                                                      
/sys/block/nvme0n1/queue/zoned: host-managed                                                                                                                
/sys/block/nvme0n1/queue/zone_write_granularity: 4096   
```







```

sudo nvme zns report-zones /dev/nvme0n1 -d 10

nr_zones: 1465                                                                                                             
SLBA: 0          WP: 0          Cap: 0x145800   State: 0x10 Type: 0x2  Attrs: 0    AttrsInfo: 0                            
SLBA: 0x200000   WP: 0x200000   Cap: 0x145800   State: 0x10 Type: 0x2  Attrs: 0    AttrsInfo: 0 
```

一个Zone实际占用2GB



以下是您提供的 `/sys/block/nvme0n1/queue/` 目录下文件的参数、它们的值以及意义的整理表格：

| 参数                       | 值                 | 意义                                                         |
| -------------------------- | ------------------ | ------------------------------------------------------------ |
| add_random                 | 0                  | 不允许在区域中随机添加数据。                                 |
| **chunk_sectors**          | 16777216           | 1chunk =  16777216 sectors，设备的 chunk 的大小，以扇区为单位。 |
| dax                        | 0                  | 设备未启用 DAX 模式，即数据不是直接映射到文件系统。          |
| discard_granularity        | 4096               | 字节，擦除操作(Trim)的最小粒度为4KB                          |
| discard_max_bytes          | 2199023255040      | 可以一次性丢弃的最大字节数，约为 2TB                         |
| discard_max_hw_bytes       | 2199023255040      | 硬件支持的一次性最大擦除字节数，同上                         |
| discard_zeroes_data        | 0                  | 不会自动将丢弃的数据区域清零。                               |
| fua                        | 0                  | 写入操作不会强制硬件进行数据刷新。                           |
| **hw_sector_size**         | 4096               | 硬件扇区大小，以字节为单位。                                 |
| io_poll                    | 0                  | 不使用轮询模式进行 I/O 操作。？                              |
| io_poll_delay              | -1                 | 轮询模式下的延迟时间，-1 表示不延迟。？                      |
| iostats                    | 1                  | 启用 I/O 统计信息。                                          |
| io_timeout                 | 30000              | I/O 超时时间，以毫秒为单位。                                 |
| **logical_block_size**     | 4096               | 逻辑块大小，以字节为单位。                                   |
| **max_active_zones**       | 16                 | 可以同时处于打开状态的最大区域数。                           |
| max_discard_segments       | 256                | 单次丢弃操作中可以包含的最大段数。                           |
| max_hw_sectors_kb          | 256                | 硬件队列可以处理的最大扇区数，256 * 4 KB= 1MB                |
| max_integrity_segments     | 0                  | 最大的完整性校验段数，0 表示不使用。                         |
| **max_open_zones**         | 16                 | 可以同时打开的最大区域数。                                   |
| max_sectors_kb             | 256                | 单次 I/O 操作可以处理的最大扇区数，以KB为单位。              |
| max_segments               | 65                 | 单次 I/O 操作可以处理的最大段数。？                          |
| max_segment_size           | 4294967295         | 单个 I/O 段的最大字节数。                                    |
| minimum_io_size            | 4096               | 最小的 I/O 操作大小，以字节为单位。                          |
| nomerges                   | 0                  | 内核合并 I/O 请求以提高效率，不允许？                        |
| nr_requests                | 1023               | 可以同时处理的请求数。                                       |
| **nr_zones**               | 1465               | 设备上的区域总数。                                           |
| optimal_io_size            | 0                  | 最佳 I/O 操作大小，0 表示无特定大小。                        |
| physical_block_size        | 4096               | 物理块大小，以字节为单位。                                   |
| read_ahead_kb              | 128                | 预读操作的字节数。                                           |
| rotational                 | 0                  | 设备为非旋转介质（例如 SSD）。                               |
| rq_affinity                | 1                  | 请求亲和性，1 表示启用。                                     |
| scheduler                  | [none] mq-deadline | 当前使用的 I/O 调度策略。                                    |
| stable_writes              | 0                  | 不保证写入操作的数据在掉电情况下的稳定性。                   |
| virt_boundary_mask         | 4095               | 虚拟地址边界掩码，用于限制 I/O 请求的地址范围。              |
| wbt_lat_usec               | 2000               | 写回缓冲区（Write-Back Tuning）延迟时间，以微秒为单位。      |
| write_cache                | write through      | 写入缓存策略为直写模式，不缓存数据。                         |
| write_same_max_bytes       | 0                  | 最大的写同样操作字节数，0 表示不使用。                       |
| write_zeroes_max_bytes     | 0                  | 最大的写零操作字节数，0 表示不使用。                         |
| **zone_append_max_bytes**  | 262144             | 每个区域追加模式下可以写入的最大字节数。                     |
| **zoned**                  | host-managed       | 区域管理方式为主机管理。                                     |
| **zone_write_granularity** | 4096               | 区域写入粒度，以字节为单位。                                 |

这些参数提供了对 NVMe 设备的 I/O 队列特性的深入了解，包括其性能特点、支持的操作类型以及当前的配置状态。通过调整这些参数（有些是可写的），系统管理员可以优化设备的性能和行为以适应特定的工作负载。



测试指标：

bs = 4K 16K 64K 128K 256K

iodepth= 1-4 低 8-32中 32-128高     1, 4, 8, 16, 32, 64, 128



> 不同io_engine的介绍:
>
> 1. **sync**：这是一个简单的 I/O 引擎，它在每个 I/O 操作后都会同步数据。这种引擎不依赖于任何特定的 Linux 内核特性，因此它几乎可以在任何文件系统上运行。但是，它的性能较低，因为它不允许任何形式的 I/O 调度。
> 2. **psync**：与 sync 类似，但使用 POSIX 风格的异步 I/O。它在每个 I/O 操作后执行 fsync，以确保数据的完整性。
> 3. **libaio**：这个 I/O 引擎使用 Linux 内核的 `io_submit` 系统调用，它支持异步 I/O。`libaio` 是 Linux 本地异步 I/O 的一个特性，可以提供比 sync 和 psync 更好的性能。
> 4. **posixaio**：这个引擎使用 POSIX 异步 I/O 接口。它与 libaio 类似，但使用不同的系统调用。
> 5. **sg**：这个引擎使用 SCSI 通用命令（sg）ioctl 接口直接向 SCSI 设备发送命令。它可以用来测试 SCSI 设备的性能。
> 6. **rbd**：这个引擎用于通过 RADOS Block Device（RBD）访问 Ceph 存储。它使用 librbd 库来执行 I/O 操作。
> 7. **io_uring**：这是一个较新的 I/O 引擎，它利用了 Linux 内核的 `io_uring` 特性，提供了非常高的性能和低延迟的 I/O 操作。
> 8. **null**：这个引擎不会执行任何实际的 I/O 操作，它用于测试 FIO 本身的性能，而不受磁盘或文件系统的影响。
> 9. **mmap**：这个引擎使用内存映射文件进行 I/O 操作。它适用于测试文件系统的性能，特别是对于那些支持 mmap 的文件系统。
> 10. **cpuio**：这个引擎不涉及任何实际的 I/O 硬件操作，而是在用户空间模拟 I/O 操作，用于压力测试 CPU。



> 记得重置区域

```
blkzone reset /dev/nvme0n1
```



### 单ZONE测试

#### 单Zone，单线程（每个线程只开一个Zone）

```ini
[global]
ioengine=sync           # 使用同步I/O引擎 
direct=1                 # 启用直接I/O
zonemode=zbd             # 使用Zoned Block Device模式
bs=64k                   # 块大小为64KB     4k/16k/64k/128k/256k
numjobs=1                # 使用1个并行作业
offset_increment=1z      # 每个作业的偏移量增加1个zone
size=1z                  # 每个作业处理1个zone大小的数据
time_based=0             # 非基于时间运行
runtime=60s              # 每个测试运行60秒
group_reporting=1        # 汇总报告

[seqwrite]
filename=/dev/nvme0n1    # 目标设备
rw=write                 # 顺序写入测试
job_max_open_zones=1     # 每个作业同时打开的最大区域数
```

`ioengine=psync` 表示使用的是 psync I/O 引擎。psync 是 FIO 提供的一种 I/O 引擎，它执行同步 I/O 操作，即数据写入操作是同步进行的。在 psync 引擎中，每次写入操作都会等待数据被完全写入后才返回，因此它是一种比较简单的 I/O 操作方式。

> 单Zone 单线程。ioengine=psync 

bs=4k，ioengine=psync 

```
Run status group 0 (all jobs):
  WRITE: bw=298MiB/s (313MB/s), 298MiB/s-298MiB/s (313MB/s-313MB/s), io=17.5GiB (18.8GB), run=60001-60001msec

Disk stats (read/write):
  nvme0n1: ios=48/4575748, merge=0/0, ticks=2/49823, in_queue=49825, util=99.89%
```

bs=16k

```
Run status group 0 (all jobs):
  WRITE: bw=663MiB/s (695MB/s), 663MiB/s-663MiB/s (695MB/s-695MB/s), io=38.9GiB (41.7GB), run=60001-60001msec

Disk stats (read/write):
  nvme0n1: ios=48/2542174, merge=0/0, ticks=1/53289, in_queue=53290, util=99.88%
```

bs=16k

```
Run status group 0 (all jobs):
  WRITE: bw=1111MiB/s (1165MB/s), 1111MiB/s-1111MiB/s (1165MB/s-1165MB/s), io=10.9GiB (11.7GB), run=10001-10001msec

Disk stats (read/write):
  nvme0n1: ios=48/351999, merge=0/0, ticks=1/8786, in_queue=8786, util=99.14%
```

**bs=64k**

```
Run status group 0 (all jobs):
  WRITE: bw=1738MiB/s (1823MB/s), 1738MiB/s-1738MiB/s (1823MB/s-1823MB/s), io=102GiB (109GB), run=60001-60001msec

Disk stats (read/write):
  nvme0n1: ios=48/1666475, merge=0/0, ticks=2/53836, in_queue=53838, util=99.89%
```

bs=128k

```
Run status group 0 (all jobs):
  WRITE: bw=2285MiB/s (2396MB/s), 2285MiB/s-2285MiB/s (2396MB/s-2396MB/s), io=134GiB (144GB), run=60001-60001msec

Disk stats (read/write):
  nvme0n1: ios=48/1095009, merge=0/0, ticks=2/53764, in_queue=53765, util=99.89%
```

bs=256k

```
Run status group 0 (all jobs):
  WRITE: bw=2500MiB/s (2622MB/s), 2500MiB/s-2500MiB/s (2622MB/s-2622MB/s), io=73.3GiB (78.7GB), run=30001-30001msec

Disk stats (read/writie):
  nvme0n1: ios=48/299012, merge=0/0, ticks=1/27422, in_queue=27423, util=99.74%
```

bs=512k 报错



> 增加io_depth，bs=64k，ioengine=psync 
>
> io_depth=4，bs=64k，除了最终结果的in_queue=27163降低了，其他没变化
>
> io_depth=4，bs=128k，同上。
>
> io_depth=16，bs=128k，同上。
>
> 切换ioengine=sync，没变化。
>
> 单Zone，单线程，同步IO，增加io_depth无意义。



> 换异步IO引擎，ioengine=libaio，速度降低了？

bs=64k，io_depth=1，ioengine=libaio

```
Run status group 0 (all jobs):
  WRITE: bw=1162MiB/s (1219MB/s), 1162MiB/s-1162MiB/s (1219MB/s-1219MB/s), io=34.1GiB (36.6GB), run=30001-30001msec

Disk stats (read/write):
  nvme0n1: ios=48/556011, merge=0/0, ticks=2/22286, in_queue=22288, util=99.74%

```

增加io_depth后报错。









#### 多线程

> 单Zone，多线程，但io_depth=1，ioengine=sync
>
> 但需要注意的是，Zoned Block Device 模式下，通常情况下一个 zone 只能由一个主机进行写入。在多个主机并发写入同一个 zone 的情况下，可能会导致数据一致性问题。

bs=64k，numjobs=2 ，iodepth=1  ， ioengine=libaio ，job_max_open_zones=1

```
Run status group 0 (all jobs):                                                                                   
WRITE: bw=2250MiB/s (2359MB/s), 2250MiB/s-2250MiB/s (2359MB/s-2359MB/s), io=65.9GiB (70.8GB), run=30001-30001msec                                                                                         	
Disk stats (read/write):                                                                
  nvme0n1: ios=99/1076181, merge=0/0, ticks=3/44718, in_queue=44721, util=99.78% 
```

bs=64k，numjobs=4 ，iodepth=1，**（基本跑满了？）**

```
Run status group 0 (all jobs):
  WRITE: bw=5226MiB/s (5479MB/s), 5226MiB/s-5226MiB/s (5479MB/s-5479MB/s), io=51.0GiB (54.8GB), run=10001-10001msec

Disk stats (read/write):
  nvme0n1: ios=96/827764, merge=0/0, ticks=1/36243, in_queue=36245, util=99.14%
```

bs=64k，numjobs=8 ，iodepth=1

```
Run status group 0 (all jobs):
  WRITE: bw=5299MiB/s (5556MB/s), 5299MiB/s-5299MiB/s (5556MB/s-5556MB/s), io=51.8GiB (55.6GB), run=10006-10006msec

Disk stats (read/write):
  nvme0n1: ios=96/839455, merge=0/0, ticks=2/75609, in_queue=75610, util=99.13%
```

bs=64k，numjobs=16 ，iodepth=1

```
Run status group 0 (all jobs):
  WRITE: bw=5232MiB/s (5486MB/s), 5232MiB/s-5232MiB/s (5486MB/s-5486MB/s), io=51.2GiB (54.9GB), run=10016-10016msec

Disk stats (read/write):
  nvme0n1: ios=96/828894, merge=0/0, ticks=1/153992, in_queue=153993, util=99.14%
```

bs=64k，numjobs=4，iodepth=4

```
Run status group 0 (all jobs):
  WRITE: bw=5213MiB/s (5466MB/s), 5213MiB/s-5213MiB/s (5466MB/s-5466MB/s), io=50.9GiB (54.7GB), run=10001-10001msec

Disk stats (read/write):
  nvme0n1: ios=96/826017, merge=0/0, ticks=1/36313, in_queue=36315, util=99.14%
```



> 貌似bs=32k * numjobs=4  = 256 KB就能跑满?

bs=32k，numjobs=8，iodepth=1  // 突然意识到 offset_increment=1z 可能会覆写， 改成50z 

**（新高：5301MiB/s）**

```
Run status group 0 (all jobs):
  WRITE: bw=5301MiB/s (5558MB/s), 5301MiB/s-5301MiB/s (5558MB/s-5558MB/s), io=51.8GiB (55.6GB), run=10003-10003msec

Disk stats (read/write):
  nvme0n1: ios=96/1678805, merge=0/0, ticks=1/73766, in_queue=73767, util=99.22%
```

bs=32k，numjobs=16，iodepth=1   //  继续增大线程数，性能下降

```
Run status group 0 (all jobs):
  WRITE: bw=5250MiB/s (5505MB/s), 5250MiB/s-5250MiB/s (5505MB/s-5505MB/s), io=51.3GiB (55.1GB), run=10005-10005msec

Disk stats (read/write):
  nvme0n1: ios=96/1661327, merge=0/0, ticks=1/135908, in_queue=135910, util=99.10%
```

> 切成libaio 异步IO会变差，跑不满？

```
Run status group 0 (all jobs):
  WRITE: bw=4491MiB/s (4709MB/s), 4491MiB/s-4491MiB/s (4709MB/s-4709MB/s), io=43.9GiB (47.1GB), run=10001-10001msec
Disk stats (read/write):
  nvme0n1: ios=96/1422095, merge=0/0, ticks=1/60295, in_queue=60296, util=99.15%
```



> 貌似bs=32k * numjobs=4  = 256 KB就能跑满? 也不是，线程数太少不能充分激活Zone？

bs=128k，numjobs=2，iodepth=1

```
Run status group 0 (all jobs):             
  WRITE: bw=4086MiB/s (4285MB/s), 4086MiB/s-4086MiB/s (4285MB/s-4285MB/s), io=39.9GiB (42.8GB), run=10001-10001msec
Disk stats (read/write):                  
  nvme0n1: ios=96/323532, merge=0/0, ticks=1/17982, in_queue=17983, util=99.14%    
```

bs=128k，numjobs=4，iodepth=1

```
Run status group 0 (all jobs):
  WRITE: bw=5172MiB/s (5423MB/s), 5172MiB/s-5172MiB/s (5423MB/s-5423MB/s), io=50.5GiB (54.2GB), run=10002-10002msec

Disk stats (read/write):
  nvme0n1: ios=96/409630, merge=0/0, ticks=2/37306, in_queue=37308, util=99.17%
```

> 继续增大线程数
>
> bs=128k，numjobs=8，iodepth=1
>
> bs=128k，numjobs=16，iodepth=1 
>
> 都是5200MiB/s



>降低块大小,看看什么时候跑不满，

bs=16k，numjobs=16

```
Run status group 0 (all jobs):                                                                                   
  WRITE: bw=5206MiB/s (5458MB/s), 5206MiB/s-5206MiB/s (5458MB/s-5458MB/s), io=50.9GiB (54.6GB), run=10005-10005mses                                                                                            
Disk stats (read/write):     
  nvme0n1: ios=96/3294062, merge=0/0, ticks=1/148318, in_queue=148319, util=99.14%  
```

bs=8k，numjobs=16

```
Run status group 0 (all jobs):
  WRITE: bw=5077MiB/s (5324MB/s), 5077MiB/s-5077MiB/s (5324MB/s-5324MB/s), io=49.6GiB (53.2GB), run=10002-10002msec

Disk stats (read/write):
  nvme0n1: ios=96/6427214, merge=0/0, ticks=1/139764, in_queue=139765, util=99.11%
```

bs=4k，numjobs=16，iodepth=1 **跑不满，4K SEQ W IOPS = 800K**

```
Run status group 0 (all jobs):
  WRITE: bw=3089MiB/s (3239MB/s), 3089MiB/s-3089MiB/s (3239MB/s-3239MB/s), io=30.2GiB (32.4GB), run=10001-10001msec

Disk stats (read/write):
  nvme0n1: ios=96/7822738, merge=0/0, ticks=1/135228, in_queue=135230, util=99.15%
```

bs=4k，numjobs=32，iodepth=1 **跑不满，线程数大于16对ZNS没意义**  

```
Run status group 0 (all jobs):
  WRITE: bw=3081MiB/s (3230MB/s), 3081MiB/s-3081MiB/s (3230MB/s-3230MB/s), io=30.1GiB (32.3GB), run=10002-10002msec

Disk stats (read/write):
  nvme0n1: ios=199/7888474, merge=0/0, ticks=4/135274, in_queue=135277, util=99.00%
```

注：报错?没ZONESIZE

> 4K写入 3100已是极限？增加iodepth
>
> bs=4k，numjobs=32，iodepth=16  无变化。



> 换引擎ioengine=io_uring  。另外，好像只有sync写入时，iodepth可以不等于1

bs=4k ，io_depth=16









### 顺序读取测试

1. **准备写入数据**:

   ```bahs
   fio --ioengine=psync --direct=1 --filename=/dev/nvme0n1 --rw=write --bs=128k --group_reporting --zonemode=zbd --name=writeprepare --offset_increment=2g --size=2g --numjobs=14
   ```

2. **FIO配置文件**:

   ```ini
   ini复制代码[global]
   ioengine=psync          # 使用同步I/O引擎
   direct=1                # 启用直接I/O
   zonemode=zbd            # 使用Zoned Block Device模式
   bs=128k                 # 块大小为128KB
   numjobs=32              # 使用32个并行作业
   offset_increment=2g     # 每个作业的偏移量增加2GB
   size=2g                 # 每个作业处理2GB数据
   time_based=1            # 基于时间运行
   runtime=60s             # 每个测试运行60秒
   group_reporting=1       # 汇总报告
   
   [seqread]
   filename=/dev/nvme0n1   # 目标设备
   rw=read                 # 顺序读取测试
   ```

这些注释解释了每个参数的含义，有助于理解和调整测试配置。运行这些FIO配置可以有效地测试ZNS设备的顺序读写性能。







## 基于RocksDB的ZNFS的测试

### 吞吐量



# 总结与展望





# 实验

很多人都会有意或无意地忽略Zipfan分布下的实验结果。

脚本配置了多种测试模式，包括：

- **TEST_WRONLY_UNIFORM**：只写操作，使用均匀分布的键。
- **TEST_MIXED_73_UNIFORM**：混合操作，73%读和27%写，键使用均匀分布。
- **TEST_MIXED_37_UNIFORM**：混合操作，37%读和63%写，键使用均匀分布。
- **TEST_WRONLY_ZIPFIAN**：只写操作，使用Zipfian（长尾）分布的键。
- **TEST_MIXED_73_ZIPFIAN**：混合操作，73%读和27%写，键使用Zipfian分布。
- **TEST_MIXED_37_ZIPFIAN**：混合操作，37%读和63%写，键使用Zipfian分布。
- **TEST_MIXGRAPH**：更复杂的混合图测试。



# 图





LSM架构图和 批量写入问题。

![image-20240508205932120](%E6%AF%95%E8%AE%BE.assets/image-20240508205932120.png)









zenfs架构图

![ZenFS架构图](%E6%AF%95%E8%AE%BE.assets/ZenFS%E6%9E%B6%E6%9E%84%E5%9B%BE.png)





# 参考文献





1. LFS 
2. F2FS
3. BetrFS
4. Yang 等人
5. ML-DT
6. Windowed Greedy
7. Random-Greedy
8. d-choices















# 查重

学信网免费查重一次

https://pmlc.cnki.net/user/Submit.aspx



[https://chsi.wanfangtech.net/](https://link.zhihu.com/?target=https%3A//chsi.wanfangtech.net/)

根据你提供的测试结果和描述，以下是对这些测试结果的总结和分析，并通过绘图来更清晰地展示性能表现。



 



![image-20240524154533433](C:\Users\26557\AppData\Roaming\Typora\typora-user-images\image-20240524154533433.png)

 

 

 

 

 

