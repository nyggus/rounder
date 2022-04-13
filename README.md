# `rounding`: Rounding of numbers in complex Python objects

`rounding` is a lightweight module for rounding float numbers in complex structures, such as dictionaries, lists, tuples, and sets, and any complex object that combines them. The package is useful mainly for presentation purposes, but in some cases, it can be useful in other situations as well.

`rounding` offers you four functions for rounding complex objects:

* `round_object(x, digits=0, use_copy=False)`, which rounds to `digits` decimal places
* `floor_object(x, use_copy=False)`, which rounds to the nearest higher integer
* `ceil_object(x, use_copy=False)`, which rounds to the nearest lower integer
* `signif_object(x, digits, use_copy=False)`, which rounds to `digits` significant digits

but it offers also a function for rounding numbers:

* `signif(x, digits)`, which rounds `x` (either an int or a float) to `digits` significant digits

You can use `signif` in a simple way:

```python
>>> import rounding as r
>>> r.signif(1.1212, 3)
1.12
>>> r.signif(12.1239112, 5)
12.124
>>> r.signif(121212.12, 3)
121000.0

```

The package is simple to use, but you have to remember that when you're working with mutable objects, such as dicts or lists, rounding them for printing purposes will affect the original mutable structure. To overcome this effect, simply use `use_copy=True` in the above functions, which will first create a copy of the object and work (and return) its deepcopy, not the original object.

While you can use `rounding` functions for rounding floats, this does not make much sense, as they will be rather slolwer than other solutions. The package does not aim to help you round single values, but to help you out with rounding complex structures, which you would have to round element by element. 

You can round a list, a tuple, a set (including a frozenset), a float `array.array`, and a dict:

```python
>>> r.round_object([1.122, 2.4434], 1)
[1.1, 2.4]
>>> r.ceil_object([1.122, 2.4434])
[2, 3]
>>> r.floor_object([1.122, 2.4434])
[1, 2]
>>> r.signif_object([1.1224, 222.4434], 4)
[1.122, 222.4]

>>> r.round_object((1.122, 2.4434), 1)
(1.1, 2.4)
>>> r.round_object({1.122, 2.4434}, 1)
{1.1, 2.4}
>>> r.round_object({"1": 1.122, "q":2.4434}, 1)
{'1': 1.1, 'q': 2.4}

```

Do remember, however, that `array.array` works in its own way, so rounding its values is a tricky thing:

```python
>>> import array
>>> arr = array.array("f", (1.122, 2.4434))
>>> r.round_object(arr, 1) == array.array("f", (1.1, 2.4))
True

```

Perfect... But:

```python
>>> array.array("f", (1.1, 2.4))
array('f', [1.100000023841858, 2.4000000953674316])

```

and indeed:


```python
>>> r.round_object(arr, 1)
array('f', [1.100000023841858, 2.4000000953674316])

```

This is seldom what you want to achieve, so more often than not, before rounding an array, you should make it a list or a tuple:

```python
>>> r.round_object(list(arr), 1)
[1.1, 2.4]

```

Note that you do not have to worry about having non-roundable objects in a list (or whatever object you're feeding into `rounding` functions). Your objects can contain objects of any type, and only floats and complex numbers will be rounded while all others will be returned untouched:

```python
>>> r.round_object([1.122, "string", 2.4434, 2.45454545-2j], 1)
[1.1, 'string', 2.4, (2.5-2j)]

```

In fact, you can round any object, and the function will simply return it if it's non-roundable:

```python
>>> r.round_object("string")
'string'
>>> r.round_object(lambda x: x**3)(2)
8
>>> r.round_object(range(10))
range(0, 10)

```

But most of all, you can apply rounding for any complex object, of any structure. Imagine you have a structure like this:

```python
>>> x = {
...    "items": ["item 1", "item 2", "item 3",],
...    "quantities": {"item 1": 235, "item 2" : 300, "item 3": 17,},
...    "prices": {
...        "item 1": {"$": 32.22534554, "EURO": 41.783234567},
...        "item 2": {"$": 42.26625, "EURO": 51.333578},
...        "item 3": {"$": 2.223043225, "EURO": 2.78098721346}
...    },
...    "income": {
...        "2009": {"$": 3445342.324364, "EURO":   39080.332546},
...        "2010": {"$": 6765675.56665554, "EURO": 78980.34564546},
...    }
... }

```

Perhaps it does not make much sense, but the point is that to round all the values in this structure, you would need to build a dedicated script for that. With `rounding`, this is a piece of cake:

```python
>>> rounded_x = r.round_object(x, digits=2, use_copy=True)

```

And you will get this:

```python
>>> from pprint import pprint
>>> pprint(rounded_x)
{'income': {'2009': {'$': 3445342.32, 'EURO': 39080.33},
            '2010': {'$': 6765675.57, 'EURO': 78980.35}},
 'items': ['item 1', 'item 2', 'item 3'],
 'prices': {'item 1': {'$': 32.23, 'EURO': 41.78},
            'item 2': {'$': 42.27, 'EURO': 51.33},
            'item 3': {'$': 2.22, 'EURO': 2.78}},
 'quantities': {'item 1': 235, 'item 2': 300, 'item 3': 17}}

```

Piece of cake! Note that we used `use_copy=True`, which means that `rounded_x` is a deepcopy of `x`, so the original dictionary has not been affected anyway.

Of course, you can achieve it in the same way yourself, as the design of the code is not too complicated. All these functions use the same class, `Rounder`, which works recursively, that way looping over the whole object. At each step, it checks the type of an object it has stepped into. If it is a complex number or a float, it rounds it; if it is a non-roundable object, it returns it, and if it is a container, it iterates over it - and so on, until each elementary object is either rounded or not.


# Examples

First of all, all these functions will work the very same way as their original counterparts (not for `signif`, which does not have one):

```python
>>> import math
>>> x = 12345.12345678901234567890
>>> for d in range(10):
...     assert round(x, d) == r.round_object(x, d)
...     assert math.ceil(x) == r.ceil_object(x)
...     assert math.floor(x) == r.floor_object(x)

```

But please remember that the in-built `round` and `math`'s `ceil` and `floor` will be quicker than their `rounding` counterparts.

### Immutable types

> `rounding` does work with immutable types!

Yes, it does. Look:

```python
>>> x = {1.12, 4.555}
>>> r.round_object(x)
{1.0, 5.0}
>>> r.round_object(frozenset(x))
frozenset({1.0, 5.0})
>>> r.round_object((1.12, 4.555))
(1.0, 5.0)
>>> r.round_object(({1.1, 1.2}, frozenset({1.444, 2.222})))
({1.0}, frozenset({1.0, 2.0}))

```

Remember, however, that in the case of immutable types, `rounding` functions do not affect the original objects, but simply return new ones.

### Generators

As a rule, mainly for safety, generators are returned unchanged. This is a safe approach for the simple reason that you often choose to use a generator instead of, say, a list when the data you're processing can be too large for your machine's memory to handle. So:

```python
>>> gen = (i**2 for i in (.1, .33, .45))
>>> r.round_object(gen) is gen
True

```

You will get the same result for `range`:

```python
>>> ran = range(10)
>>> r.round_object(ran) is ran
True

```

### NumPy and Pandas

`rounding` does not work with `numpy` and `pandas`: they have their own in-built methods for rounding, and using them will be much quicker.