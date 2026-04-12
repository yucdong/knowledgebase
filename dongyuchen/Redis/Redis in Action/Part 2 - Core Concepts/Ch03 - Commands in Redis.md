# Chapter 3: Commands in Redis

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 3.1 Strings
- 3.2 Lists
- 3.3 Sets
- 3.4 Hashes
- 3.5 Sorted sets
- 3.6 Publish/subscribe
- 3.7 Other commands
- 3.8 Summary

---

Commands in Redis
In this chapter, we’ll primarily cover commands that we haven’t already covered in
chapters 1 and 2. By learning about Redis through its commands, you’ll be able to
build on the examples provided and have a better understanding of how to solve
your own problems. If you’re looking for short examples that are more than the
simple interactions I show here, you’ll find some in chapter 2.
 The commands that are highlighted in this chapter are broken down by struc-
ture or concept, and were chosen because they include 95% or more of the typical
Redis calls in a variety of applications. The examples are interactions in the con-
sole, similar to the way I introduced each of the structures in chapter 1. Where
appropriate, I’ll reference earlier or later sections that use those commands.
 In the section for each of the different data types, I’ll show commands that are
unique to the different structures, primarily focusing on what makes those struc-
tures and commands distinct. Let’s start by seeing how Redis STRINGs offer more
than just GET and SET operations.
This chapter covers
■String, list, and set commands
■Hash and sorted set commands
■Publish/subscribe commands
■Other commands

>>> conn.incr('key', 15)

>>> conn.decr('key', 5)

>>> conn.zcard('zset-key')

3.8
Summary
In this chapter, we’ve looked at commands that typically should cover at least 95% of
your command usage in Redis. We started with each of the different datatypes, and
then discussed PUBLISH and SUBSCRIBE, followed by SORT, MULTI/EXEC transactions,
and key expiration. If there’s one thing that you should learn from this chapter, it’s that a wide variety
of commands can be used to manipulate Redis structures in numerous ways. Although
this chapter presents more than 70 of the most important commands, still more are
listed and described at http://redis.io/commands. If there’s a second thing you should take away from this chapter, it’s that I some-
times don’t offer the perfect answer to every problem. In revisiting a few of our exam-
ples from chapters 1 and 2 in the exercises (whose answers you can see in the
downloadable source code), I’m giving you an opportunity to try your hand at taking
our already pretty-good answers, and making them better overall, or making them suit
your problems better. One large group of commands that we didn’t cover in this chapter was configuration-
related commands. In the next chapter, we get into configuring Redis to ensure your
data stays healthy, and we give pointers on how to ensure that Redis performs well. If we set a key to expire in the future 
and we wait long enough for the key 
to expire, when we try to fetch the 
key, it’s already been deleted.
