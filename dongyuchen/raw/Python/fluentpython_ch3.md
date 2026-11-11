# Dictionaries and sets

hashtable is behind the dict engines, high performance
set and frozenset --> based on hashtable

## Modern dict syntax

dict comprehension

>>> dial_codes = [                                                  1
...     (880, 'Bangladesh'),
...     (55,  'Brazil'),
...     (86,  'China'),
...     (91,  'India'),
...     (62,  'Indonesia'),
...     (81,  'Japan'),
...     (234, 'Nigeria'),
...     (92,  'Pakistan'),
...     (7,   'Russia'),
...     (1,   'United States'),
... ]
>>> country_dial = {country: code for code, country in dial_codes}  2
>>> country_dial
{'Bangladesh': 880, 'Brazil': 55, 'China': 86, 'India': 91, 'Indonesia': 62,
'Japan': 81, 'Nigeria': 234, 'Pakistan': 92, 'Russia': 7, 'United States': 1}
>>> {code: country.upper()                                          3
...     for country, code in sorted(country_dial.items())
...     if code < 70}
{55: 'BRAZIL', 62: 'INDONESIA', 7: 'RUSSIA', 1: 'UNITED STATES'}

unpacking mappings

>>> def dump(**kwargs):
...     return kwargs
...
>>> dump(**{'x': 1}, y=2, **{'z': 3})
{'x': 1, 'y': 2, 'z': 3}

** can occur multiple times, duplicate keys are allowed and later occurrences overwrite previous ones

merge mappings with | and |=

## Pattern matching with mapping

def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:  1
            return names
        case {'type': 'book', 'api': 1, 'author': name}:  2
            return [name]
        case {'type': 'book'}:  3
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:  4
            return [name]
        case _:  5
            raise ValueError(f'Invalid record: {record!r}')

order of the keys in the pattern is irrelevant

## Standard API of mapping types

isinstance(my_dict, abc.Mapping)

what is hashable:
__hash__() method which value never changes during its lifetime
__eq__() methoc which can compare with other objects of the same type
hashable objects which compare equal must have the same hash code.

numeric types and str bytes are all hashable
container types are hashable if they are immutable and contained objects that are also hashable

>>> tt = (1, 2, (30, 40))
>>> hash(tt)
8027212646858338501
>>> tl = (1, 2, [30, 40])
>>> hash(tl)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> tf = (1, 2, frozenset([30, 40]))
>>> hash(tf)
-4118419923444501110

d.get(k, default) is an alternative to d[k] if you want to always have a default value rather than handling keyError

dict.setdefault(key, default_value) -> returns the default value, you can chain elements

## Automatic handling of missing keys

1. defaultdict: create a default value when the key does not exist

the callable that produces the default value is held in an instance attribute named default_factory

default_factory is only invoked to provide default values for __getitem__ calls, and not for other methods

__missing__ special method makes this defaultdict work by calling default_factory

class StrKeyDict0(dict):  1

    def __missing__(self, key):
        if isinstance(key, str):  2
            raise KeyError(key)
        return self[str(key)]  3

    def get(self, key, default=None):
        try:
            return self[key]  4
        except KeyError:
            return default  5

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys() 

StrKeyDict0 uses __missing__ to convert a value to str and then search again, so code like d['4'] and d[4] both works

get --> __getitem__ --> __missing__ --> fail? KeyError, return default value

the __contains__ method should also consider to align with the logic defined in __missing__ method

if you want to customize a dict, inherit the collections.UserDict 

## Variations of dict

collections.OrderedDict # implemented with trees
collections.ChainMap: holds a list of mappings that can be searched as one, and succeeds as soon as the key is found in one of those mappings
collections.Counter

import collections


class StrKeyDict(collections.UserDict):  1

    def __missing__(self, key):  2
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data  3

    def __setitem__(self, key, item):
        self.data[str(key)] = item   4

UserDict has an internal dict instance called `data` which holds the actual items

UserDict extends abc.MutableMapping

MutableMapping.update: used by __init__, it uses self[key] = value to add items, and ends up calling our implementation of __setitem__

Mapping.get: UserDict already has implementation

## Immutable Mappings

MappingProxyType: builds a read-only mappingProxy instance from a dict, you cannot update its elements

## Dictionary Views

dict.keys() .values() .items() return instances of classes called dict_keys dict_values and dict_items respectively, thetse dictionary views are read-only projections of the internal data structures

views are a proxy, if the source is changed, you can immediately see the view change

## Practical consequences of how dict works

takeaway: to save memory, avoid creating instance attributes outside of the __init__ method

## Sets

the first usage of sets is to dedup

>>> l = ['spam', 'spam', 'eggs', 'spam', 'bacon', 'eggs']
>>> set(l)
{'eggs', 'spam', 'bacon'}
>>> list(set(l))
['eggs', 'spam', 'bacon']

set elements must be hashable

set operations:

a | b union
a & b intersection
a - b difference
a ^ b symmetric difference

found = len(needles & haystack) # find the count of needles in the haystack

Any one of the preceding examples are capable of searching 1,000 elements in a haystack of 10,000,000 items in about 0.3 milliseconds—that’s close to 0.3 microseconds per element.

set literal: {1, 2, 3}: python uses BUILD_SET bytecode, so it is faster


## Chapter Summary

Dictionaries are a keystone of Python. Over the years, the familiar {k1: v1, k2: v2} literal syntax was enhanced to support unpacking with **, pattern matching, as well as dict comprehensions.

Beyond the basic dict, the standard library offers handy, ready-to-use specialized mappings like defaultdict, ChainMap, and Counter, all defined in the collections module. With the new dict implementation, OrderedDict is not as useful as before, but should remain in the standard library for backward compatibility—and has specific characteristics that dict doesn’t have, such as taking into account key ordering in == comparisons. Also in the collections module is the UserDict, an easy to use base class to create custom mappings.

Two powerful methods available in most mappings are setdefault and update. The setdefault method can update items holding mutable values—for example, in a dict of list values—avoiding a second search for the same key. The update method allows bulk insertion or overwriting of items from any other mapping, from iterables providing (key, value) pairs, and from keyword arguments. Mapping constructors also use update internally, allowing instances to be initialized from mappings, iterables, or keyword arguments. Since Python 3.9, we can also use the |= operator to update a mapping, and the | operator to create a new one from the union of two mappings.

A clever hook in the mapping API is the __missing__ method, which lets you customize what happens when a key is not found when using the d[k] syntax that invokes __getitem__.

The collections.abc module provides the Mapping and MutableMapping abstract base classes as standard interfaces, useful for runtime type checking. The MappingProxyType from the types module creates an immutable façade for a mapping you want to protect from accidental change. There are also ABCs for Set and MutableSet.

Dictionary views were a great addition in Python 3, eliminating the memory overhead of the Python 2 .keys(), .values(), and .items() methods that built lists duplicating data in the target dict instance. In addition, the dict_keys and dict_items classes support the most useful operators and methods of frozenset