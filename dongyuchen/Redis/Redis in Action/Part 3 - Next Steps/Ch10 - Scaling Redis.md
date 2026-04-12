# Chapter 10: Scaling Redis

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 10.1 Scaling reads
- 10.2 Scaling writes and memory capacity
- 10.3 Scaling complex queries
- 10.4 Summary

---

Scaling Redis
As your use of Redis grows, there may come a time when you’re no longer able to
fit all of your data into a single Redis server, or when you need to perform more
reads and/or writes than Redis can sustain. When this happens, you have a few
options to help you scale Redis to your needs. 
 In this chapter, we’ll cover techniques to help you to scale your read queries,
write queries, total memory available, and techniques for scaling a selection of
more complicated queries.
 Our first task is addressing those problems where we can store all of the data we
need, and we can handle writes without issue, but where we need to perform more
read queries in a second than a single Redis server can handle.
10.1
Scaling reads
In chapter 8 we built a social network that offered many of the same features and
functionalities of Twitter. One of these features was the ability for users to view their
home timeline as well as their profile timeline. When viewing these timelines, we’ll be
This chapter covers
■Scaling reads
■Scaling writes and memory capacity
■Scaling complex queries

Scaling reads
ENCRYPTION AND COMPRESSION OVERHEAD
Generally, encryption overhead for
SSH tunnels shouldn’t be a huge burden on your server, since AES-128 can
encrypt around 180 megabytes per second on a single core of a 2.6 GHz Intel
Core 2 processor, and RC4 can encrypt about 350 megabytes per second on
the same machine. Assuming that you have a gigabit network link, roughly
one moderately powerful core can max out the connection with encryption. Compression is where you may run into issues, because SSH compression
defaults to gzip. At compression level 1 (you can configure SSH to use a spe-
cific compression level; check the man pages for SSH), our trusty 2.6 GHz pro-
cessor can compress roughly 24–52 megabytes per second of a few different
types of Redis dumps (the initial sync), and 60–80 megabytes per second of a
few different types of append-only files (streaming replication). Remember
that, though higher compression levels may compress more, they’ll also use
more processor, which may be an issue for high-throughput low-processor
machines. Generally, I’d recommend using compression levels below 5 if pos-
sible, since 5 still provides a 10–20% reduction in total data size over level 1,
for roughly 2–3 times as much processing time. Compression level 9 typically
takes 5–10 times the time for level 1, for compression only 1–5% better than
level 5 (I stick to level 1 for any reasonably fast network connection).

Scaling writes and memory capacity
machine for each of your shards, or you can use multiple Redis databases
inside a single Redis server.
