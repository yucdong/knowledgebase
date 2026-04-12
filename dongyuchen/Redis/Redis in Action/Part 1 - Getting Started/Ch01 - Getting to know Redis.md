# Chapter 1: Getting to know Redis

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 1.1 What is Redis?
- 1.2 What Redis data structures look like
- 1.3 Hello Redis
- 1.4 Getting help
- 1.5 Summary

---

Getting to know Redis
Redis is an in-memory remote database that offers high performance, replication,
and a unique data model to produce a platform for solving problems. By support-
ing five different types of data structures, Redis accommodates a wide variety of
problems that can be naturally mapped into what Redis offers, allowing you to solve
your problems without having to perform the conceptual gymnastics required by
other databases. Additional features like replication, persistence, and client-side
sharding allow Redis to scale from a convenient way to prototype a system, all the
way up to hundreds of gigabytes of data and millions of requests per second.
 My first experience with Redis was at a company that needed to search a data-
base of client contacts. The search needed to find contacts by name, email address,
location, and phone number. The system was written to use a SQL database that
performed a series of queries that would take 10–15 seconds to find matches
This chapter covers
■How Redis is like and unlike other software 
you’ve used
■How to use Redis
■Simple interactions with Redis using example 
Python code
■Solving real problems with Redis

What Redis data structures look like
to Redis data are always fast, because data is always in memory,2 and queries to Redis
don’t need to go through a typical query parser/optimizer. By using Redis instead of a relational or other primarily on-disk database, you can
avoid writing unnecessary temporary data, avoid needing to scan over and delete this
temporary data, and ultimately improve performance. These are both simple exam-
ples, but they demonstrate how your choice of tool can greatly affect the way you solve
your problems. As you continue to read about Redis, try to remember that almost everything that we
do is an attempt to solve a problem in real time (except for task queues in chapter 6). I show techniques and provide working code for helping you remove bottlenecks, sim-
plify your code, collect data, distribute data, build utilities, and, overall, to make your
task of building software easier. When done right, your software can even scale to levels
that would make other users of so-called web-scale technologies blush. We could keep talking about what Redis has, what it can do, or even why. Or I
could show you. In the next section, we’ll discuss the structures available in Redis,
what they can do, and some of the commands used to access them. 1.2
What Redis data structures look like
As shown in table 1.1, Redis allows us to store keys that map to any one of five different
data structure types; STRINGs, LISTs, SETs, HASHes, and ZSETs.

member0
