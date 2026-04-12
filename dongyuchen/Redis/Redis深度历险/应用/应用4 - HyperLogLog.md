# 应用 4：四两拨千斤 —— HyperLogLog

> 来源：*Redis深度历险：核心原理和应用实践*

## 目录

- 思考 & 作业
- 使用方法
- pfadd 这个 pf 是什么意思？
- pfmerge 适合什么场合用？
- 注意事项
- HyperLogLog 实现原理

---

127.0.0.1:6379> bitfield w overflow fail incrby u4 2 1   # 不执行 
1) (nil)  
思考 & 作业 
1、文中我们使用位操作设置了 he 两个字符，请读者将完整的 hello 单词中 5 个字符
都使用位操作设置一下。 
2、bitfield 可以同时混合执行多个 set/get/incrby 子指令，请读者尝试完成。

应用 4：四两拨千斤 —— HyperLogLog 
在开始这一节之前，我们先思考一个常见的业务问题：如果你负责开发维护一个大型的
网站，有一天老板找产品经理要网站每个网页每天的 UV 数据，然后让你来开发这个统计模
块，你会如何实现？ 
如果统计 PV 那非常好办，给每个网页一个独立的 Redis 计数器就可以了，这个计数器
的 key 后缀加上当天的日期。这样来一个请求，incrby 一次，最终就可以统计出所有的 PV 
数据。

但是 UV 不一样，它要去重，同一个用户一天之内的多次访问请求只能计数一次。这就
要求每一个网页请求都需要带上用户的 ID，无论是登陆用户还是未登陆用户都需要一个唯一 
ID 来标识。 
你也许已经想到了一个简单的方案，那就是为每一个页面一个独立的 set 集合来存储所
有当天访问过此页面的用户 ID。当一个请求过来时，我们使用 sadd 将用户 ID 塞进去就可
以了。通过 scard 可以取出这个集合的大小，这个数字就是这个页面的 UV 数据。没错，这
是一个非常简单的方案。 
但是，如果你的页面访问量非常大，比如一个爆款页面几千万的 UV，你需要一个很大
的 set 集合来统计，这就非常浪费空间。如果这样的页面很多，那所需要的存储空间是惊人
的。为这样一个去重功能就耗费这样多的存储空间，值得么？其实老板需要的数据又不需要
太精确，105w 和 106w 这两个数字对于老板们来说并没有多大区别，So，有没有更好的解
决方案呢？ 
这就是本节要引入的一个解决方案，Redis 提供了 HyperLogLog 数据结构就是用来解决
这种统计问题的。HyperLogLog 提供不精确的去重计数方案，虽然不精确但是也不是非常不
精确，标准误差是 0.81%，这样的精确度已经可以满足上面的 UV 统计需求了。 
HyperLogLog 数据结构是 Redis 的高级数据结构，它非常有用，但是令人感到意外的
是，使用过它的人非常少。 
使用方法 
HyperLogLog 提供了两个指令 pfadd 和 pfcount，根据字面意义很好理解，一个是增加
计数，一个是获取计数。pfadd 用法和 set 集合的 sadd 是一样的，来一个用户 ID，就将用
户 ID 塞进去就是。pfcount 和 scard 用法是一样的，直接获取计数值。

127.0.0.1:6379> pfadd codehole user1 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 1 
127.0.0.1:6379> pfadd codehole user2 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 2 
127.0.0.1:6379> pfadd codehole user3 
(integer) 1

127.0.0.1:6379> pfcount codehole 
(integer) 3 
127.0.0.1:6379> pfadd codehole user4 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 4 
127.0.0.1:6379> pfadd codehole user5 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 5 
127.0.0.1:6379> pfadd codehole user6 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 6 
127.0.0.1:6379> pfadd codehole user7 user8 user9 user10 
(integer) 1 
127.0.0.1:6379> pfcount codehole 
(integer) 10

简单试了一下，发现还蛮精确的，一个没多也一个没少。接下来我们使用脚本，往里面
灌更多的数据，看看它是否还可以继续精确下去，如果不能精确，差距有多大。人生苦短，
我用 Python！Python 脚本走起来！😄

