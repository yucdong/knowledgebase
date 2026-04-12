# 第2章 API的理解和使用

> 来源：*Redis开发与运维*

## 目录

- 2.1 预备
- 2.2 字符串
- 2.3 哈希
- 2.4 列表
- 2.5 集合
- 2.6 有序集合
- 2.7 键管理
- 2.8 本章重点回顾

---

第2章　API的理解和使用
Redis提供了5种数据结构，理解每种数据结构的特点对于Redis开发运
维非常重要，同时掌握Redis的单线程命令处理机制，会使数据结构和命令
的选择事半功倍，本章内容如下：
·预备知识：几个简单的全局命令，数据结构和内部编码，单线程命令
处理机制分析。
·5种数据结构的特点、命令使用、应用场景。
·键管理、遍历键、数据库管理。

2.1　预备
在正式介绍5种数据结构之前，了解一下Redis的一些全局命令、数据结
构和内部编码、单线程命令处理机制是十分有必要的，它们能为后面内容的
学习打下一个好的基础，主要体现在两个方面：第一、Redis的命令有上百
个，如果纯靠死记硬背比较困难，但是如果理解Redis的一些机制，会发现
这些命令有很强的通用性。第二、Redis不是万金油，有些数据结构和命令
必须在特定场景下使用，一旦使用不当可能对Redis本身或者应用本身造成
致命伤害。

·-1：键没设置过期时间。
·-2：键不存在
可以通过ttl命令观察键hello的剩余过期时间：
#还剩7秒
127.0.0.1:6379> ttl hello
(integer) 7
...
#还剩1秒
127.0.0.1:6379> ttl hello
(integer) 1
#返回结果为-2，说明键hello已经被删除
127.0.0.1:6379> ttl hello
(integer) -2
127.0.0.1:6379> get hello
(nil)
有关键过期更为详细的使用以及原理会在2.7节介绍。
6.键的数据结构类型
type key
例如键hello是字符串类型，返回结果为string。键mylist是列表类型，返
回结果为list：
127.0.0.1:6379> set a b
OK
127.0.0.1:6379> type a
string
127.0.0.1:6379> rpush mylist a b c d e f g
(integer) 7
127.0.0.1:6379> type mylist
list
如果键不存在，则返回none：
127.0.0.1:6379> type not_exsit_key
none

的优势，为列表类型提供了一种更为优秀的内部编码实现，而对外部用户来
说基本感知不到。第二，多种内部编码实现可以在不同场景下发挥各自的优
势，例如ziplist比较节省内存，但是在列表元素比较多的情况下，性能会有
所下降，这时候Redis会根据配置选项将列表类型的内部实现转换为
linkedlist。

图2-4　所有命令在一个队列里排队等待被执行
图2-5　不存在多个命令被同时执行的情况
2.为什么单线程还能这么快
通常来讲，单线程处理能力要比多线程差，例如有10000斤货物，每辆
车的运载能力是每次200斤，那么要50次才能完成，但是如果有50辆车，只
要安排合理，只需要一次就可以完成任务。那么为什么Redis使用单线程模
型会达到每秒万级别的处理能力呢？可以将其归结为三点：
第一，纯内存访问，Redis将所有数据放在内存中，内存的响应时长大
约为100纳秒，这是Redis达到每秒万级别访问的重要基础。
第二，非阻塞I/O，Redis使用epoll作为I/O多路复用技术的实现，再加上
Redis自身的事件处理模型将epoll中的连接、读写、关闭都转换为事件，不
在网络I/O上浪费过多的时间，如图2-6所示。

