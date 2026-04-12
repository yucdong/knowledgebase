# Chapter 11: Scripting Redis with Lua

> Source: *Redis in Action* by Josiah L. Carlson (Manning, 2013)

## Topics

- 11.1 Adding functionality without writing C
- 11.2 Rewriting locks and semaphores with Lua
- 11.3 Doing away with WATCH/MULTI/EXEC
- 11.4 Sharding LISTs with Lua
- 11.5 Summary

---

Scripting Redis with Lua
Over the last several chapters, you’ve built up a collection of tools that you can use
in existing applications, while also encountering techniques you can use to solve a
variety of problems. This chapter does much of the same, but will turn some of
your expectations on their heads. As of Redis 2.6, Redis includes server-side scripting
with the Lua programming language. This lets you perform a variety of operations
inside Redis, which can both simplify your code and increase performance.
 In this chapter, we’ll start by discussing some of the advantages of Lua over per-
forming operations on the client, showing an example from the social network in
chapter 8. We’ll then go through two problems from chapters 4 and 6 to show exam-
ples where using Lua can remove the need for WATCH/MULTI/EXEC transactions.
Later, we’ll revisit our locks and semaphores from chapter 6 to show how they can be
implemented using Lua for fair multiple client access and higher performance.
Finally, we’ll build a sharded LIST using Lua that supports many (but not all) stan-
dard LIST command equivalents.
This chapter covers
■Adding functionality without writing C
■Rewriting locks and semaphores with Lua
■Doing away with WATCH/MULTI/EXEC
■Sharding LISTs with Lua

14ms
5 listers, 5 buyers, 
with fine-grained lock
116,000
111,000

Summary
def sharded_blpop(conn, key, timeout=0):
return sharded_bpop_helper(
conn, key, timeout, sharded_lpop, 'blpop', ':first', 'lpush')
def sharded_brpop(conn, key, timeout=0):
return sharded_bpop_helper(
conn, key, timeout, sharded_rpop, 'brpop', ':last', 'rpush')
sharded_bpop_helper_lua = script_load('''
local shard = redis.call('get', KEYS[2]) or '0'
if shard ~= ARGV[1] then
redis.call(ARGV[2], KEYS[1]..ARGV[1], ARGV[3])
end
''')
There are a lot of pieces that come together to make this actually work, but remember
that there are three basic pieces. The first piece is a helper that handles the loop to
actually fetch the item. Inside this loop, we call the second piece, which is the helper/
blocking pop pair of functions, which handles the blocking portion of the calls. The
third piece is the API that users will actually call, which handles passing all of the
proper arguments to the helper. For each of the commands operating on sharded LISTs, we could implement them
with WATCH/MULTI/EXEC transactions. But a practical issue comes up when there’s a
modest amount of contention, because each of these operations manipulates multiple
structures simultaneously, and will manipulate structures that are calculated as part of
the transaction itself. Using a lock over the entire structure can help somewhat, but
using Lua improves performance significantly. 11.5
Summary
If there’s one idea that you should take away from this chapter, it’s that scripting with
Lua can greatly improve performance and can simplify the operations that you need
to perform.
