# 第13章 Redis监控运维云平台CacheCloud

> 来源：*Redis开发与运维*

## 目录

- 13.1 CacheCloud是什么
- 13.2 快速部署
- 13.3 机器部署
- 13.4 接入应用
- 13.5 用户功能
- 13.6 运维功能
- 13.7 客户端上报
- 13.8 本章重点回顾

---

第13章　Redis监控运维云平台CacheCloud
无论使用还是运维Redis，千万不要将其看作黑盒，虽然Redis提供了一
些命令来做监控统计（例如info）和日常运维（例如redis-trib.rb），但是当
Redis达到了一定规模，这些命令会变得捉襟见肘，如果通过平台化的工具
统一监控和管理将极大地提升开发和运维人员工作效率。本章首先分析
Redis监控和运维中现有的问题，随后将介绍笔者团队开源的Redis私有云平
台CacheCloud，及其解决这些问题的方案。主要内容如下：
·由Redis监控和运维的现有问题引出CacheCloud。
·快速部署：快速搭建CacheCloud项目。
·机器部署：实现CacheCloud对机器管理部署。
·接入应用：使用CacheCloud部署Redis Cluster并完成客户端快速接入。
·用户功能：站在开发人员角度介绍CacheCloud相关功能。
·运维功能：站在运维人员角度介绍CacheCloud相关功能。
·客户端上报：CacheCloud获取上报客户端统计信息。

13.1　CacheCloud是什么
读者有没有想过，如果让你去运维大规模的Redis节点，例如数千个
Redis节点、数百台机器、数百个业务支撑，会遇到什么问题吗？很明显就
是缺少一个好的可视化运维平台。本节首先分析如果没有好的运维平台可能
存在的问题，接着介绍Redis开源私有云平台CacheCloud。

13.1.1　现有问题
1.部署成本
我们在第9章和第10章详细讲解了Redis Sentinel和Redis Cluster的安装、
配置、部署、运维。以Redis Cluster为例子，虽然Redis的作者开发了redis-
trib.rb这样的工具帮助我们快速构建和管理Redis Cluster，但是每个Redis节
点仍然需要手工配置和启动，相对来说还是比较繁琐的，而且由于是人工操
作，所以存在一定的错误率。例如作为一个Redis运维人员，管理几百上千
个Redis节点是很正常的事，如果单纯手工安装配置，既耗时又容易出错。
2.实例碎片化
关系型数据库（例如Oracle、MySQL）发展很多年已经非常成熟，会有
专职的DBA人员管理，运维流程和监控平台相对成熟稳定。对于像Redis这
样的NoSQL数据库，很多公司没有专职人员来维护，于是就会出现一种现
象：Redis由各个业务组来维护，造成Redis散落在各个机器上，没有整体的
管理。并且存在着很多由于业务收缩或者下线无人管理的Redis节点。高效
的做法应该是提供统一管理和监控的Redis平台，用于管理机器、集群、节
点、用户等资源并做好全方位监控，防止各种“私搭乱建”造成的混乱现象。
3.监控、统计和管理不完善
Redis Live[1]等工具虽然提供了可视化的方式来监控Redis的相关数据，
但是如果从功能全面性上还是不够的，例如Redis2.8之后提供的Redis
Sentinel和Redis3.0提供的Redis Cluster，目前的开源工具没有提供较好的支

持，而且对于Redis info中的某些重要指标也没有实现很好的监控和报警功
能。
4.运维、经济成本
业务组运维Redis会造成如下三个问题：
·业务组的开发人员可能更加善于使用Redis实现各种功能，但是没有足
够的精力和经验来维护好Redis。
·各个业务组的Redis较为分散地部署在各自服务器上，造成机器利用率
较低，出现大量闲置资源，同时监控和运维无法有效支撑。
·各个业务组的Redis使用各种不同的版本，不便于管理和交互。
所以，应该由一些在Redis运维方面更有经验的人来维护，使得开发者
更加关注于Redis使用本身，这样开发和运维可以各自做自己擅长的事情。
[1] https://github.com/nkrode/RedisLive

