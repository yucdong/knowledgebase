# Chapter 6: Application components in Redis

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 6.1 Autocomplete
- 6.2 Distributed locking
- 6.3 Counting semaphores
- 6.4 Task queues
- 6.5 Pull messaging
- 6.6 Distributing files with Redis
- 6.7 Summary

---

Application
 components in Redis
In the last few chapters, we’ve gone through some basic use cases and tools to help
build applications in Redis. In this chapter, we’ll get into more useful tools and
techniques, working toward building bigger pieces of applications in Redis.
 We’ll begin by building autocomplete functions to quickly find users in short
and long lists of items. We’ll then take some time to carefully build two different
types of locks to reduce data contention, improve performance, prevent data cor-
ruption, and reduce wasted work. We’ll construct a delayed task queue, only to aug-
ment it later to allow for executing a task at a specific time with the use of the lock
This chapter covers
■Building two prefix-matching autocomplete methods
■Creating a distributed lock to improve performance
■Developing counting semaphores to control 
concurrency
■Two task queues for different use cases
■Pull messaging for delayed message delivery
■Handling file distribution

Distributed locking
 With distributed locking, we have the same sort of acquire, operate, release opera-
tions, but instead of having a lock that’s only known by threads within the same pro-
cess, or processes on the same machine, we use a lock that different Redis clients on
different machines can acquire and release. When and whether to use locks or WATCH
will depend on a given application; some applications don’t need locks to operate cor-
rectly, some only require locks for parts, and some require locks at every step. One reason why we spend so much time building locks with Redis instead of using
operating system–level locks, language-level locks, and so forth, is a matter of scope. Clients want to have exclusive access to data stored on Redis, so clients need to have
access to a lock defined in a scope that all clients can see—Redis. Redis does have a
basic sort of lock already available as part of the command set (SETNX), which we use,
but it’s not full-featured and doesn’t offer advanced functionality that users would
expect of a distributed lock. Throughout this section, we’ll talk about how an overloaded WATCHed key can
cause performance issues, and build a lock piece by piece until we can replace WATCH
for some situations. 6.2.1
Why locks are important
In the first version of our autocomplete, we added and removed items from a LIST. We
did so by wrapping our multiple calls with a MULTI/EXEC pair. Looking all the way back
to section 4.6, we first introduced WATCH/MULTI/EXEC transactions in the context of an
in-game item marketplace. If you remember, the market is structured as a single ZSET,
with members being an object and owner ID concatenated, along with the item price
as the score.

ItemC.7

ItemE.2

ItemG.3
