# `rounder`: Rounding of numbers in complex Python objects

`rounder` is a lightweight package for rounding float numbers in complex structures, such as dictionaries, lists, tuples, and sets, and any complex object that combines any number of such objects in any nested structure. The code is organized as a Python (Python >= 3.6 is required) package that can be installed from PyPi (`pip install rounder`), but as it is a one-file package, you can simply download the main module ([rounder.py](rounder/rounder.py)) and use it directly in your project.

The package is useful mainly for presentation purposes, but in some cases, it can be useful in other situations as well.

`rounder` offers you four functions for rounding complex objects:

* `round_object(obj, digits=0, use_copy=False)`, which rounds `x` to `digits` decimal places
* `floor_object(obj, use_copy=False)`, which rounds `x` down to the nearest integer
* `ceil_object(obj, use_copy=False)`, which rounds `x` up to the nearest integer
* `signif_object(obj, digits, use_copy=False)`, which rounds `x` to `digits` significant digits

In addition, `rounder` comes with a generalized function:

* `map_obj(func, obj, use_copy=False)`, which runs callable `func`, which takes a number as an argument and returns a number, to all numbers across the object.

`rounder` also offers a function for rounding numbers to significant digits:

* `signif(x, digits)`, which rounds `x` (either an int or a float) to `digits` significant digits

You can use `signif` in a simple way:

```python
>>> import rounder as r
>>> r.signif(1.1212, 3)
1.12
>>> r.signif(12.1239112, 5)
12.124
>>> r.signif(121212.12, 3)
121000.0

```

The package is simple to use, but you have to remember that when you're working with mutable objects, such as dicts or lists, rounding them for printing purposes will affect the original object; no such effect, of course, will occur for immutable types (e.g., tuples and sets). To overcome this effect, simply use `use_copy=True` in the above functions for rounding objects (not in `signif`). If you do so, the function will create a copy of the object and work (and return) its deepcopy, not the original object.

You can use `rounder` functions for rounding floats, but do remember that their behavior is slightly different than that of their `builtin` and `math` counterparts, as they do not throw an exception when a non-number object is used.

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

This is seldom what you want to achieve when rounding numbers, so more often than not, before rounding an array, you should make it a list or a tuple:

```python
>>> arr = array.array("d", (1.122, 2.4434))
>>> r.round_object(arr, 1)
array('d', [1.1, 2.4])

```

Note that you do not have to worry about having non-roundable objects in a list (or whatever object you're feeding into `rounder` functions). Your objects can contain objects of any type, and only numbers will be rounded while all others will be remain untouched:

```python
>>> r.round_object([1.122, "string", 2.4434, 2.45454545-2j], 1)
[1.1, 'string', 2.4, (2.5-2j)]

```

In fact, you can round any object, and the function will simply return it if it cannot be rounded:

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
...     "items": ["item 1", "item 2", "item 3",],
...     "quantities": {"item 1": 235, "item 2" : 300, "item 3": 17,},
...     "prices": {
...         "item 1": {"$": 32.22534554, "EURO": 41.783234567},
...         "item 2": {"$": 42.26625, "EURO": 51.333578},
...         "item 3": {"$": 2.223043225, "EURO": 2.78098721346}
...     },
...     "income": {
...         "2009": {"$": 3445342.324364, "EURO":   39080.332546},
...         "2010": {"$": 6765675.56665554, "EURO": 78980.34564546},
...     }
... }

```

Perhaps it does not make much sense, but the point is that to round all the values in this structure, you would need to build a dedicated script for that. With `rounder`, this is a piece of cake:

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


### `map_object`

In addition, `rounder` offers you a `map_object()` function, which enables you to run any function that takes a number and returns a number for all numbers in an object. This works like the following:

```python
>>> xy = {"x": [12, 33.3, 45.5, 3543.22], "y": [.45, .3554, .55223, .9911], "expl": "x and y values"}
>>> r.round_object(r.map_object(lambda x: x**3/(1 - 1/x), xy, use_copy=True), 4, use_copy=True)
{'x': [1885.0909, 38069.258, 96313.1475, 44495587353.9829], 'y': [-0.0746, -0.0248, -0.2077, -108.4126], 'expl': 'x and y values'}

