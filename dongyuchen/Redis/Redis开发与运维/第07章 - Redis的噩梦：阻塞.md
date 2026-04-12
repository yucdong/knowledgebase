# 第7章 Redis的噩梦：阻塞

> 来源：*Redis开发与运维*

## 目录

- 7.1 发现阻塞
- 7.2 内在原因
- 7.3 外在原因
- 7.4 本章重点回顾

---

第7章　Redis的噩梦：阻塞
Redis是典型的单线程架构，所有的读写操作都是在一条主线程中完成
的。当Redis用于高并发场景时，这条线程就变成了它的生命线。如果出现
阻塞，哪怕是很短时间，对于我们的应用来说都是噩梦。导致阻塞问题的场
景大致分为内在原因和外在原因：
·内在原因包括：不合理地使用API或数据结构、CPU饱和、持久化阻塞
等。
·外在原因包括：CPU竞争、内存交换、网络问题等。
本章我们聚焦于Redis阻塞问题，通过学习本章可掌握快速定位和解决
Redis阻塞的思路和技巧。

7.1　发现阻塞
当Redis阻塞时，线上应用服务应该最先感知到，这时应用方会收到大
量Redis超时异常，比如Jedis客户端会抛出JedisConnectionException异常。常
见的做法是在应用方加入异常统计并通过邮件/短信/微信报警，以便及时发
现通知问题。开发人员需要处理如何统计异常以及触发报警的时机。何时触
发报警一般根据应用的并发量决定，如1分钟内超过10个异常触发报警。在
实现异常统计时要注意，由于Redis调用API会分散在项目的多个地方，每个
地方都监听异常并加入监控代码必然难以维护。这时可以借助于日志系统，
如Java语言可以使用logback或log4j。当异常发生时，异常信息最终会被日志
系统收集到Appender（输出目的地），默认的Appender一般是具体的日志文
件，开发人员可以自定义一个Appender，用于专门统计异常和触发报警逻
辑，如图7-1所示。

