container sequences

list, tuple, collections.deque

flat sequences:
str, bytes, array.array

container sequences can hold objects of different types, eg. [9.46, 'cat', [2.08, 4.29]]

flat sequences are more compact

in python each object has a header, so a array of float is more compact than
a tuple of floats

## Mutability

some sequences are mutable
list bytearray array.array collections.deque

some are not:
tuple, str, bytes


## Generator expression and list comprehension


x = 'abc'
codes = [ord(x) for x in x]

the x is a new variable scoped within the expression, not accessible from outside

tuple(ord(symbol) for symbol in symbols)

generator expression yields one item at
a time, it does not build a list beforehand, which is good for for loops

## Tuple

Tuples are not just immutable 
but tuples can be used as records, in that case, position of each item in the tuple matters

immutable: the reference cannot be changed, but if the object is a mutable type, that can change

tuples of mutable items can be a source of bugs

given a tuple t, tuple(t) just gives the same reference, won't copy, but a list will 

## unpacking sequences and iterables

lat, long = (33.925, -118.408)

t = (20, 8)
divmod(*t)

a, *body, c, d = range(5)
>>> (0, [1, 2], 3, 4)

*sequence is another type of unpacking

nested unpacking:

[[field]] = query_returning_single_row_with_single_field()

## Pattern matching

with the very powerful match keyword

match subject:
    case [..., ..., ...]:
        ...

def handle_command(self, message):
        match message:  1
            case ['BEEPER', frequency, times]:  2
                self.beep(times, frequency)
            case ['NECK', angle]:  3
                self.rotate_neck(angle)
            case ['LED', ident, intensity]:  4
                self.leds[ident].set_brightness(ident, intensity)
            case ['LED', ident, red, green, blue]:  5
                self.leds[ident].set_color(ident, red, green, blue)
            case _:  6
                raise InvalidCommand(message)

the first match case mean the first string must be 'BEEPER' to match the row
destructing.
you can specify type for destructing:
[str(name), _, _, (float(lat), float(lon))]

## Slicing

the syntax:
seq[start:stop:step]

l[:2] index 0 and 1
l[2:] index starting at 2

s[::3] skip three items , negative代表从后往前
s = 'bicycle'
s[::3] # 'bye'
s[::-1] # 'elcycib'
s[::-2] # 'eccb'

slice objects
example: slice(0, 6)

assigning to slices

l = list(range(10))

l[2:5] = [20, 30]
[0, 1, 20, 30, 5, 6, 7, 8, 9]

when the target of assignment is a slice, the righthand side must be  an iterable object

## Using + and * with Sequences

>>> l = [1, 2, 3]
>>> l * 5
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> 5 * 'abcd'
'abcdabcdabcdabcdabcd'

+ and * always create a new object, but never change their operands

beware of using * when the sequence contains mutable items, they may cause references to 
the same object

+= and *= methods
their implementation depends on the __iadd__ and __imul__ methods, inplace add and multiplication, if these methods are implemented, then 

lessons:

1. avoid putting mutable objects (like lists) in tuples
2. Augmented assignment is not an atomic operation
3. Inspecting python bytecode is not too difficult, and can be helpful to see what is going on under the hood

## Sorting: list.sort() versus the sorted built-in

list.sort sort inplace, returning None, does not create a new list
sorted() create a new list and returns it

remember to use `key` parameter when you want to customize you sorting strategy

## Other types

array.array

if a list only contains numbers, an array.array is more efficient

memory views: shares memory with sequences without copying bytes

>>> from array import array
>>> octets = array('B', range(6))  1
>>> m1 = memoryview(octets)  2
>>> m1.tolist()
[0, 1, 2, 3, 4, 5]
>>> m2 = m1.cast('B', [2, 3])  3
>>> m2.tolist()
[[0, 1, 2], [3, 4, 5]]
>>> m3 = m1.cast('B', [3, 2])  4
>>> m3.tolist()
[[0, 1], [2, 3], [4, 5]]
>>> m2[1,1] = 22  5
>>> m3[1,1] = 33  6
>>> octets  7
array('B', [0, 1, 2, 33, 22, 5])

assignment to memoryview will actually change the underlying array

## Numpy

## deque

if you want fifo and operation on both ends, use a deque

there are other python standard libraries that implement queues
queue
multiprocessing: SimpleQueue
asyncio
heapq