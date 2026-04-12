# 拓展 1：耳听八方 —— Stream

> 来源：*Redis深度历险：核心原理和应用实践*

## 目录

- 消息 ID
- 消息内容
- 增删改查
- 独立消费
- 创建消费组
- 消费
- Stream 消息太多怎么办?
- 消息如果忘记 ACK 会怎样?
- PEL 如何避免消息丢失?
- Stream 的高可用
- 分区 Partition
- 小结

---

拓展 1：耳听八方 —— Stream 
Redis5.0 被作者 Antirez 突然放了出来，增加了很多新的特色功能。而 Redis5.0 最大的
新特性就是多出了一个数据结构 Stream，它是一个新的强大的支持多播的可持久化的消息队
列，作者坦言 Redis Stream 狠狠地借鉴了 Kafka 的设计。

Redis Stream 的结构如上图所示，它有一个消息链表，将所有加入的消息都串起来，每
个消息都有一个唯一的 ID 和对应的内容。消息是持久化的，Redis 重启后，内容还在。 
每个 Stream 都有唯一的名称，它就是 Redis 的 key，在我们首次使用xadd 指令追加消
息时自动创建。 
每个 Stream 都可以挂多个消费组，每个消费组会有个游标last_delivered_id 在 Stream 
数组之上往前移动，表示当前消费组已经消费到哪条消息了。每个消费组都有一个 Stream 
内唯一的名称，消费组不会自动创建，它需要单独的指令xgroup create 进行创建，需要指定
从 Stream 的某个消息 ID 开始消费，这个 ID 用来初始化last_delivered_id 变量。 
每个消费组 (Consumer Group) 的状态都是独立的，相互不受影响。也就是说同一份 
Stream 内部的消息会被每个消费组都消费到。

同一个消费组 (Consumer Group) 可以挂接多个消费者 (Consumer)，这些消费者之间是
竞争关系，任意一个消费者读取了消息都会使游标last_delivered_id 往前移动。每个消费者有
一个组内唯一名称。 
消费者 (Consumer) 内部会有个状态变量pending_ids，它记录了当前已经被客户端读取
的消息，但是还没有 ack。如果客户端没有 ack，这个变量里面的消息 ID 会越来越多，一
旦某个消息被 ack，它就开始减少。这个 pending_ids 变量在 Redis 官方被称之为PEL，也
就是Pending Entries List，这是一个很核心的数据结构，它用来确保客户端至少消费了消息一
次，而不会在网络传输的中途丢失了没处理。 
消息 ID 
消息 ID 的形式是timestampInMillis-sequence，例如1527846880572-5，它表示当前的消
息在毫米时间戳1527846880572 时产生，并且是该毫秒内产生的第 5 条消息。消息 ID 可以
由服务器自动生成，也可以由客户端自己指定，但是形式必须是整数-整数，而且必须是后面
加入的消息的 ID 要大于前面的消息 ID。 
消息内容 
消息内容就是键值对，形如 hash 结构的键值对，这没什么特别之处。 
增删改查 
    1、xadd 追加消息 
    2、xdel 删除消息，这里的删除仅仅是设置了标志位，不影响消息总长度 
    3、xrange 获取消息列表，会自动过滤已经删除的消息 
    4、xlen 消息长度 
    5、del 删除 Stream 
# * 号表示服务器自动生成 ID，后面顺序跟着一堆 key/value 
#  名字叫 laoqian，年龄 30 岁 
127.0.0.1:6379> xadd codehole * name laoqian age 30   
1527849609889-0  # 生成的消息 ID 
127.0.0.1:6379> xadd codehole * name xiaoyu age 29 
1527849629172-0 
127.0.0.1:6379> xadd codehole * name xiaoqian age 1 
1527849637634-0

2) "youming" 
            3) "age" 
            4) "60" 
(93.11s)

客户端如果想要使用 xread 进行顺序消费，一定要记住当前消费到哪里了，也就是返回
的消息 ID。下次继续调用 xread 时，将上次返回的最后一个消息 ID 作为参数传递进去，
就可以继续消费后续的消息。 
block 0 表示永远阻塞，直到消息到来，block 1000 表示阻塞 1s，如果 1s 内没有任何
消息到来，就返回 nil。

127.0.0.1:6379> xread block 1000 count 1 streams codehole $ 
(nil) 
(1.07s)

创建消费组

