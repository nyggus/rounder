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
    def __init__(self, x, digits=0, method="round"):
        self.x = x
        self.digits = digits
        self.method = method
        self._check_args()

    def _check_args(self):
        check_if(
            self.digits >= 0,
            handle_with=RoundingError,
            message="Argument digits must be 0 or bigger."
        )
        check_argument(
            self.method, "method",
            expected_instance=str,
            expected_choices=("round", "ceil", "floor", "signif"),
            handle_with=RoundingError
        )
        
    
    def run_method(self):
        if self.method == "round":
            return orig_round(self.x, self.digits)
        elif self.method == "floor":
            return orig_floor(self.x)
        elif self.method == "ceil":
            return orig_ceil(self.x)
        elif self.method == "signif":
            return self.signif_object(self.x)
    
    
    def run_method_for_complex_number(self):
        if self.method == "round":
            return (
                orig_round(self.x.real, self.digits)
                + orig_round(self.x.imag, self.digits) * 1j
            )
        elif self.method == "floor":
            return (
                orig_floor(self.x.real)
                + orig_floor(self.x.imag) * 1j
            )
        elif self.method == "ceil":
            return (
                orig_ceil(self.x.real)
                + orig_ceil(self.x.imag) * 1j
            )
        elif self.method == "signif":
            return (
                self.signif_object(self.x.real)
                + orig_round(self.x.imag) * 1j
            )
        
    def signif_object(self, x):
        """
        Translated from Java algorithm available on
        <a href="http://stackoverflow.com/questions/202302">Stack Overflow</a>"""
        if x == 0:
            return 0
        x = float(x)
        d = orig_ceil(log10(-x if x < 0 else x))
        power = self.digits - d
        magnitude = pow(10, power)
        shifted = orig_round(x * magnitude);
        return shifted/magnitude
        
    def __call__(self):
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
                    #breakpoint()
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
    y = deepcopy(x) if use_copy else x
    return Rounder(y, digits, method="round")()



def floor_object(x, use_copy=False):
    y = deepcopy(x) if use_copy else x
    return Rounder(y, 0, method="floor")()


def ceil_object(x, use_copy=False):
    y = deepcopy(x) if use_copy else x
    return Rounder(y, 0, method="ceil")()


def signif_object(x, digits, use_copy=False):
    y = deepcopy(x) if use_copy else x
    return Rounder(y, digits, method="signif")()


signif = signif_object

if __name__ == "__main__":
    import doctest
    doctest.testmod()