图7-1　自定义Appender收集Redis异常
以Java的logback为例，实现代码如下：
public class Redis Appender extends AppenderBase<ILoggingEvent> {
    // 使用guava的AtomicLongMap,用于并发计数
    public static final AtomicLongMap<String> ATOMIC_LONG_MAP = AtomicLongMap.c
    static {
        // 自定义Appender加入到logback的rootLogger中
        LoggerContext loggerContext = (LoggerContext) LoggerFactory.getILoggerFa
        Logger rootLogger = loggerContext.getLogger(Logger.ROOT_LOGGER_NAME);
        ErrorStatisticsAppender errorStatisticsAppender = new ErrorStatisticsApp
        errorStatisticsAppender.setContext(loggerContext);
        errorStatisticsAppender.start();
        rootLogger.addAppender(errorStatisticsAppender);
}
    // 重写接收日志事件方法
    protected void append(ILoggingEvent event) {
        // 只监控error级别日志
        if (event.getLevel() == Level.ERROR) {
            IThrowableProxy throwableProxy = event.getThrowableProxy();
            // 确认抛出异常
            if (throwableProxy != null) {
                // 以每分钟为key，记录每分钟异常数量
                String key = DateUtil.formatDate(new Date(), "yyyyMMddHHmm");
                long errorCount = ATOMIC_LONG_MAP.incrementAndGet(key);
                if (errorCount > 10) {
                    // 超过10次触发报警代码
                }
                // 清理历史计数统计，防止极端情况下内存泄露
                for (String oldKey : ATOMIC_LONG_MAP.asMap().keySet()) {
                    if (!StringUtils.equals(key, oldKey)) {
                        ATOMIC_LONG_MAP.remove(oldKey);
                    }
                }
            }
        }
    }
开发提示
借助日志系统统计异常的前提是，需要项目必须使用日志API进行异常
统一输出，比如所有的异常都通过logger.error打印，这应该作为开发规范推
广。其他编程语言也可以采用类似的日志系统实现异常统计报警。
应用方加入异常监控之后还存在一个问题，当开发人员接到异常报警
后，通常会去线上服务器查看错误日志细节。这时如果应用操作的是多个

Redis节点（比如使用Redis集群），如何决定是哪一个节点超时还是所有的
节点都有超时呢？这是线上很常见的需求，但绝大多数的客户端类库并没有
在异常信息中打印ip和port信息，导致无法快速定位是哪个Redis节点超时。
不过修改Redis客户端成本很低，比如Jedis只需要修改Connection类下的
connect、sendCommand、readProtocolWithCheckingBroken方法专门捕获连
接，发送命令，协议读取事件的异常。由于客户端类库都会保存ip和port信
息，当异常发生时很容易打印出对应节点的ip和port，辅助我们快速定位问
题节点。
除了在应用方加入统计报警逻辑之外，还可以借助Redis监控系统发现
阻塞问题，当监控系统检测到Redis运行期的一些关键指标出现不正常时会
触发报警。Redis相关的监控系统开源的方案有很多，一些公司内部也会自
己开发监控系统。一个可靠的Redis监控系统首先需要做到对关键指标全方
位监控和异常识别，辅助开发运维人员发现定位问题。如果Redis服务没有
引入监控系统作辅助支撑，对于线上的服务是非常不负责任和危险的。这里
推荐笔者团队开源的CacheCloud系统，它内部的统计监控模块能够很好地辅
助工程师发现定位问题。
监控系统所监控的关键指标有很多，如命令耗时、慢查询、持久化阻
塞、连接拒绝、CPU/内存/网络/磁盘使用过载等。当出现阻塞时如果相关人
员不能深刻理解这些关键指标的含义和背后的原理，会严重影响解决问题的
速度。后面的内容将围绕引起Redis阻塞的原因做重点说明。

7.2　内在原因
定位到具体的Redis节点异常后，首先应该排查是否是Redis自身原因导
致，围绕以下几个方面排查：
·API或数据结构使用不合理。
·CPU饱和的问题。
·持久化相关的阻塞。

7.2.1　API或数据结构使用不合理
通常Redis执行命令速度非常快，但也存在例外，如对一个包含上万个
元素的hash结构执行hgetall操作，由于数据量比较大且命令算法复杂度是
O（n），这条命令执行速度必然很慢。这个问题就是典型的不合理使用API
和数据结构。对于高并发的场景我们应该尽量避免在大对象上执行算法复杂
度超过O（n）的命令，关于Redis命令的复杂度，详见第2章。
1.如何发现慢查询
Redis原生提供慢查询统计功能，执行slowlog get{n}命令可以获取最近
的n条慢查询命令，默认对于执行超过10毫秒的命令都会记录到一个定长队
列中，线上实例建议设置为1毫秒便于及时发现毫秒级以上的命令。如果命
令执行时间在毫秒级，则实例实际OPS只有1000左右。慢查询队列长度默认
128，可适当调大。慢查询更多细节见第3章。慢查询本身只记录了命令执行
时间，不包括数据网络传输时间和命令排队时间，因此客户端发生阻塞异常
后，可能不是当前命令缓慢，而是在等待其他命令执行。需要重点比对异常
和慢查询发生的时间点，确认是否有慢查询造成的命令阻塞排队。
发现慢查询后，开发人员需要作出及时调整。可以按照以下两个方向去
调整：
1）修改为低算法度的命令，如hgetall改为hmget等，禁用keys、sort等命
令。
2）调整大对象：缩减大对象数据或把大对象拆分为多个小对象，防止

一次命令操作过多的数据。大对象拆分过程需要视具体的业务决定，如用户
好友集合存储在Redis中，有些热点用户会关注大量好友，这时可以按时间
或其他维度拆分到多个集合中。
2.如何发现大对象
Redis本身提供发现大对象的工具，对应命令：redis-cli-h{ip}-
p{port}bigkeys。内部原理采用分段进行scan操作，把历史扫描过的最大对象
统计出来便于分析优化，运行效果如下：
# redis-cli --bigkeys
# Scanning the entire keyspace to find biggest keys as well as
# average sizes per key type. You can use -i 0.1 to sleep 0.1 sec
# per 100 SCAN commands (not usually needed).
[00.00%] Biggest string found so far 'ptc:-571805194744395733' with 17 bytes
[00.00%] Biggest string found so far 'RVF#2570599,1' with 3881 bytes
[00.01%] Biggest hash found so far 'pcl:8752795333786343845' with 208 fields
[00.37%] Biggest string found so far 'RVF#1224557,1' with 3882 bytes
[00.75%] Biggest string found so far 'ptc:2404721392920303995' with 4791 bytes
[04.64%] Biggest string found so far 'pcltm:614' with 5176729 bytes
[08.08%] Biggest string found so far 'pcltm:8561' with 11669889 bytes
[21.08%] Biggest string found so far 'pcltm:8598' with 12300864 bytes
..忽略更多输出...
-------- summary -------
Sampled 3192437 keys in the keyspace!
Total key length in bytes is 78299956 (avg len 24.53)
Biggest string found 'pcltm:121' has 17735928 bytes
Biggest hash found 'pcl:3650040409957394505' has 209 fields
2526878 strings with 954999242 bytes (79.15% of keys, avg size 377.94)
0 lists with 0 items (00.00% of keys, avg size 0.00)
0 sets with 0 members (00.00% of keys, avg size 0.00)
665559 hashs with 19013973 fields (20.85% of keys, avg size 28.57)
0 zsets with 0 members (00.00% of keys, avg size 0.00)
根据结果汇总信息能非常方便地获取到大对象的键，以及不同类型数据
结构的使用情况。

是因为上面的Redis实例为了追求低内存使用量，过度放宽ziplist使用条件
（修改了hash-max-ziplist-entries和hash-max-ziplist-value配置）。进程内的
hash对象平均存储着上万个元素，而针对ziplist的操作算法复杂度在O（n）
到O（n2）之间。虽然采用ziplist编码后hash结构内存占用会变小，但是操作
变得更慢且更消耗CPU。ziplist压缩编码是Redis用来平衡空间和效率的优化
手段，不可过度使用。关于ziplist编码细节见第8章的8.3节“内存优化”。

也可以查看info persistence统计中的aof_delayed_fsync指标，每次发生
fdatasync阻塞主线程时会累加。定位阻塞问题后具体优化方法见第5.3节的
AOF追加阻塞部分。
运维提示
硬盘压力可能是Redis进程引起的，也可能是其他进程引起的，可以使
用iotop查看具体是哪个进程消耗过多的硬盘资源。
3.HugePage写操作阻塞
子进程在执行重写期间利用Linux写时复制技术降低内存开销，因此只
有写操作时Redis才复制要修改的内存页。对于开启Transparent HugePages的
操作系统，每次写命令引起的复制内存页单位由4K变为2MB，放大了512
倍，会拖慢写操作的执行时间，导致大量写操作慢查询。例如简单的incr命
令也会出现在慢查询中。关于Transparent HugePages的细节见第12章的12.1
节“Linux配置优化”。
Redis官方文档中针对绝大多数的阻塞问题进行了分类说明，这里不再
详细介绍，细节请见：http://www.redis.io/topics/latency。

7.3.1　CPU竞争
CPU竞争问题如下：
·进程竞争：Redis是典型的CPU密集型应用，不建议和其他多核CPU密
集型服务部署在一起。当其他进程过度消耗CPU时，将严重影响Redis吞吐
量。可以通过top、sar等命令定位到CPU消耗的时间点和具体进程，这个问
题比较容易发现，需要调整服务之间部署结构。
·绑定CPU：部署Redis时为了充分利用多核CPU，通常一台机器部署多
个实例。常见的一种优化是把Redis进程绑定到CPU上，用于降低CPU频繁上
下文切换的开销。这个优化技巧正常情况下没有问题，但是存在例外情况，
如图7-2所示。
图7-2　Redis绑定CPU后父子进程使用一个CPU

当Redis父进程创建子进程进行RDB/AOF重写时，如果做了CPU绑定，
会与父进程共享使用一个CPU。子进程重写时对单核CPU使用率通常在90%
以上，父进程与子进程将产生激烈CPU竞争，极大影响Redis稳定性。因此
对于开启了持久化或参与复制的主节点不建议绑定CPU。

7.3.3　网络问题
网络问题经常是引起Redis阻塞的问题点。常见的网络问题主要有：连
接拒绝、网络延迟、网卡软中断等。
1.连接拒绝
当出现网络闪断或者连接数溢出时，客户端会出现无法连接Redis的情
况。我们需要区分这三种情况：网络闪断、Redis连接拒绝、连接溢出。
第一种情况：网络闪断。一般发生在网络割接或者带宽耗尽的情况，对
于网络闪断的识别比较困难，常见的做法可以通过sar-n DEV查看本机历史
流量是否正常，或者借助外部系统监控工具（如Ganglia）进行识别。具体
问题定位需要更上层的运维支持，对于重要的Redis服务需要充分考虑部署
架构的优化，尽量避免客户端与Redis之间异地跨机房调用。
第二种情况：Redis连接拒绝。Redis通过maxclients参数控制客户端最大
连接数，默认10000。当Redis连接数大于maxclients时会拒绝新的连接进入，
info stats的rejected_connections统计指标记录所有被拒绝连接的数量：
# redis-cli -p 6384 info Stats | grep rejected_connections
rejected_connections:0
Redis使用多路复用IO模型可支撑大量连接，但是不代表可以无限连
接。客户端访问Redis时尽量采用NIO长连接或者连接池的方式。
开发提示

7.4　本章重点回顾
1）客户端最先感知阻塞等Redis超时行为，加入日志监控报警工具可快
速定位阻塞问题，同时需要对Redis进程和机器做全面监控。
2）阻塞的内在原因：确认主线程是否存在阻塞，检查慢查询等信息，
发现不合理使用API或数据结构的情况，如keys、sort、hgetall等。关注CPU
使用率防止单核跑满。当硬盘IO资源紧张时，AOF追加也会阻塞主线程。
3）阻塞的外在原因：从CPU竞争、内存交换、网络问题等方面入手排
查是否因为系统层面问题引起阻塞。