```

You would have achieved the same result had you used `round` inside the `lambda` body:

```python
>>> r.map_object(lambda x: round(x**3/(1 - 1/x), 4), xy, use_copy=True)
{'x': [1885.0909, 38069.258, 96313.1475, 44495587353.9829], 'y': [-0.0746, -0.0248, -0.2077, -108.4126], 'expl': 'x and y values'}

```

The latter approach, actually, will be quicker, as the full recursion is used just once, not twice, as it was done in the former example.


If the function takes additional arguments, you can use a wrapper function to overcome this issue:

```python
>>> def forget(something): pass
>>> def fun(x, to_forget):
...     forget(to_forget)
...     return x**2
>>> def wrapper(x):
...     return fun(x, "this can be forgotten")
>>> r.map_object(wrapper, [2, 2, [3, 3, ], {"a": 5}])
[4, 4, [9, 9], {'a': 25}]

```

Or even:

```python
>>> r.map_object(lambda x: fun(x, "this can be forgotten"), [2, 2, [3, 3, ], {"a": 5}])
[4, 4, [9, 9], {'a': 25}]

```

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

### Immutable types

`rounder` does work with immutable types! It simply creates a new object, with rounded numbers:

```python
>>> x = {1.12, 4.555}
>>> r.round_object(x)
{1, 5}
>>> r.round_object(frozenset(x))
frozenset({1, 5})
>>> r.round_object((1.12, 4.555))
(1, 5)
>>> r.round_object(({1.1, 1.2}, frozenset({1.444, 2.222})))
({1}, frozenset({1, 2}))

```

Remember, however, that in the case of sets, you can get a shorter set then the original one:

```python
>>> x = {1.12, 1.99}
>>> r.ceil_object(x)
{2}

```


### Generators and other unpickable objects

This should be an extremely rare situation to request to round an object that contains a generator, or any other unpickable object. But if you happen to be in such a situation, be aware of some limitations of `rounder` functions.

As a rule, mainly for safety, generators are returned unchanged. This is a safe approach for the simple reason that you often choose to use a generator instead of, say, a list when the data you're processing can be too large for your machine's memory to handle. So:

```python
>>> gen = (i**2 for i in range(10))
>>> rounded_gen = r.round_object(gen)
>>> rounded_gen is gen
True
>>> next(gen)
0
>>> next(gen)
1
>>> next(rounded_gen)
4

```

You will get the same result for `range`:

```python
>>> ran = range(10)
>>> r.round_object(ran) is ran
True

```

But you have to remember that when you request a deepcopy (with `use_copy=True`), all elements to be rounded need to be pickable:

```python
>>> gen_2 = (i**2 for i in range(10))
>>> gen_2_copied_rounded = r.round_object(gen_2, use_copy=True)
Traceback (most recent call last):
    ...
rounder.rounder.UnpickableObjectError

```

`range()` is pickable, so you can request a deepcopy of it in `rounder` functions. 

This is a rare situation, however, to include such objects in an object to be rounded. Remember about the above limitations, and you can either work with the original object (not its copy, so with default `use_copy=False`), or change it so that all its elements can be pickled.


### NumPy and Pandas

`rounder` does not work with `numpy` and `pandas`: they have their own builtin methods for rounding, and using them will be much quicker.


## Testing

The package is covered with unit `pytest`s, located in the tests/ folder. In addition, the package uses `doctest`s, which are collected here, in this README, and in the main module, [rounder.py](rounder/rounder.py). These `doctest`s serve mainly documentation purposes, and since they can be run any time during development and before with each release, this helps to check whether all the examples work fine.


## OS

The package is OS-independent. Its releases are checked in local machines, on Windows 10 and Ubuntu 20.04 for Windows, and in Pythonista for iPad.
