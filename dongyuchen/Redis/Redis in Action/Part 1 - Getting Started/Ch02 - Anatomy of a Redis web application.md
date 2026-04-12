# Chapter 2: Anatomy of a Redis web application

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 2.1 Login and cookie caching
- 2.2 Shopping carts in Redis
- 2.3 Web page caching
- 2.4 Database row caching
- 2.5 Web page analytics
- 2.6 Summary

---

Anatomy of a
 Redis web application
In the first chapter, I introduced you to what Redis is about and what it’s capable of.
In this chapter, I’ll continue on that path, starting to dig into several examples that
come up in the context of some types of web applications. Though I’ve simplified
the problems quite a bit compared to what happens in the real world, each of these
pieces can actually be used with little modification directly in your applications.
This chapter is primarily meant as a practical guide to what you can do with Redis,
and chapter 3 is more of a command reference.
 To start out, let’s look at what we mean by a web application from the high level.
Generally, we mean a server or service that responds over the HTTP protocol to
This chapter covers
■Login cookies
■Shopping cart cookies
■Caching generated web pages
■Caching database rows
■Analyzing web page visits

The server parses the request.

The request is forwarded to a predefined handler.

CHAPTER 2
Anatomy of a Redis web application
continue
end_index = min(size - LIMIT, 100)
tokens = conn.zrange('recent:', 0, end_index-1)
session_keys = []

CHAPTER 2
Anatomy of a Redis web application
And with that final piece, we’re now able to take our actual viewing statistics and only
cache those pages that are in the top 10,000 product pages. If we wanted to store even
more pages with minimal effort, we could compress the pages before storing them in
Redis, use a technology called edge side includes to remove parts of our pages, or we
could pre-optimize our templates to get rid of unnecessary whitespace. Each of these
techniques and more can reduce memory use and increase how many pages we could
store in Redis, all for additional performance improvements as our site grows. 2.6
Summary
In this chapter, we’ve covered a few methods for reducing database and web server
load for Fake Web Retailer. The ideas and methods used in these examples are cur-
rently in use in real web applications today. If there’s one thing that you should take away from this chapter, it’s that as you’re
building new pieces that fit within your application, you shouldn’t be afraid to revisit
and update old components that you’ve already written. Sometimes you may find that
your earlier solutions got you a few steps toward what you need now (as was the case
with both shopping cart cookies and web analytics combined with our initial login ses-
sion cookies code). As we continue through this book, we’ll keep introducing new
topics, and we’ll occasionally revisit them later to improve performance or functional-
ity, or to reuse ideas we already understand.