13.1.2　CacheCloud基本功能
笔者团队于2016年在GitHub上正式开源了Redis的私有云平台
CacheCloud[1]，它实现多种Redis类型（Redis Standalone、Redis Sentinel、
Redis Cluster）的自动部署、解决Redis节点碎片化现象，提供完善的统计、
监控、运维功能，减少运维成本和误操作，提高机器的利用率，提供灵活的
伸缩性，可方便地接入客户端，对于Redis的开发和运维人员非常有帮助。
整体功能架构如图13-1所示。
图13-1　CacheCloud整体功能架构
CacheCloud于2014年9月在搜狐视频正式上线，期间每天的平均命令调

13.2　快速部署
13.2.1　CacheCloud环境需求
安装部署CacheCloud需要以下环境：
·JDK7+：CacheCloud使用Java语言开发，并使用了JDK7的一些特性。
·Maven3：CacheCloud使用Maven3作为开发构建工具。
·MySQL5.5+：CacheCloud需要Redis的相关元信息进行持久化。
·Redis：CacheCloud支持对2.8以上版本的Redis，但建议读者使用
Redis3.0+。
注意
上述JDK指的是Oracle JDK，如果是Open JDK会存在错误。
CacheCloud提供了视频教
程：http://my.tv.sohu.com/pl/9100280/index.shtml。

13.2.2　CacheCloud快速开始
1.下载项目源码
访问CacheCloud的GitHub主页，可以通过两种方式下载CacheCloud的源
代码。
·直接下载zip压缩包。
·通过git选择对应的分支进行克隆。
master和各个release版本是生产可用的，其他分支可能是处于开发阶段
的，请慎重选择。
注意
截止本书完成，CacheCloud的release版本为1.3，开发和运维人员可以使
用该版本，同时在搜狐视频不存在内部版本的CacheCloud，都是使用GitHub
的版本，保证项目持续更新。
CacheCloud目录结构如下：
cachecloud：根目录
      cachecloud-open-client：cachecloud客户端相关
              cachecloud-jedis：cachecloud-web用到jedis
              cachecloud-open-client-basic：cachecloud客户端基础包
              cachecloud-open-client-redis：cachecloud客户端
              cachecloud-open-jedis-stat：cachecloud客户端上报统计
      cachecloud-open-common：cachecloud通用模块
      cachecloud-open-web：cachecloud服务模块
      script：启动和闭关项目脚本、数据库schema等
      pom.xml：Maven配置

13.3.1　部署脚本
1.脚本说明
CacheCloud项目中的cachecloud-init.sh（cachecloud/script目录下）脚本
是用来初始化服务器的CacheCloud环境，主要工作如下：
1）创建SSH用户。
2）创建CacheCloud相关目录：
Redis数据目录：/opt/cachecloud/data
Redis配置目录：/opt/cachecloud/conf
Redis日志目录：/opt/cachecloud/logs
Redis安装目录：/opt/cachecloud/redis
目录的用户和用户组设置为SSH用户。
3）安装最新的release版本的Redis。
注意
·CacheCloud默认使用Redis3.0以上版本，如需替换可以修改脚本中相应
代码。
·CacheCloud默认会安装在/opt目录下，如果/opt硬盘空间较小，可以修
改脚本中相应代码，同时需要在后台系统配置管理修改cachecloud根目录，
后面介绍。
·SSH是CacheCloud通信的重要基础，如果企业基于安全考虑禁用SSH，

13.4　接入应用
为CacheCloud添加机器资源后，可以利用自动化部署功能部署Redis应
用，这是自动化部署Redis的基础。本节将利用CacheCloud自动化部署一个
应用，并介绍开发人员如何通过CacheCloud客户端实现对Redis的使用。
注意
在CacheCloud中，Redis Standalone、Redis Sentinel、Redis Cluster统一称
为应用，后面读者将看到开发者只需要一个应用id，就可以实现Redis节点
的获取，完成客户端的正常调用。

