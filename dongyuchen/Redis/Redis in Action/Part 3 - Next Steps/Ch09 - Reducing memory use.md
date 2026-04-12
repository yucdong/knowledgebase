# Chapter 9: Reducing memory use

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 9.1 Short structures
- 9.2 Sharded structures
- 9.3 Packing bits and bytes
- 9.4 Summary

---

Reducing memory use
In this chapter, we’ll cover three important methods to help reduce your memory
use in Redis. By reducing the amount of memory you use in Redis, you can reduce
the time it takes to create or load a snapshot, rewrite or load an append-only file,
reduce slave synchronization time,1 and store more data in Redis without addi-
tional hardware.
 We’ll begin this chapter by discussing how the use of short data structures in
Redis can result in a more efficient representation of the data. We’ll then discuss
how to apply a concept called sharding to help make some larger structures small.2
Finally, we’ll talk about packing fixed-length data into STRINGs for even greater
memory savings.
This chapter covers
■Short structures
■Sharded structures
■Packing bits and bytes
1 Snapshots, append-only file rewriting, and slave synchronization are all discussed in chapter 4.
2 Our use of sharding here is primarily driven to reduce memory use on a single server. In chapter 10, we’ll
apply similar techniques to allow for increased read throughput, write throughput, and memory partition-
ing across multiple Redis servers.

"one\0"

"two\0"

"ten\0"
Figure 9.1
How long LISTs are stored in Redis

Sharded structures
example we can exploit our CPU caches. But when scanning through a list for a partic-
ular value, like our autocomplete example from section 6.1, or fetching/updating
individual fields of a HASH, Redis will have to decode many individual entries, and CPU
caches won’t be as effective. As a point of data, replacing our RPOPLPUSH command
with a call to LINDEX that gets an element in the middle of the LIST shows perfor-
mance at roughly half the number of operations per second as our RPOPLPUSH call
when LISTs are at least 5,000 items long. Feel free to try it for yourself. If you keep your max ziplist sizes in the 500–2,000 item range, and you keep the
max item size under 128 bytes or so, you should get reasonable performance. I per-
sonally try to keep max ziplist sizes to 1,024 elements with item sizes at 64 bytes or
smaller.

Summary
9.4
Summary
In this chapter, we’ve explored a number of ways to reduce memory use in Redis using
short data structures, sharding large structures to make them small again, and by
packing data directly into STRINGs.
 If there’s one thing that you should take away from this chapter, it’s that by being
careful about how you store your data, you can significantly reduce the amount of
memory that Redis needs to support your applications.
 In the next chapter, we’ll revisit a variety of topics to help Redis scale to larger
groups of machines, including read slaves, sharding data across multiple masters, and
techniques for scaling a variety of different types of queries.
