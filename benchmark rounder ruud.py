import timeit
from collections import deque, namedtuple
import rounder0
import rounder0a
import rounder5
import rounder5a

rounders=(rounder0, rounder0a, rounder5, rounder5a)
reference_rounder = rounder0a

int_ = 1
float_ = 1.6
string_ = "1.6"
list_ = [1.6, 2.4]
tuple_ = (1.6, 2.4)
dict_ = {"a": 1.6, "b": 2.4}
deque_ = deque([1.6, 2.4])

objects = {
    "int": int_,
    "float": float_,
    "string": string_,
    "list": list_,
    "tuple": tuple_,
    "dict": dict_,
    "deque": deque_,
    "list of 10 int": 10 * [int_],
    "list of 10 float": 10 * [float_],
    "list of 10 string": 10 * [string_],
    "list of 10 list": 10 * [list_],
    "list of 10 tuple": 10 * [tuple_],
    "list of 10 dict": 10 * [dict_],
    "list of 10 deque": 10 * [deque_],

    "list of 100 int": 100 * [int_],
    "list of 100 float": 100 * [float_],
    "list of 100 string": 100 * [string_],
    "list of 100 list": 100 * [list_],
    "list of 100 tuple": 100 * [tuple_],
    "list of 100 dict": 100 * [dict_],
    "list of 100 deque": 100 * [deque_],

    "list of 1000 int": 1000 * [int_],
    "list of 1000 float": 1000 * [float_],
    "list of 1000 string": 1000 * [string_],
    "list of 1000 list": 1000 * [list_],
    "list of 1000 tuple": 1000 * [tuple_],
    "list of 1000 dict": 1000 * [dict_],
    "list of 1000 deque": 1000 * [deque_],

    "list of 10000 int": 10000 * [int_],
    "list of 10000 float": 10000 * [float_],
    "list of 10000 string": 10000 * [string_],
    "list of 10000 list": 100000 * [list_],
    "list of 10000 tuple": 10000 * [tuple_],
    "list of 10000 dict": 10000 * [dict_],
    "list of 10000 deque": 10000 * [deque_],

    "list of 100000 int": 100000 * [int_],
    "list of 100000 float": 100000 * [float_],
    "list of 100000 string": 100000 * [string_],
    "list of 100000 list": 100000 * [list_],
    "list of 100000 tuple": 100000 * [tuple_],
    "list of 100000 dict": 100000 * [dict_],
    "list of 100000 deque": 100000 * [deque_],

    "deque of 100000 int": deque(100000 * [int_]),
    "deque of 100000 float": deque(100000 * [float_]),
    "deque of 100000 string": deque(100000 * [string_]),
    "deque of 100000 list": deque(100000 * [list_]),
    "deque of 100000 tuple": deque(100000 * [tuple_]),
    "deque of 100000 dict": deque(100000 * [dict_]),
    "deque of 100000 deque": deque(100000 * [deque_]),
}


if __name__ == "__main__":
    repeat = 10

    print("relative performance")
    print(f"{'object':30}",end="")
#    for rounder in rounders:
#        print(f"{rounder.__name__:>12}", end="")
#    print(end=" | ")
    for rounder in rounders:
        print(f"{rounder.__name__:>12}", end="")
    print()

    for object_type, obj in objects.items():
        if " of 10 " in object_type:
            n = 10000
        elif "of 100 " in object_type:
            n = 1000
        elif "of 1000 " in object_type:
            n = 100
        elif "of 10000 " in object_type:
            n = 10
        elif "of 100000 " in object_type:
            n = 1
        else:
            n = 100000

        res={}
        minimum={}
        for rounder in rounders:
            res[rounder] = timeit.repeat(lambda: rounder.round_object(obj), number=n, repeat=repeat)
            minimum[rounder]=min(res[rounder])


        print(f"{object_type:30}",end="")
#        for rounder in rounders:
#            print(f"{minimum[rounder]:12.2f}",end="")
#        print(end=" | ")
        for rounder in rounders:
            print(f"{minimum[rounder]/minimum[reference_rounder]:12.2f}",end="")
        print()