13.4.3　应用申请和审批
1）点击“应用申请”按钮，弹出“应用申请”界面，如图13-11所示，按要
求填写应用需求，提交申请即可。

图13-11　应用申请表单
其中比较重要的属性用表13-2进行说明。

图13-18　CacheCloud服务端与客户端交互流程
http:// ip:port/cache/client/redis/cluster/10001.jsonclientVersion=1.2-SNAPSHOT
{
    message: "client is up to date, Cheers!", 
    shardNum: 10, # 节点个数
    appId: 10001, # 应用id
    status: 1,   # 状态为1表示数据正确
    shardInfo: "10.10.xx.1:6379,10.10.xx.2:6380 10.10.xx.3:6379,10.10.xx.4:6381 
        10.10.xx.5:6380,10.10.xx.7:6381 10.10.xx.8:6379,10.10.xx.xx:6381" #所有
        节点信息。主从节点用逗号隔开，多对主从节点用空格隔开。
}
有一点需要注意的是clientVersion=1.2-SNAPSHOT参数，它表示客户端
的版本，这个参数会传到服务端做校验，错误的版本将无法获取到接口信
息，如图13-19所示。

图13-19　CacheCloud客户端与服务端进行版本校验
管理员可以在后台的系统配置管理中，添加目前可以使用的客户端版
本，如图13-20所示。
图13-20　CacheCloud后台设置可用客户端版本
REST接口存在安全性问题，任意用户通过应用id都可以获取Redis节点
信息。如果希望更加安全，需要一个秘钥在CacheCloud服务端进行验证。这
个秘钥在应用申请成功后就会自动生成，并且展示到了应用详情页面（13.5
节会介绍）。新的接口添加了两处改动：
·参数增加了一个appkey。
·接口地址添加了一个safe路径。

所以如原接口为：
http:// ip:port/cache/client/redis/cluster/10001.jsonclientVersion=1.2-SNAPSHOT
那么新接口为：
http:// ip:port/cache/client/redis/cluster/safe/10001.jsonclientVersion=1.2-
    SNAPSHOT&appkey=xxxxx
运维提示
CacheCloud服务端为了兼容老的客户端，保留了两套接口，如果有需要
可以自行修改。
2.Java客户端
CacheCloud为Java开发者提供了封装好的客户端，基本实现原理也是调
用之前的REST接口，解析并初始化Jedis相关API，如JedisPool、
JedisSentinelPool、JedisCluster。
CacheCloud项目中的cachecloud-open-client模块是客户端模块，由以下
子模块组成：
·cachecloud-jedis：cachecloud-web用到的Jedis。
·cachecloud-open-client-basic：CacheCloud客户端基础模块。
·cachecloud-open-client-redis：CacheCloud客户端。
·cachecloud-open-jedis-stat：CacheCloud客户端上报统计。

13.5.2　实例列表
实例列表选项卡展示该应用下所有的Redis节点的基本信息：运行状
态、内存使用情况、对象数、连接数、命中率、碎片率、角色等，如图13-
24所示。通过实例列表，开发人员可以了解到每个节点数据、命中率等关键
指标，及时发现有问题的节点。
图13-24　应用实例列表
除此之外，单击每个Redis节点的ID还可以进入每个实例的监控界面，
包含了实例统计信息、慢查询分析、配置查询（包含了申请修改单个实例配
置的功能）、连接信息、故障报警、命令曲线等功能，它的功能和应用下的
功能是类似的，这里就不占用篇幅介绍了，有些不同的是实例信息都是实时
统计（例如直接调用info命令），而应用统计信息是周期性统计后进行汇总
生成的，所以会有一定的延迟。

