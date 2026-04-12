# Chapter 8: Building a simple social network

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 8.1 Users and statuses
- 8.2 Home timeline
- 8.3 Followers/following lists
- 8.4 Posting or deleting a status update
- 8.5 Streaming API
- 8.6 Summary

---

Building a
 simple social network
In this chapter, we’ll cover the data structures and concepts necessary to build a sys-
tem that offers almost all of the back-end-level functionality of Twitter. This chapter
isn’t intended to allow you to build a site that scales to the extent of Twitter, but the
methods that we cover should give you a much better understanding of how social
networking sites can be built from simple structures and data.
 We’ll begin this chapter by talking about user and status objects, which are the
basis of almost all of the information in our application. From there, we’ll discuss
the home timeline and followers/following lists, which are sequences of status mes-
sages or users. Continuing on, we’ll work through posting status messages, follow-
ing/unfollowing someone, and deleting posts, which involves manipulating those
This chapter covers
■Users and statuses
■Home timeline
■Followers/following lists
■Posting or deleting a status update
■Streaming API

following

posts

...
558960079     1342915440
14502701       1342917840
14314352       1342957620
zset
following:139960061
...

CHAPTER 8
Building a simple social network
order to process each incoming request separately. When the server receives a
request, the server will create a thread to execute a request handler. This request han-
dler is where we’ll perform some initial basic routing for GET and POST HTTP requests. Both the threaded server and the request handler are shown in the next listing. class StreamingAPIServer(
SocketServer.ThreadingMixIn,
BaseHTTPServer.HTTPServer):
daemon_threads = True
class StreamingAPIRequestHandler(
BaseHTTPServer.BaseHTTPRequestHandler):
def do_GET(self):
parse_identifier(self)
if self.path != '/statuses/sample.json':
return self.send_error(404)
process_filters(self)
def do_POST(self):
parse_identifier(self)
if self.path != '/statuses/filter.json':
return self.send_error(404)
process_filters(self)
What we didn’t write is the code that actually starts up the server, but we’ll get to that
in a moment. For now, you can see that we defined a server that created threads on
each request. Those threads execute methods on a request handler object, which
eventually lead to either do_GET() or do_POST(), which handle the two major types of
streaming API requests: filtered and sampled. To actually run this server, we’ll use a bit of Python magic. This magic allows us to
later import a module to use these predefined classes, or it allows us to run the mod-
ule directly in order to start up a streaming API server. The code that lets us both
import the module and run it as a daemon can be seen in the next listing. Before you put these two blocks of code into a file and run them, remember that
we’re still missing two functions that are called as part of the streaming API server,
parse_identifier() and process_filters(), which we’ll cover next. Listing 8.9
Server and request handler for our streaming HTTP server
Create a new class called
“StreamingAPIServer”.