#  表示从头开始消费 
127.0.0.1:6379> xgroup create codehole cg1 0-0 
OK 
# $ 表示从尾部开始消费，只接受新消息，当前 Stream 消息会全部忽略 
127.0.0.1:6379> xgroup create codehole cg2 $ 
OK 
# 获取 Stream 信息

127.0.0.1:6379> xinfo stream codehole 
 1) length 
 2) (integer) 3  # 共 3 个消息 
 3) radix-tree-keys 
 4) (integer) 1 
 5) radix-tree-nodes 
 6) (integer) 2 
 7) groups 
 8) (integer) 2  # 两个消费组 
 9) first-entry  # 第一个消息 
10) 1) 1527851486781-0 
    2) 1) "name" 
       2) "laoqian" 
       3) "age" 
       4) "30" 
11) last-entry  # 最后一个消息 
12) 1) 1527851498956-0 
    2) 1) "name" 
       2) "xiaoqian" 
       3) "age" 
       4) "1" 
# 获取 Stream 的消费组信息 
127.0.0.1:6379> xinfo groups codehole 
1) 1) name 
   2) "cg1" 
   3) consumers 
   4) (integer) 0  # 该消费组还没有消费者 
   5) pending 
   6) (integer) 0  # 该消费组没有正在处理的消息 
2) 1) name 
   2) "cg2" 
   3) consumers  # 该消费组还没有消费者 
   4) (integer) 0 
   5) pending 
   6) (integer) 0  # 该消费组没有正在处理的消息

我们看到 Stream 的长度被砍掉了。如果 Stream 在未来可以提供按时间戳清理消息的
规则那就更加完美了，但是目前还没有。 
消息如果忘记 ACK 会怎样? 
Stream 在每个消费者结构中保存了正在处理中的消息 ID 列表 PEL，如果消费者收到
了消息处理完了但是没有回复 ack，就会导致 PEL 列表不断增长，如果有很多消费组的
话，那么这个 PEL 占用的内存就会放大。

PEL 如何避免消息丢失? 
在客户端消费者读取 Stream 消息时，Redis 服务器将消息回复给客户端的过程中，客
户端突然断开了连接，消息就丢失了。但是 PEL 里已经保存了发出去的消息 ID。待客户端
重新连上之后，可以再次收到 PEL 中的消息 ID 列表。不过此时 xreadgroup 的起始消息 
ID 不能为参数>，而必须是任意有效的消息 ID，一般将参数设为 0-0，表示读取所有的 
PEL 消息以及自last_delivered_id 之后的新消息。 
Stream 的高可用 
Stream 的高可用是建立主从复制基础上的，它和其它数据结构的复制机制没有区别，也
就是说在 Sentinel 和 Cluster 集群环境下 Stream 是可以支持高可用的。不过鉴于 Redis 的
指令复制是异步的，在 failover 发生时，Redis 可能会丢失极小部分数据，这点 Redis 的其
它数据结构也是一样的。 
分区 Partition 
Redis 的服务器没有原生支持分区能力，如果想要使用分区，那就需要分配多个 
Stream，然后在客户端使用一定的策略来生产消息到不同的 Stream。你也许会认为 Kafka 要
先进很多，它是原生支持 Partition 的。关于这一点，我并不认同。记得 Kafka 的客户端也
存在 HashStrategy 么，因为它也是通过客户端的 hash 算法来将不同的消息塞入不同分区
的。 
另外,Kafka 还支持动态增加分区数量的能力，但是这种调整能力也是很蹩脚的，它不会
把之前已经存在的内容进行 rehash，不会重新分区历史数据。这种简单的动态调整的能力 
Redis Stream 通过增加新的 Stream 就可以做到。 
小结 
Stream 的消费模型借鉴了 Kafka 的消费分组的概念，它弥补了 Redis Pub/Sub 不能持
久化消息的缺陷。但是它又不同于 kafka，Kafka 的消息可以分 partition，而 Stream 不行。
如果非要分 parition 的话，得在客户端做，提供不同的 Stream 名称，对消息进行 hash 取
模来选择往哪个 Stream 里塞。

如果读者稍微研究过 Redis 作者的另一个开源项目 Disque 的话，这极可能是作者意识
到 Disque 项目的活跃程度不够，所以将 Disque 的内容移植到了 Redis 里面。这只是本人
的猜测，未必是作者的初衷。