图2-6　Redis使用IO多路复用和自身事件模型
第三，单线程避免了线程切换和竞态产生的消耗。
既然采用单线程就能达到如此高的性能，那么也不失为一种不错的选
择，因为单线程能带来几个好处：第一，单线程可以简化数据结构和算法的
实现。如果对高级编程语言熟悉的读者应该了解并发数据结构实现不但困难
而且开发测试比较麻烦。第二，单线程避免了线程切换和竞态产生的消耗，
对于服务端开发来说，锁和线程切换通常是性能杀手。
但是单线程会有一个问题：对于每个命令的执行时间是有要求的。如果
某个命令执行过长，会造成其他命令的阻塞，对于Redis这种高性能的服务
来说是致命的，所以Redis是面向快速执行场景的数据库。
单线程机制很容易被初学者忽视，但笔者认为Redis单线程机制是开发
和运维人员使用和理解Redis的核心之一，随着后面的学习，相信读者会逐

2.2.1　命令
字符串类型的命令比较多，本小节将按照常用和不常用两个维度进行说
明，但是这里常用和不常用是相对的，希望读者尽可能都去了解和掌握。
1.常用命令
（1）设置值
set key value [ex seconds] [px milliseconds] [nx|xx]
下面操作设置键为hello，值为world的键值对，返回结果为OK代表设置
成功：
127.0.0.1:6379> set hello world
OK
set命令有几个选项：
·ex seconds：为键设置秒级过期时间。
·px milliseconds：为键设置毫秒级过期时间。
·nx：键必须不存在，才可以设置成功，用于添加。
·xx：与nx相反，键必须存在，才可以设置成功，用于更新。
除了set选项，Redis还提供了setex和setnx两个命令：
setex key seconds value
setnx key value

图2-9　一次mget命令执行模型
Redis可以支撑每秒数万的读写操作，但是这指的是Redis服务端的处理
能力，对于客户端来说，一次命令除了命令时间还是有网络时间，假设网络
时间为1毫秒，命令时间为0.1毫秒（按照每秒处理1万条命令算），那么执
行1000次get命令和1次mget命令的区别如表2-1，因为Redis的处理能力已经
足够高，对于开发人员来说，网络可能会成为性能的瓶颈。
表2-1　1000次get和1次get对比表
学会使用批量操作，有助于提高业务处理效率，但是要注意的是每次批
量操作所发送的命令数不是无节制的，如果数量过多可能造成Redis阻塞或
者网络拥塞。

在更新操作上会更加便捷。可以将每个用户的id定义为键后缀，多对field-
value对应每个用户的属性，类似如下伪代码：
UserInfo getUserInfo(long id){
    // 用户id作为key后缀
    userRedisKey = "user:info:" + id;
    // 使用hgetall获取所有用户信息映射关系
    userInfoMap = redis.hgetAll(userRedisKey);
    UserInfo userInfo;
    if (userInfoMap != null) {
        // 将映射关系转换为UserInfo
        userInfo = transferMapToUserInfo(userInfoMap);
    } else {
        // 从MySQL中获取用户信息
        userInfo = mysql.get(id);
        // 将userInfo变为映射关系使用hmset保存到Redis中
        redis.hmset(userRedisKey, transferUserInfoToMap(userInfo));
        // 添加过期时间
        redis.expire(userRedisKey, 3600);
    }
    return userInfo;
}
但是需要注意的是哈希类型和关系型数据库有两点不同之处：
·哈希类型是稀疏的，而关系型数据库是完全结构化的，例如哈希类型
每个键可以有不同的field，而关系型数据库一旦添加新的列，所有行都要为
其设置值（即使为NULL），如图2-17所示。
·关系型数据库可以做复杂的关系查询，而Redis去模拟关系型复杂查询
开发困难，维护成本高。

2）序列化字符串类型：将用户信息序列化后用一个键保存。
set user:1 serialize(userInfo)
优点：简化编程，如果合理的使用序列化可以提高内存的使用效率。
缺点：序列化和反序列化有一定的开销，同时每次更新属性都需要把全
部数据取出进行反序列化，更新后再序列化到Redis中。
3）哈希类型：每个用户属性使用一对field-value，但是只用一个键保
存。
hmset user:1 name tomage 23 city beijing
优点：简单直观，如果使用合理可以减少内存空间的使用。
缺点：要控制哈希在ziplist和hashtable两种内部编码的转换，hashtable会
消耗更多内存。

