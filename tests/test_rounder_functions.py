import pytest
import rounder as r
import random
from copy import deepcopy
from math import ceil, floor

from rounder.rounder import map_object


def test_randomized_tests_round_ceil_floor_object(n, limits, digits_range):
    for _ in range(n):
        x = random.uniform(*limits)
        for digits in digits_range:
            assert round(x, digits) == r.round_object(x, digits)
            assert ceil(x) == r.ceil_object(x)
            assert floor(x) == r.floor_object(x)


def test_use_copy_with_lists_and_dicts():
    items = (
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
    )

    for x in items:
        x_rounder_copy = r.round_object(x, 1, True)
        assert x_rounder_copy != x
        x_rounder_no_copy = r.round_object(x, 1, False)
        assert x_rounder_no_copy == x_rounder_copy
        assert x_rounder_no_copy is not x_rounder_copy
        assert x_rounder_no_copy is x


def test_no_copy_with_lists_and_dicts():
    items = (
        [222.222, 333.333, 1.000045, "Shout Bamalama!"],
        {"a": 222.222, "b": 333.333, "c": 1.000045, "d": "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1)
        assert x_rounder is x


def test_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1, True)
        assert x_rounder is not x
        assert x_rounder != x


def test_no_copy_with_tuples_and_sets():
    items = (
        (222.222, 333.333, 1.000045, "Shout Bamalama!"),
        {222.222, 333.333, 1.000045, "Shout Bamalama!"},
    )

    for x in items:
        x_rounder = r.round_object(x, 1, False)
        assert x_rounder is not x
        assert x_rounder != x


def test_randomized_tests_using_copy_lists_tuples_sets(
    n, list_len, limits, digits_range
):
    for _ in range(n):
        for length in list_len:
            for digits in digits_range:
                for iter_type in (list, tuple, set):
                    x = iter_type(
                        random.uniform(*limits) for i in range(length)
                    )
                    x_copy = deepcopy(x)

                    r_rounded_x = r.round_object(x, digits, use_copy=True)
                    assert r_rounded_x != x

                    rounded_x = iter_type(round(x, digits) for x in x_copy)
                    assert r_rounded_x is not x
                    assert rounded_x == r_rounded_x

                    # use_copy was used, so the original list did not change:
                    # (here, this makes a difference for lists but not for
                    # sets and tuples)
                    if iter_type is list:
                        assert r_rounded_x != x
                        no_copy_r_rounded_x = r.round_object(
                            x, digits, use_copy=False
                        )
                        assert no_copy_r_rounded_x == r_rounded_x

                        # use_copy was NOT used, so the original list DID change:
                        assert r_rounded_x == x


def test_randomized_tests_using_copy_dicts(n, limits, digits_range):
    for _ in range(n):
        for digits in digits_range:
            for iter_type in (list, tuple, set):
                x = {
                    letter: random.uniform(*limits) for letter in "abcefghijk"
                }
                x_copy = deepcopy(x)

                r_rounded_x = r.round_object(x, digits, use_copy=True)
                assert r_rounded_x != x

                rounded_x = {
                    letter: round(x, digits) for letter, x in x_copy.items()
                }
                assert r_rounded_x is not x
                assert rounded_x == r_rounded_x

                # use_copy was used, so the original list did not change:
                assert r_rounded_x != x
                no_copy_r_rounded_x = r.round_object(x, digits, use_copy=False)
                assert no_copy_r_rounded_x == r_rounded_x

                # use_copy was NOT used, so the original list DID change:
                assert r_rounded_x == x


def test_with_non_roundable_items():
    assert r.round_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.ceil_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.floor_object("Shout Bamalama!") == "Shout Bamalama!"
    assert r.signif_object("Shout Bamalama!", 5) == "Shout Bamalama!"


def test_with_non_roundable_items_lists():
    assert r.round_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.ceil_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.floor_object(["Shout Bamalama!"]) == ["Shout Bamalama!"]
    assert r.signif_object(["Shout Bamalama!"], 5) == ["Shout Bamalama!"]


def test_with_non_roundable_items_tuples():
    assert r.round_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.ceil_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.floor_object(("Shout Bamalama!")) == ("Shout Bamalama!")
    assert r.signif_object(("Shout Bamalama!"), 5) == ("Shout Bamalama!")


def test_with_non_roundable_items_sets():
    assert r.round_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.ceil_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.floor_object({"Shout Bamalama!"}) == {"Shout Bamalama!"}
    assert r.signif_object({"Shout Bamalama!"}, 5) == {"Shout Bamalama!"}


def test_with_non_roundable_items_dicts():
    assert r.round_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.ceil_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.floor_object({"phrase": "Shout Bamalama!"}) == {
        "phrase": "Shout Bamalama!"
    }
    assert r.signif_object({"phrase": "Shout Bamalama!"}, 5) == {
        "phrase": "Shout Bamalama!"
    }


def test_round_object_for_complex_object(complex_object):
    rounded_complex_object = r.round_object(complex_object, 3, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.222
    assert rounded_complex_object["e"] == {
        "ea": 0.023,
        "eb": {1.333, 2.999},
        "ec": {"eca": 1.566, "ecb": 1.766},
    }
    assert rounded_complex_object["d"] == [1.123, 0.023]


def test_ceil_object_for_complex_object(complex_object):
    rounded_complex_object = r.ceil_object(complex_object, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 13
    assert rounded_complex_object["e"] == {
        "ea": 1,
        "eb": {2, 3},
        "ec": {"eca": 2, "ecb": 2},
    }
    assert rounded_complex_object["d"] == [2, 1]


def test_floor_object_for_complex_object(complex_object):
    rounded_complex_object = r.floor_object(complex_object, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12
    assert rounded_complex_object["e"] == {
        "ea": 0,
        "eb": {1, 2},
        "ec": {"eca": 1, "ecb": 1},
    }
    assert rounded_complex_object["d"] == [1, 0]


def test_signif_object_for_complex_object_3_digits(complex_object):
    rounded_complex_object = r.signif_object(complex_object, 3, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.2
    assert rounded_complex_object["e"] == {
        "ea": 0.0227,
        "eb": {1.33, 3.0},
        "ec": {"eca": 1.57, "ecb": 1.77},
    }
    assert rounded_complex_object["d"] == [1.12, 0.0235]


def test_signif_object_for_complex_object_5_digits(complex_object):
    rounded_complex_object = r.signif_object(complex_object, 4, use_copy=True)
    assert rounded_complex_object is not complex_object
    assert rounded_complex_object["a"] == 12.22
    assert rounded_complex_object["e"] == {
        "ea": 0.02273,
        "eb": {1.333, 2.999},
        "ec": {"eca": 1.566, "ecb": 1.766},
    }
    assert rounded_complex_object["d"] == [1.123, 0.02349]


def test_for_complex_numbers():
    assert r.round_object(1.934643 - 2j, 2) == 1.93 - 2j
    assert r.ceil_object(1.934643 - 2j) == 2 - 2j
    assert r.floor_object(1.934643 - 2j) == 1 - 2j
    assert r.signif_object(1.934643 - 2j, 5) == 1.9346 - 2j


def test_signif_floats():
    assert r.signif(1.444555, 1) == 1.0
    assert r.signif(1.444555, 2) == 1.4
    assert r.signif(1.444555, 3) == 1.44
    assert r.signif(1.444555, 4) == 1.445
    assert r.signif(1.444555, 5) == 1.4446
    assert r.signif(1.444555, 6) == 1.44456
    assert r.signif(1.444555, 7) == 1.444555
    assert r.signif(1.444555, 8) == 1.444555


def test_signif_ints():
    assert r.signif(1444555, 1) == 1000000
    assert r.signif(1444555, 2) == 1400000
    assert r.signif(1444555, 3) == 1440000
    assert r.signif(1444555, 4) == 1445000
    assert r.signif(1444555, 5) == 1444600
    assert r.signif(1444555, 6) == 1444560
    assert r.signif(1444555, 7) == 1444555
    assert r.signif(1444555, 8) == 1444555


def test_signif_exception():
    with pytest.raises(r.NonNumericTypeError):
        r.signif("string", 3)

    with pytest.raises(r.NonNumericTypeError):
        r.signif([2.12], 3)

    with pytest.raises(r.NonNumericTypeError):
        r.signif((1,), 3)


def test_with_unpickable_objects():
    gen = (i ** 2 for i in range(10))
    with pytest.raises(r.UnpickableObjectError):
        _ = r.round_object(gen, use_copy=True)
    _ = r.round_object(gen, use_copy=False)


def test_with_callable():
    f = lambda x: x
    assert callable(r.round_object(f))

    def f():
        pass

    x = {"items": [1.1222, 1.343434], "function": f}
    assert callable(x["function"])

    x_rounded = r.round_object(x, 2, use_copy=True)
    assert callable(x_rounded["function"])

    x_ceil = r.ceil_object(x, use_copy=True)
    assert callable(x_ceil["function"])

    x_floor = r.floor_object(x, use_copy=True)
    assert callable(x_floor["function"])

    x_signif = r.signif_object(x, 3, use_copy=True)
    assert callable(x_signif["function"])


def test_map_object_basic():
    x = [1.12, 1.13]
    assert r.map_object(lambda x: x, x, False) is x
    assert r.map_object(lambda x: x, x, True) is not x
    assert r.map_object(lambda x: x, x, True) == x


def test_map_object_exception():
    with pytest.raises(r.NonCallableError):
        r.map_object(2, 2)
    with pytest.raises(r.NonCallableError):
        r.map_object((lambda x: x)(2), 2)
    with pytest.raises(r.NonCallableError):
        r.map_object([], [2, 2])


def test_map_object_dicts_lists():
    obj = {
        "list": [1.44, 2.67, 3.334, 6.665],
        "main value": 5.55,
        "explanation": "to be filled in",
    }
    negative_reversed_obj = r.signif_object(
        r.map_object(lambda x: -1 / x, obj, True), 5
    )
    assert negative_reversed_obj == {
        "list": [-0.69444, -0.37453, -0.29994, -0.15004],
        "main value": -0.18018,
        "explanation": "to be filled in",
    }


def test_map_object_squared(complex_object):
    squared_complex_object = r.round_object(
        r.map_object(lambda x: x * x, complex_object, True), 3
    )
    assert squared_complex_object["a"] == 149.382
    assert squared_complex_object["e"] == {
        "ea": 0.001,
        "eb": {8.994, 1.777},
        "ec": {"eca": 2.451, "ecb": 3.118},
    }
    assert squared_complex_object["d"] == [1.262, 0.001]
