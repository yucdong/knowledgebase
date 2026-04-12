# Chapter 4: Keeping data safe and ensuring performance

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 4.1 Persistence options
- 4.2 Replication
- 4.3 Handling system failures
- 4.4 Redis transactions
- 4.5 Non-transactional pipelines
- 4.6 Performance considerations
- 4.7 Summary

---

Keeping data safe
 and ensuring performance
In the last few chapters, you’ve learned about the variety of commands available in
Redis and how they manipulate structures, and you’ve even solved a few problems
using Redis. This chapter will prepare you for building real software with Redis by
showing you how to keep your data safe, even in the face of system failure, and I’ll
point out methods that you can use to improve Redis performance while preserv-
ing data integrity.
 We’ll start by exploring the various Redis persistence options available to you
for getting your data on disk. We’ll then talk about the use of replication to keep
up-to-date copies of your data on additional machines for both performance and
This chapter covers
■Persisting data to disk
■Replicating data to other machines
■Dealing with system failures
■Redis transactions
■Non-transactional pipelines
■Diagnosing performance issues

CHAPTER 4
Keeping data safe and ensuring performance
Though the example shown in figure 4.1 may not necessarily need to be in a tree
structure, remembering and understanding that this is both possible and reasonable
for Redis replication can help you later.

Non-transactional pipelines
is the underlying library’s use of a pipeline, which improves performance. This section
will show how to use a pipeline without a transaction to further improve performance. You’ll remember from chapter 2 that some commands take multiple arguments for
adding/updating—commands like MGET, MSET, HMGET, HMSET, RPUSH/LPUSH, SADD, ZADD,
and others. Those commands exist to streamline calls to perform the same operation
repeatedly. As you saw in chapter 2, this can result in significant performance
improvements. Though not as drastic as these commands, the use of non-transac-
tional pipelines offers many of the same performance advantages, and allows us to run
a variety of commands at the same time. In the case where we don’t need transactions, but where we still want to do a lot of
work, we could still use MULTI/EXEC for their ability to send all of the commands at the
same time to minimize round trips and latency. Unfortunately, MULTI and EXEC aren’t
free, and can delay other important commands from executing. But we can gain all the
benefits of pipelining without using MULTI/EXEC. When we used MULTI/EXEC in Python
in chapter 3 and in section 4.4, you may have noticed that we did the following:
pipe = conn.pipeline()
By passing True to the pipeline() method (or omitting it), we’re telling our client to
wrap the sequence of commands that we’ll call with a MULTI/EXEC pair. If instead of
passing True we were to pass False, we’d get an object that prepared and collected
commands to execute similar to the transactional pipeline, only it wouldn’t be
wrapped with MULTI/EXEC.