13.5.3　应用详情
单击“应用详情”选项卡，可以看到三个模块：应用详情、用户管理、报
警指标，如图13-25所示。
·应用详情：应用id、应用名称、应用申请人、应用类型、报警用户、
负责人、Redis节点拓扑、appkey等。
·用户管理：对该应用的用户权限进行设置，添加进来的用户能有应用
的访问权。
·应用报警配置：CacheCloud面向用户的报警配置比较少，只有内存和
连接数，相关报警主要集中在管理员层面，13.6节会对CacheCloud监控报警
做详细介绍。

13.5.7　应用拓扑
“应用拓扑”选项卡展示应用下所有Redis所在机器的拓扑信息，实心的
方块代表主节点，同一列的空心方块代表从节点，如图13-30所示，它是一
个包含了24主24从的Redis Cluster集群，并且集群中没有出现主从节点同机
器的情况，但是当前集群在某几台机器上启动过多的主节点，该功能方便及
时发现当前集群部署结构存在的问题。
CacheCloud会每隔1分钟收集应用下所有节点的info信息，并将部分属性
做差值计算（例如命令、网络流量、过期键数量等等），然后将它们进行汇
总保存到MySQL中，前面的介绍的统计报表都是从MySQL中获取并制作成
图表的。除此之外，CacheCloud还会对机器信息、内存、连接数、AOF重
写、慢查询等做定期收集，每种收集都是在一个线程池内异步执行的，而整
体的调度依赖quartz[1]，整个过程如图13-31所示。
图13-30　应用拓扑

13.6.1　应用运维
CacheCloud的应用运维主要包含以下几个方面：
·应用上下线。
·Redis Sentinel运维。
·Redis Cluster运维。
·配置管理。
·垂直扩容和水平扩容。
1.应用上下线
我们已经通过CacheCloud自动化部署了应用（上线），那么当需要将这
个应用下线时，如何操作以及要注意哪些呢？管理员进入CacheCloud后台，
进入全局统计选项卡，可以看到应用列表，其中就包含了应用下线的按钮，
如图13-32所示。
图13-32　应用下线
应用下线会做如下操作：

·将应用所有的Redis节点关掉。
·CacheCloud停止应用下所有节点统计任务。
·将应用的状态变为下线，客户端无法集群使用已下线应用。
·将所有Redis节点的状态变为下线，这样客户端获取的Redis节点列表代
表为空。
运维提示
1）应用下线属于比较重要的操作，需要应用方和CacheCloud管理员确
认后方可进行，下线应用无法再次上线。
2）超级管理员组的用户才有权限下线应用，超级管理员组的配置方法
请参考13.6.6节。
2.应用运维
单击应用运维按钮即可进入运维界面，图13-33为Redis Cluster的运维界
面。

有关水平扩容有两点需要注意：
·不要过度依赖水平扩容，在开启应用分配资源时，提前做好规划更重
要，因为迁移无论对客户端还是服务端都有一定的成本。
·迁移速度上，migrate<set<AOF<RDB，所以在需要做数据迁移时，要弄
清真正需要什么粒度的迁移。 <li="">

13.6.2　接入已存在的Redis节点
到目前为止，Redis都是通过CacheCloud开启的，那么已经存在的Redis
节点如何接入到CacheCloud中呢？操作步骤如下：
1）管理员用户命令下拉菜单中导入应用链接。
2）填写导入应用表单，如图13-38所示，最重要的就是实例详情。与部
署应用不同的是，由于当前导入的节点已经存在，所以除了ip和
maxmemory，还需要填写端口号。
图13-38　CacheCloud接入已经存在的Redis
Redis数据节点和Sentinel节点格式如下：
·Redis数据节点：ip：port：maxmemory（单位为MB）。

