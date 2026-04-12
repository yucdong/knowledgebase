# Chapter 7: Search-based applications

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 7.1 Searching in Redis
- 7.2 Sorted indexes
- 7.3 Ad targeting
- 7.4 Job search
- 7.5 Summary

---

Search-based applications
Over the last several chapters, I’ve introduced a variety of topics and problems that
can be solved with Redis. Redis is particularly handy in solving a class of problems
that I generally refer to as search-based problems. These types of problems primarily
involve the use of SET and ZSET intersection, union, and difference operations to
find items that match a specified criteria.
 In this chapter, I’ll introduce the concept of searching for content with Redis
SETs. We’ll then talk about scoring and sorting our search results based on a few
different options. After getting all of the basics out of the way, we’ll dig into creat-
ing an ad-targeting engine using Redis, based on what we know about search.
Before finishing the chapter, we’ll talk about a method for matching or exceeding
a set of requirements as a part of job searching.
 Overall, the set of problems in this chapter will show you how to search and fil-
ter data quickly and will expand your knowledge of techniques that you can use to
This chapter covers
■Searching in Redis
■Scoring your search results
■Ad targeting
■Job search

CHAPTER 7
Search-based applications
more than 63 bits, and for our case, we’ll only use 48 bits for the sake of simplicity.

CHAPTER 7
Search-based applications
to ads that have already matched the required location. In this section, we’ll talk about
how we can record information about those words and the ads that were targeted to
discover basic patterns about user behavior in order to develop per-word, per-ad-
targeting bonuses. A crucial question you should be asking yourself is “Why are we using words in the
web page content to try to find better ads?” The simple reason is that ad placement is
all about context. If a web page has content related to the safety of children’s toys, show-
ing an ad for a sports car probably won’t do well. By matching words in the ad with
words in the web page content, we get a form of context matching quickly and easily. One thing to remember during this discussion is that we aren’t trying to be perfect. We aren’t trying to solve the ad-targeting and learning problem completely; we’re trying
to build something that will work “pretty well” with simple and straightforward methods. As such, our note about the fact that this isn’t mathematically rigorous still applies. RECORDING VIEWS
The first step in our learning process is recording the results of our ad targeting with
the record_targeting_result() function that we called earlier from listing 7.11. Overall, we’ll record some information about the ad-targeting results, which we’ll
later use to help us calculate click-through rates, action rates, and ultimately eCPM
bonuses for each word.
