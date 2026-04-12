# Chapter 5: Using Redis for application support

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 5.1 Logging to Redis
- 5.2 Counters and statistics
- 5.3 IP-to-city and -country lookup
- 5.4 Service discovery and configuration
- 5.5 Summary

---

Using Redis for
 application support
In the last chapter, we spent most of our time talking about how to keep Redis up
and running as part of a larger group of systems. In this chapter, we’ll talk about
using Redis to support other parts of your environment: from gathering informa-
tion about the current state of the system with logs and counters, to discovering
information about the clients using your system, all the way to configuring your sys-
tem by using Redis as a directory.
 Overall, this chapter offers control of and insight into how your system operates
during runtime. As you read along, keep in mind that we’re looking to support the
continued running of higher-level applications—that the components we build in
this chapter aren’t the applications themselves, but will help to support those appli-
cations. This support comes by way of recording information about the applications
This chapter covers
■Logging to Redis
■Counters and statistics
■Discovering city and country from IP address
■Service discovery and configuration

Logging to Redis
and application visitors, and a method of configuring applications. Let’s look at the first
level of monitoring that we can add through logging. 5.1
Logging to Redis
As we build applications and services, being able to discover information about the
running system becomes increasingly important. Being able to dig into that informa-
tion to diagnose problems, discover problems before they become severe, or even just
to discover information about users—these all necessitate logging. In the world of Linux and Unix, there are two common logging methods. The first
is logging to a file, where over time we write individual log lines to a file, and every
once in a while, we write to a new file. Many thousands of pieces of software have been
written do this (including Redis itself). But this method can run into issues because we
have many different services writing to a variety of log files, each with a different way
of rolling them over, and no common way of easily taking all of the log files and doing
something useful with them. Running on TCP and UDP port 514 of almost every Unix and Linux server available
is a service called syslog, the second common logging method. Syslog accepts log mes-
sages from any program that sends it a message and routes those messages to various
on-disk log files, handling rotation and deletion of old logs. With configuration, it can
even forward messages to other servers for further processing. As a service, it’s far
more convenient than logging to files directly, because all of the special log file rota-
tion and deletion is already handled for us.

ip_address = ip_to_score(ip_address)
city_id = conn.zrevrangebyscore(