·Sentinel节点：ip：port：masterName。
具体格式参考实例列表下面的说明即可，这里就不占用篇幅了。但是有
几点需要注意，如下情况会造成检查格式失败：
·机器不受CacheCloud管理。
·Redis节点不存在。
·Redis节点已经在CacheCloud中（可以在机器管理中查询，或者直接查
询instance_info表）。
·Sentinel节点masterName为空或者与真实masterName不符。
·Redis节点节点包含密码，此功能暂不支持密码。
·Redis节点没有配置maxmemory，会展示不出来应用内存统计。
验证格式并点击开始导入，就可以将填写的Redis节点导入到
CacheCloud中，包括应用信息、实例信息、应用和实例的各种统计信息的收
集就会生效，报表就可以展示出来，并且相关报警也会自动启动。那么将已
经存在的Redis接入CacheCloud到底做了什么呢？CacheCloud不会对Redis节
点造成任何性能上影响，只做了如下三件事：
1）验证输入内容。
2）保存应用信息、实例信息、应用与实例关系信息。
3）开启统计功能（每分钟执行一次info命令）。

13.6.3　Redis配置模板
该功能可以对每次开启的Redis节点添加配置模板，如图13-39为后台
Redis配置模板的管理页面。
图13-39　Redis配置模板管理
可以看到Redis配置模板管理提供了对配置模板的增删改查功能，按照
Redis普通节点、Sentinel节点、Cluster节点分别展示。当管理员设置好认为
最好的配置时，可以点击“配置预览”，即可看到配置模板预览，如下所示。
但需要注意该功能是配置模板，不是修改线上配置。
Redis普通节点配置，所用参数port=6379,maxmemory=2048 配置模板预览:
daemonize no
tcp-backlog 511
timeout 300
tcp-keepalive 60
loglevel notice
databases 16….
例如读者当前使用的是Redis3.2版本，那么就可以添加诸如protected-

org.springframework.dao.DeadlockLoserDataAccessException=22
com.sohu.cache.exception.SSHException=2
org.springframework.dao.DataIntegrityViolationException=1
这样管理员可以了解CacheCloud服务端的一些运行状态，如果发现异常
较多，可以尽快处理。
3）Redis实例心跳（邮件和短信）。CacheCloud会每5分钟对所有Redis
节点做心跳检测（3次ping操作），如果检测失败（3次ping都失败），管理
员会收到Redis节点心跳停止的消息，例如下面就是appId=10001的某个节点
可能宕掉。
CacheCloud系统-实例(10.10.xx.1:6381)-由运行中变为心跳停止, appId:10001-ranking-online
如果下一次检测到Redis已经恢复（3次ping命令，有一次ping通），管
理员同样会收到Redis节点已经运行的消息，如下所示：
CacheCloud系统-实例(10.10.xx.1:6381)-由心跳停止变为运行中, appId:10001-ranking-online
需要注意的是，心跳停止和下线是两个概念，下线是管理员操作的，心
跳停止是Cachecloud判断的，Redis节点是否真的宕掉需要管理员确认。
4）应用内存和客户端连接数（邮件和短信）。CacheCloud会每隔20分
钟，检测应用以及应用下每个Redis节点的内存和客户端连接数是否超过预
设阀值（第一次申请应用和应用详情界面可以设置）。
例如应用总体内存超过阀值会收到如下消息：
应用(10001)-内存使用率报警-预设百分之90-现已达到百分之92.88-请及时关注

例如应用单个Redis节点超过内存预设阀值会收到如下消息：
分片(10.10.xx.1:6380,应用(10001))内存使用率报警-预设百分之90-现已达到百分之92.28-应用的内存使用率百分之88
同样客户端连接数，也是如此同样会收到如下消息：
分片(10.10.xx.1:6380,应用(10001))客户端连接数报警-预设2500-现已达到2525-请及时关注
5）机器性能报警（邮件和短信）。CacheCloud会每小时对机器的内
存、负载、CPU进行监控，一旦超过预设阀值，将会收到如下信息：
ip:10.10.xx.1，load:10.79
机器报警阀值管理员只需要在后台的系统配置管理中，按照图13-46设
置即可。
图13-46　机器性能报警阀值设置
注意
CacheCloud已经计划在后期的版本中加入机器信息详细统计以及相关报
警功能，保证功能完整性。

