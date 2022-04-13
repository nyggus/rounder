import array
from copy import deepcopy
from easycheck import check_argument, check_if
from math import ceil as orig_ceil
from math import floor as orig_floor
from math import log10, pow


orig_round = round


class RoundingError(Exception):
    """Exception class to be used across the package."""

    pass


class Rounder:
    """Callable class for rounding complex objects in Python.
    
    The class is not experted with the package, and is not to be used by
    the user. Instead, four functions that run the class should be used:
    round_object(), floor_object(), ceil_object() and signif_object().
    """
    def __init__(self, x, digits=0, method="round"):
        self.x = x
        self.digits = digits
        self.method = method
        self._check_args()

    def _check_args(self):
        check_if(
            self.digits >= 0,
            handle_with=RoundingError,
            message="Argument digits must be 0 or bigger.",
        )
        check_argument(
            self.method,
            "method",
            expected_instance=str,
            expected_choices=("round", "ceil", "floor", "signif"),
            handle_with=RoundingError,
        )

    def run_method(self):
        if self.method == "round":
            return orig_round(self.x, self.digits)
        elif self.method == "floor":
            return orig_floor(self.x)
        elif self.method == "ceil":
            return orig_ceil(self.x)
        elif self.method == "signif":
            return signif(self.x, self.digits)

    def run_method_for_complex_number(self):
        if self.method == "round":
            return (
                orig_round(self.x.real, self.digits)
                + orig_round(self.x.imag, self.digits) * 1j
            )
        elif self.method == "floor":
            return orig_floor(self.x.real) + orig_floor(self.x.imag) * 1j
        elif self.method == "ceil":
            return orig_ceil(self.x.real) + orig_ceil(self.x.imag) * 1j
        elif self.method == "signif":
            return (
                signif(self.x.real, self.digits)
                + signif(self.x.imag, self.digits) * 1j
            )

    def __call__(self):
        if isinstance(self.x, int) and self.method == "signif":
            return int(self.run_method())
        if isinstance(self.x, (int, str)):
            return self.x
        elif isinstance(self.x, complex):
            return self.run_method_for_complex_number()
        elif isinstance(self.x, float):
            return self.run_method()
        elif isinstance(self.x, dict):
            for k, v in self.x.items():
                self.x[k] = Rounder(v, self.digits, self.method)()
        elif isinstance(self.x, array.array):
            if self.x.typecode == "f":
                list_x = list(self.x)
                for i, v in enumerate(self.x):
                    list_x[i] = Rounder(v, self.digits, self.method)()
                self.x = array.array("f", list_x)
        elif isinstance(self.x, tuple):
            list_x = list(self.x)
            for i, v in enumerate(list_x):
                list_x[i] = Rounder(v, self.digits, self.method)()
            self.x = tuple(list_x)
        elif isinstance(self.x, set):
            list_x = list(self.x)
            for i, v in enumerate(list_x):
                list_x[i] = Rounder(v, self.digits, self.method)()
            self.x = set(list_x)
        elif isinstance(self.x, frozenset):
            list_x = list(self.x)
            for i, v in enumerate(list_x):
                list_x[i] = Rounder(v, self.digits, self.method)()
            self.x = frozenset(list_x)
        elif isinstance(self.x, list):
            for i, v in enumerate(self.x):
                self.x[i] = Rounder(v, self.digits, self.method)()
        return self.x


def round_object(x, digits=0, use_copy=False):
    """Round numbers in a Python object.
    
    Args:
        x (any): any Python object
        digits (int, optional): number of digits. Defaults to 0.
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affected inplace. In the case of
            unpickable objects, TypeError will be raised.

    Returns:
        any: the object with values rounded to requested number of digits
    
    >>> round_object(12.12, 1)
    12.1
    >>> round_object("string", 1)
    'string'
    >>> round_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> round_object(obj, 2)
    {'number': 12.32, 'string': 'whatever', 'list': [122.45, 0.01]}
    """
    y = deepcopy(x) if use_copy else x
    return Rounder(y, digits, method="round")()


def floor_object(x, use_copy=False):
    """Round numbers in a Python object, using the floor algorithm.
    
    This means rounding to the closest smaller integer.
    
    Args:
        x (any): any Python object
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.

    Returns:
        any: the object with values floor-rounded to requested number of
            digits
    
    >>> floor_object(12.12)
    12
    >>> floor_object("string")
    'string'
    >>> floor_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> floor_object(obj)
    {'number': 12, 'string': 'whatever', 'list': [122, 0]}
    """
    y = deepcopy(x) if use_copy else x
    return Rounder(y, 0, method="floor")()


def ceil_object(x, use_copy=False):
    """Round numbers in a Python object, using the ceiling algorithm.
    
    This means rounding to the closest greater integer.
    
    Args:
        x (any): any Python object
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.

    Returns:
        any: the object with values ceiling-rounded to requested number of digits
    
    >>> ceil_object(12.12)
    13
    >>> ceil_object("string")
    'string'
    >>> ceil_object(["Shout", "Bamalama"])
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> ceil_object(obj)
    {'number': 13, 'string': 'whatever', 'list': [123, 1]}"""
    y = deepcopy(x) if use_copy else x
    return Rounder(y, 0, method="ceil")()


def signif_object(x, digits, use_copy=False):
    """Round numbers in a Python object to requested significant digits.
    
    Args:
        x (any): any Python object
        digits (int, optional): number of digits.
        use_copy (bool, optional): use a deep copy or work with the original
            object? Defaults to False, in which case mutable objects (a list
            or a dict, for instance) will be affect inplace.

    Returns:
        any: the object with values rounded to requested number of significant
            digits
    
    >>> signif_object(12.12, 3)
    12.1
    >>> signif_object(.1212, 3)
    0.121
    >>> signif_object(.00001212, 3)
    1.21e-05
    >>> signif_object(.00001219, 3)
    1.22e-05
    >>> signif_object(1212.0, 3)
    1210.0
        
    >>> signif_object("string", 1)
    'string'
    >>> signif_object(["Shout", "Bamalama"], 5)
    ['Shout', 'Bamalama']
    >>> obj = {'number': 12.323, 'string': 'whatever', 'list': [122.45, .01]}
    >>> signif_object(obj, 3)
    {'number': 12.3, 'string': 'whatever', 'list': [122.0, 0.01]}
    """
    y = deepcopy(x) if use_copy else x
    return Rounder(y, digits, method="signif")()


def signif(x, digits=3):
    """Round number to significant digits.

    Translated from Java algorithm available on
    <a href="http://stackoverflow.com/questions/202302">Stack Overflow</a>

    Args:
        x (float, int): a value to be rounded
        digits (int, optional): number of significant digits. Defaults to 3.

    Returns:
        float or int: x rounded to significant digits

    >>> signif(1.2222, 3)
    1.22
    >>> signif(12222, 3)
    12200.0
    >>> signif(1, 3)
    1.0
    >>> signif(123.123123, 5)
    123.12
    >>> signif(123.123123, 3)
    123.0
    >>> signif(123.123123, 1)
    100.0
    """
    if x == 0:
        return 0
    try:
        x = float(x)
    except (TypeError, ValueError):
        raise TypeError(
            f"x must be an int or a float, not '{type(x).__name__}'"
        )
    d = orig_ceil(log10(-x if x < 0 else x))
    power = digits - d
    magnitude = pow(10, power)
    shifted = orig_round(x * magnitude)
    return shifted / magnitude


if __name__ == "__main__":
    import doctest

    doctest.testmod()
