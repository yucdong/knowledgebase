# Appendix A: Quick and dirty setup

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

appendix A
Quick and dirty setup
Depending on your platform, setting up Redis can range from easy to difficult. I’ve
broken down installation instructions into sections for the three major platforms. Feel
free to skip ahead to your platform, which will also include instructions for installing
and configuring Python and the Redis client libraries for Python on your system.
A.1
Installation on Debian or Ubuntu Linux
If you’re using a Debian-derived Linux, your first instinct will be to apt-get install
redis-server, but this is probably the wrong thing to do. Depending on your version
of Debian or Ubuntu, you could be installing an old version of Redis. As an example,
if you’re using Ubuntu 10.4, you’d be downloading Redis 1.2.6, which was released
in March 2010 and doesn’t support many of the commands that we use.
 In this section, you’ll first install the build tools because you’ll compile Redis
from scratch. Then you’ll download, compile, and install Redis. After Redis is run-
ning, you’ll download the Redis client libraries for Python.
 To get started, make sure that you have all of the standard required build tools
installed by fetching and downloading make, as can be seen in the following listing.
~$ sudo apt-get update
~$ sudo apt-get install make gcc python-dev
When your build tools are installed (they were probably installed before; this was a
verification step), you’ll take these steps:

APPENDIX A
Quick and dirty setup
features too long to mention here. Whether you go basic or fully featured,
you can’t go wrong. REDIS ON OS X AND WINDOWS
Right now, precompiled versions of Redis for
Windows and OS X are from the 2.4 series. In some chapters, we use features
that are only available in the Redis 2.6 and later series. If you find that some-
thing we do doesn’t work, and you’re using Redis 2.4, it’s probably because
the feature or usage was added in Redis 2.6. See the notes in chapter 3 for
specific examples. CONFIGURING REDIS
By default, Redis should be configured to keep your data
using either snapshots or append-only files, and as long as you execute shut-
down on a client, Redis should keep your data around. Depending on how you
started it, Redis may be keeping the on-disk version of data in the same path
as the path you’re running it from. To update that, you’ll want to edit
redis.conf and use system startup scripts appropriate for your platform
(remember to move your data to the newly configured path). More informa-
tion about configuring Redis is available in chapter 4. IS HIREDIS AVAILABLE ON NON-LINUX PLATFORMS? For those who are using Win-
dows or OS X and peeked at the Debian/Ubuntu install instructions, you’ll
have noticed that we installed a library called hiredis to be used with Python. This library is an accelerator that passes protocol processing to a C library.