13.7　客户端上报
客户端的耗时、值范围、异常对于开发人员发现定位自身Redis使用问
题至关重要，这些指标是了解Redis客户端运行状态的关键。本节将介绍
CacheCloud提供的一个Java客户端上报功能，可以将上述信息进行可视化展
示，本节内容包括：客户端上报整体设计、Jedis核心代码修改、带上报功
能的客户端、CacheCloud客户端统计。

13.7.2　Jedis核心代码修改
Jedis所有的命令调用函数主要分为两个部分：发送命令和获取结果，
如图13-48所示。
通过进步一观察，可以发现Jedis所有命令调用经过
redis.clients.jedis.Connection类，其中发送命令对应sendCommand（）函数，
返回结果对应readProtocol WithCheckingBroken（）函数，如图13-50所示。
所以可以在Connection类的这两个方法做命令调用的数据收集。
图13-48　Jedis命令与Connection类的对应关系

13.7.3　带上报功能的客户端
上个小节介绍了一下Jedis代码统计数据的方法和思路，本节将介绍如
何使用带有上报功能的客户端。
1）修改Jedis。
下载Jedis2.8以上的版本。修改Connection类，前面只给出了重要代码，
全部修改请参考：
https:// github.com/sohutv/jedis-2.8.0-stat/commit/0d82201172df25f769ced2786c88a
    5b928060c13
在Jedis中添加如下Maven依赖：
<dependency>
    <groupId>com.sohu.tv</groupId>
    <artifactId>cachecloud-open-jedis-stat</artifactId>
    <version>1.0</version>
</dependency>
这个模块是CacheCloud客户端的统计模块，上个小节中的
UsefulDataCollector和UsefulDataModel都在这个模块中，其中包含了
CacheCloud客户端管理统计数据和http上报的相关代码，这些代码都打包在
cachecloud-open-jedis-stat中，读者可以自行阅读。
2）以Redis Cluster为例，RedisClusterBuilder可以设置统计开关：
public RedisClusterBuilder setClientStatIsOpen(boolean clientStatIsOpen) { this
3）将cachecloud-open-client-redis包的pom.xml中的Jedis版本修改为你的

13.7.4　CacheCloud客户端统计
进入应用详情界面，点击客户端统计按钮即可进入客户端统计报表页
面。
第一步，耗时统计，如图13-49所示，包含如下内容：
1）应用和客户端的全局耗时统计，命令按照调用量倒排序。
2）所有客户端和Redis实例对应关系，以及耗时统计。
3）耗时统计包含了：平均值、中位值、90%最大值、99%最大值、最
大值五个维度。
第二步，值分布统计：客户端每次获取结果的大小都会被计数，图13-
50是所有值的分布，需要注意的是这些值是客户端访问过的键，不代表
Redis中所有的键。此功能有助于开发和运维人员分析bigkey问题。

13.8　本章重点回顾
1）CacheCloud可以解决规模化运维Redis带来的问题：部署成本、实例
碎片化、监控不完善、运维成本。
2）CacheCloud与机器使用SSH协议通信，所以使用脚本初始化机器信
息填写的ssh用户名和密码必须和后台系统配置一致。
3）CacheCloud客户端只是启动时从服务端获取应用的Redis节点信息，
之后不会与之产生交互。
4）利用好CacheCloud的监控功能，对于了解Redis的运行健康状况至关
重要。
5）CacheCloud提供了功能强大的运维功能：应用上下线、扩容、配置
修改、Redis节点上下线、Failover、数据迁移、各维度监控报警等。
6）客户端上报功能可以有效帮助开发和运维人员了解客户端运行状
态。
7）Jedis中的Connection类是命令的汇集点，是用来做命令统计的基础，
其他编程语言客户端也可以参照此方法进行二次开发。
