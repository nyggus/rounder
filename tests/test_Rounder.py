import array
import pytest
from rounding.rounding import Rounder, RoundingError

def test_basic_Rounder(methods, digits_range):
    rer = Rounder("10", digits=2, method="round")
    for method in methods:
        for digit in digits_range:
            rer.method = method
            assert rer() == "10"


def test_Rounder_incorrect_method():
    with pytest.raises(RoundingError, match="method's value, Bum bamabama"):
        Rounder("10", digits=2, method="Bum bamabama")()


def test_Rounder_with_callable():
    f = lambda x: x
    assert Rounder(f)() == f
    assert Rounder(f)()(1) == 1


def test_Rounder_with_bool():
    assert Rounder(True)()
    assert not Rounder(False)()


def test_Rounder_with_generator():
    gen = (i**2 for i in (.1, .33, .45))
    assert Rounder(gen)() is gen


def test_Rounder_with_range():
    ran = range(10)
    assert Rounder(ran)() is ran


def test_Rounder_frozenset():
    x = frozenset((1.22, 2.22, 3.22))
    assert Rounder(x)() == frozenset({1, 2, 3})
    
    
def test_Rounder_bytes():
    x = b"Shout Bamalama!"
    assert Rounder(x)() == b"Shout Bamalama!"


def test_Rounder_bytearray():
    x = bytearray.fromhex('2Ef0 F1f2  ')
    assert Rounder(x)() == bytearray(b'.\xf0\xf1\xf2')


def test_Rounder_memoryview():
    x = memoryview(b"Shout Bamalama!")
    assert Rounder(x)() == b"Shout Bamalama!"
    

def test_Rounder_array_array():
    x = array.array("f", [1.12, 2.222, 3.123])
    assert Rounder(x, 1)() == array.array("f", [1.1, 2.2, 3.1])