·有序集合相比集合提供了排序字段，但是也产生了代价，zadd的时间
复杂度为O（log（n）），sadd的时间复杂度为O（1）。
（2）计算成员个数
zcard key
例如下面操作返回有序集合user：ranking的成员数为5，和集合类型的
scard命令一样，zcard的时间复杂度为O（1）。
127.0.0.1:6379> zcard user:ranking
(integer) 5
（3）计算某个成员的分数
zscore key member
tom的分数为251，如果成员不存在则返回nil：
127.0.0.1:6379> zscore user:ranking tom
"251"
127.0.0.1:6379> zscore user:ranking test
(nil)
（4）计算成员的排名
zrank key member
zrevrank key member
zrank是从分数从低到高返回排名，zrevrank反之。例如下面操作中，tom
在zrank和zrevrank分别排名第5和第0（排名从0开始计算）。

ttl命令和pttl都可以查询键的剩余过期时间，但是pttl精度更高可以达到
毫秒级别，有3种返回值：
·大于等于0的整数：键剩余的过期时间（ttl是秒，pttl是毫秒）。
·-1：键没有设置过期时间。
·-2：键不存在。
expireat命令可以设置键的秒级过期时间戳，例如如果需要将键hello在
2016-08-0100：00：00（秒级时间戳为1469980800）过期，可以执行如下操
作：
127.0.0.1:6379> expireat hello 1469980800
(integer) 1
除此之外，Redis2.6版本后提供了毫秒级的过期方案：
·pexpire key milliseconds：键在milliseconds毫秒后过期。
·pexpireat key milliseconds-timestamp键在毫秒级时间戳timestamp后过
期。
但无论是使用过期时间还是时间戳，秒级还是毫秒级，在Redis内部最
终使用的都是pexpireat。
在使用Redis相关过期命令时，需要注意以下几点。
1）如果expire key的键不存在，返回结果为0：

下面的例子证实了set会导致过期时间失效，因为ttl变为-1：
127.0.0.1:6379> expire hello 50
(integer) 1
127.0.0.1:6379> ttl hello
(integer) 46
127.0.0.1:6379> set hello world
OK
127.0.0.1:6379> ttl hello
(integer) -1
5）Redis不支持二级数据结构（例如哈希、列表）内部元素的过期功
能，例如不能对列表类型的一个元素做过期时间设置。
6）setex命令作为set+expire的组合，不但是原子执行，同时减少了一次
网络通讯的时间。
有关Redis键过期的详细原理，8.2节会深入剖析。
4.迁移键
迁移键功能非常重要，因为有时候我们只想把部分数据由一个Redis迁
移到另一个Redis（例如从生产环境迁移到测试环境），Redis发展历程中提
供了move、dump+restore、migrate三组迁移键的方法，它们的实现方式以及
使用的场景不太相同，下面分别介绍。
（1）move
move key db
如图2-26所示，move命令用于在Redis内部进行数据迁移，Redis内部可
以有多个数据库，由于多个数据库功能后面会进行介绍，这里只需要知道
Redis内部可以有多个数据库，彼此在数据上是相互隔离的，move key db就