# coding: utf-8

import redis

client = redis.StrictRedis() 
for i in range(1000): 
    client.pfadd("codehole", "user%d" % i) 
    total = client.pfcount("codehole") 
    if total != i+1: 
        print total, i+1 
        break

当然 Java 也不错，大同小异，下面是 Java 版本： 
public class PfTest { 
  public static void main(String[] args) { 
    Jedis jedis = new Jedis(); 
    for (int i = 0; i < 1000; i++) { 
      jedis.pfadd("codehole", "user" + i);

long total = jedis.pfcount("codehole"); 
      if (total != i + 1) { 
        System.out.printf("%d %d\n", total, i + 1); 
        break; 
      } 
    } 
    jedis.close(); 
  } 
}

我们来看下输出： 
> python pftest.py 
99 100

当我们加入第 100 个元素时，结果开始出现了不一致。接下来我们将数据增加到 10w 
个，看看总量差距有多大。

# coding: utf-8

import redis

client = redis.StrictRedis() 
for i in range(100000): 
    client.pfadd("codehole", "user%d" % i) 
print 100000, client.pfcount("codehole")

跑了约半分钟，我们看输出：

> python pftest.py 
100000 99723

差了 277 个，按百分比是 0.277%，对于上面的 UV 统计需求来说，误差率也不算高。
然后我们把上面的脚本再跑一边，也就相当于将数据重复加入一边，查看输出，可以发现，
pfcount 的结果没有任何改变，还是 99723，说明它确实具备去重功能。 
pfadd 这个 pf 是什么意思？ 
它是 HyperLogLog 这个数据结构的发明人 Philippe Flajolet 的首字母缩写，老师觉得他
发型很酷，看起来是个佛系教授。

pfmerge 适合什么场合用？ 
HyperLogLog 除了上面的 pfadd 和 pfcount 之外，还提供了第三个指令 pfmerge，用于
将多个 pf 计数值累加在一起形成一个新的 pf 值。 
比如在网站中我们有两个内容差不多的页面，运营说需要这两个页面的数据进行合并。
其中页面的 UV 访问量也需要合并，那这个时候 pfmerge 就可以派上用场了。 
注意事项 
HyperLogLog 这个数据结构不是免费的，不是说使用这个数据结构要花钱，它需要占据
一定 12k 的存储空间，所以它不适合统计单个用户相关的数据。如果你的用户上亿，可以算
算，这个空间成本是非常惊人的。但是相比 set 存储方案，HyperLogLog 所使用的空间那真
是可以使用千斤对比四两来形容了。

不过你也不必过于当心，因为 Redis 对 HyperLogLog 的存储进行了优化，在计数比较
小时，它的存储空间采用稀疏矩阵存储，空间占用很小，仅仅在计数慢慢变大，稀疏矩阵占
用空间渐渐超过了阈值时才会一次性转变成稠密矩阵，才会占用 12k 的空间。 
HyperLogLog 实现原理 
HyperLogLog 的使用非常简单，但是实现原理比较复杂，如果读者没有特别的兴趣，下
面的内容暂时可以跳过不看。 
为了方便理解 HyperLogLog 的内部实现原理，我画了下面这张图。

这张图的意思是，给定一系列的随机整数，我们记录下低位连续零位的最大长度 k，通
过这个 k 值可以估算出随机数的数量。 首先不问为什么，我们编写代码做一个实验，观察
一下随机整数的数量和 k 值的关系。

import math 
import random

# 算低位零的个数 
def low_zeros(value): 
    for i in xrange(1, 32): 
        if value >> i << i != value: 
            break

return i - 1

# 通过随机数记录最大的低位零的个数 
class BitKeeper(object):

def __init__(self): 
        self.maxbits = 0

def do(self): 
        for i in range(self.n): 
            self.keeper.random()

37300 15.19 14 
37400 15.19 16 
37500 15.19 14 
37600 15.20 15

def estimate(self):

观察脚本的输出，误差率控制在百分比个位数： 
100000 97287.38 0.03 
200000 189369.02 0.05 
300000 287770.04 0.04 
400000 401233.52 0.00 
500000 491704.97 0.02
