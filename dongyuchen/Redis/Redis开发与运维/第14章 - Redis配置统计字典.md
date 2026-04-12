# 第14章 Redis配置统计字典

> 来源：*Redis开发与运维*

## 目录

- 14.1 info系统状态说明
- 14.2 standalone配置说明和分析
- 14.3 Sentinel配置说明和分析
- 14.4 Cluster配置说明和分析

---

第14章　Redis配置统计字典
本章将对Redis的系统状态信息（info命令结果）和Redis的所有配置
（包括Standalone、
Sentinel、Cluster三种模式）做一个全面的梳理，希望本章能够成为
Redis配置统计字典，协助大家分析和解决日常开发和运维中遇到的问题，
主要内容如下：
·info系统状态说明。
·Standalone配置说明。
·Sentinel配置说明。
·Cluster配置说明。

14.1　info系统状态说明
14.1.1　命令说明
info命令的使用方法有以下三种：
·info：部分Redis系统状态统计信息。
·info all：全部Redis系统状态统计信息。
·info section：某一块的系统状态统计信息，其中section可以忽略大小
写。
例如，只对Redis的内存相关统计比较感兴趣，可以执行info memory，
此时section=memory，下面是info memory的结果：
127.0.0.1:6379> info memory
# Memory
used_memory:5209229784
used_memory_human:4.85G
used_memory_rss:6255316992
used_memory_peak:5828761544
used_memory_peak_human:5.43G
used_memory_lua:36864
mem_fragmentation_ratio:1.20
mem_allocator:jemalloc-3.6.0
在运维的时候发现客户端有些异常，可以执行client clients，如以下信
息反映了输出缓冲区存在溢出的情况：
127.0.0.1:6379> info clients
# Clients
connected_clients:225
client_longest_output_list:245639
client_biggest_input_buf:0
blocked_clients:0

info all命令包含Redis最全的系统状态信息，表14-1是info all命令涉及的
所有section，其中每个模块名就是我们上面提到的section，例如info Server
是查看Redis服务的基本信息。
表14-1　info命令所有的section

14.1.2　详细说明
下面将对每个模块进行详细说明，为了更加方便解释，我们直接结合线
上一个运行的Redis实例进行说明。
1.Server
表14-2是info Server模块的统计信息，包含了Redis服务本身的一些信
息，例如版本号、运行模式、操作系统的版本、TCP端口等。
表14-2　info Server模块统计信息
2.Clients
表14-3是info Clients模块的统计信息，包含了连接数、阻塞命令连接

数、输入输出缓冲区等相关统计信息。
表14-3　info Clients模块统计信息
3.Memory
表14-4是info Memory模块的统计信息，包含了Redis内存使用、系统内
存使用、碎片率、内存分配器等相关统计信息。
表14-4　info Memory模块统计信息
4.Persistence
表14-5是info Persistence模块的统计信息，包含了RDB和AOF两种持久
化的一些统计信息。
表14-5　info Persistence模块统计信息

5.Stats
表14-6是info Stats模块的统计信息，是Redis的基础统计信息，包含了：
连接、命令、网络、过期、同步等很多统计信息。
表14-6　info Stats模块统计信息

6.Replication
表14-7是info Replication模块的统计信息，包含了Redis主从复制的一些
统计信息，根据主从节点，统计信息也略有不同
表14-7　info Replication模块统计信息

7.CPU
表14-8是info CPU模块的统计信息，包含了Redis进程和子进程对于CPU
消耗的一些统计信息。
表14-8　info CPU模块统计信息
8.Commandstats
表14-9是info Commandstats模块的统计信息，是Redis命令统计信息，包
含各个命令的命令名、总次数、总耗时、平均耗时。
表14-9　info Commandstats模块统计信息

9.Cluster
表14-10是info Cluster模块的统计信息，目前只有一个统计信息，标识当
前Redis是否为Cluster模式。
表14-10　info Cluster模块统计信息
10.Keyspace
表14-11是info Keyspace模块的统计信息，包含了每个数据库的键值统计
信息。
表14-11　info Keyspace模块统计信息

14.2　standalone配置说明和分析
相对于很多大型存储系统，Redis的配置不是很多，到了Redis3.0之后有
60多个，虽然还是不多，但是每个配置都有很重要的作用和意义，本节我们
将对Redis单机模式下的所有配置进行说明：

14.2.1　总体配置
表14-12是Redis的一些总体配置，例如端口、日志、数据库等。
表14-12　总体配置

14.2.2　最大内存及策略
表14-13是Redis内存相关配置，第8章有详细介绍。
表14-13　内存相关配置

14.2.3　AOF相关配置
表14-14是AOF方式持久化相关配置，第5章有详细介绍。
表14-14　AOF相关配置

14.2.4　RDB相关配置
表14-15是RDB方式持久化相关配置，第5章有详细介绍。
表14-15　RDB相关配置

14.2.5　慢查询配置
表14-16是Redis慢查询相关配置，第3章有详细介绍。
表14-16　慢查询相关配置

14.2.6　数据结构优化配置
表14-17是Redis数据结构优化的相关配置，第8章有详细介绍。
表14-17　数据结构优化相关配置

14.2.7　复制相关配置
表14-18是Redis复制相关的配置，第6章有详细介绍。
表14-18　复制相关配置

14.2.8　客户端相关配置
表14-19是Redis客户端的相关配置，第4章有详细介绍。
表14-19　客户端相关配置

14.2.9　安全相关配置
表14-20是Redis安全的相关配置，第12章有详细介绍。
表14-20　安全相关配置

14.3　Sentinel配置说明和分析
Sentinel节点是特殊的Redis节点，有几个特殊的配置，如表14-21所示。
表14-21　Redis Sentinel节点配置说明

14.4　Cluster配置说明和分析
Cluster节点是特殊的Redis节点，有几个特殊的配置，如表14-22所示。
表14-22　Redis Cluster配置说明