redis-target> get hello
(nil)
redis-target> restore hello 0 "\x00\x05world\x06\x00\x8f<T\x04%\xfcNQ"
OK
redis-target> get hello
"world"
上面2步对应的伪代码如下：
Redis sourceRedis = new Redis("sourceMachine", 6379);
Redis targetRedis = new Redis("targetMachine", 6379);
targetRedis.restore("hello", 0, sourceRedis.dump(key));
（3）migrate
migrate host port key|"" destination-db timeout [copy] [replace] [keys key [key 
migrate命令也是用于在Redis实例间进行数据迁移的，实际上migrate命
令就是将dump、restore、del三个命令进行组合，从而简化了操作流程。
migrate命令具有原子性，而且从Redis3.0.6版本以后已经支持迁移多个键的
功能，有效地提高了迁移效率，migrate在10.4节水平扩容中起到重要作用。
整个过程如图2-28所示，实现过程和dump+restore基本类似，但是有3点
不太相同：第一，整个过程是原子执行的，不需要在多个Redis实例上开启
客户端的，只需要在源Redis上执行migrate命令即可。第二，migrate命令的
数据传输直接在源Redis和目标Redis上完成的。第三，目标Redis完成restore
后会发送OK给源Redis，源Redis接收后会根据migrate对应的选项来决定是否
在源Redis上删除对应的键。

·[]代表匹配部分字符，例如[1，3]代表匹配1，3，[1-10]代表匹配1到10
的任意数字。
·\x用来做转义，例如要匹配星号、问号需要进行转义。
下面操作匹配以j，r开头，紧跟edis字符串的所有键：
127.0.0.1:6379> keys [j,r]edis
1) "jedis"
2) "redis"
例如下面操作会匹配到hello和hill这两个键：
127.0.0.1:6379> keys hll*
1) "hill"
2) "hello"
当需要遍历所有键时（例如检测过期或闲置时间、寻找大对象等），
keys是一个很有帮助的命令，例如想删除所有以video字符串开头的键，可以
执行如下操作：
redis-cli keys video* | xargs redis-cli del
但是如果考虑到Redis的单线程架构就不那么美妙了，如果Redis包含了
大量的键，执行keys命令很可能会造成Redis阻塞，所以一般建议不要在生
产环境下使用keys命令。但有时候确实有遍历键的需求该怎么办，可以在以
下三种情况使用：
·在一个不对外提供服务的Redis从节点上执行，这样不会阻塞到客户端
的请求，但是会影响到主从复制，有关主从复制我们将在第6章进行详细介
绍。

·如果确认键值总数确实比较少，可以执行该命令。
·使用下面要介绍的scan命令渐进式的遍历所有键，可以有效防止阻
塞。
2.渐进式遍历
Redis从2.8版本后，提供了一个新的命令scan，它能有效的解决keys命
令存在的问题。和keys命令执行时会遍历所有键不同，scan采用渐进式遍历
的方式来解决keys命令可能带来的阻塞问题，每次scan命令的时间复杂度是
O（1），但是要真正实现keys的功能，需要执行多次scan。Redis存储键值对
实际使用的是hashtable的数据结构，其简化模型如图2-29所示。
图2-29　hashtable示意图
那么每次执行scan，可以想象成只扫描一个字典中的一部分键，直到将
字典中的所有键遍历完毕。scan的使用方法如下：
scan cursor [match pattern] [count number]

2.8　本章重点回顾
1）Redis提供5种数据结构，每种数据结构都有多种内部编码实现。
2）纯内存存储、IO多路复用技术、单线程架构是造就Redis高性能的三
个因素。
3）由于Redis的单线程架构，所以需要每个命令能被快速执行完，否则
会存在阻塞Redis的可能，理解Redis单线程命令处理机制是开发和运维Redis
的核心之一。
4）批量操作（例如mget、mset、hmset等）能够有效提高命令执行的效
率，但要注意每次批量操作的个数和字节数。
5）了解每个命令的时间复杂度在开发中至关重要，例如在使用keys、
hgetall、smembers、zrange等时间复杂度较高的命令时，需要考虑数据规模
对于Redis的影响。
6）persist命令可以删除任意类型键的过期时间，但是set命令也会删除
字符串类型键的过期时间，这在开发时容易被忽视。
7）move、dump+restore、migrate是Redis发展过程中三种迁移键的方
式，其中move命令基本废弃，migrate命令用原子性的方式实现了
dump+restore，并且支持批量操作，是Redis Cluster实现水平扩容的重要工
具。
8）scan命令可以解决keys命令可能带来的阻塞问题，同时Redis还提供

了hscan、sscan、zscan渐进式地遍历hash、set、zset。
