import timeit
from collections import deque, namedtuple
from rounder import rounder, rounder2, rounder3, rounder4, rounder5
from random import uniform
import array
from pprint import pprint

objects = {
    "int": 1234567890,
    "float": 1234567890.54323445645234346,
    "string": "This is a perfect string for benchmarking, yay!",
    "float list short": [
        1.123,
        5.55345346,
        -0.234523423,
        123123123.123123123,
        50505050505.505050505999,
    ],
    "float list long": [uniform(-1000, 1000) for _ in range(1_000_000)],
    "float tuple short": (
        1.123,
        5.55345346,
        -0.234523423,
        123123123.123123123,
        50505050505.505050505999,
    ),
    "float tuple long": tuple(uniform(-1000, 1000) for _ in range(1_000_000)),
    "float set short": {
        1.123,
        5.55345346,
        -0.234523423,
        123123123.123123123,
        50505050505.505050505999,
    },
    "float tuple long": set(uniform(-1000, 1000) for _ in range(1_000_000)),
    "float dict short": {
        "1": 1.123,
        "2": 5.55345346,
        "3": -0.234523423,
        "4": 123123123.123123123,
        "5": 50505050505.505050505999,
    },
    "mixed list short": [
        1.123,
        "a",
        -0.234523423,
        "Shout Bamalama",
        123123123.123123123,
        "zing",
        50505050505.505050505999,
    ],
    "mixed list long": [
        str(v) if i % 5 == 0 else str(v)
        for i, v
        in enumerate([uniform(-1000, 1000) for _ in range(1_000_000)])
    ],
    "mixed tuple short": (
        1.123,
        "a",
        -0.234523423,
        "Shout Bamalama",
        123123123.123123123,
        "zing",
        50505050505.505050505999,
    ),
    "mixed set short": {
        1.123,
        "a",
        -0.234523423,
        "Shout Bamalama",
        123123123.123123123,
        "zing",
        50505050505.505050505999,
    },
    "mixed dict short": {
        "1": 1.123,
        "2": "a",
        "3": -0.234523423,
        "4": "Shout Bamalama",
        "5": 123123123.123123123,
        "6": "zing",
        "7": 50505050505.505050505999,
    },
    "complex object long": {
        "a": 12.22221111,
        "string": "something nice, ha?",
        "callable": lambda x: x ** 2,
        "float list long": [uniform(-1000, 1000) for _ in range(100_000)],
        "float list of deque": [
            deque(uniform(-1000, 1000) for _ in range(100))
            for _ in range(100_000)
        ],
        "mixed list long": [
            str(v) if i % 5 == 0 else str(v)
            for i, v
            in enumerate([uniform(-1000, 1000) for _ in range(200_000)])
        ],
        "b": 2,
        "c": 1.222,
        "d": [1.12343, 0.023492],
        "e": {
            "ea": 1 / 44,
            "eb": {1.333, 2.999},
            "ec": dict(eca=1.565656, ecb=1.765765765),
        },
    },
}

objects["float deque short"] = deque(objects["float list short"])
objects["float deque long"] = deque(objects["float list long"])
objects["mixed deque short"] = deque(objects["mixed list short"])
objects["mixed deque long"] = deque(objects["mixed list long"])

objects["double array short"] = array.array(
    "d", objects["float list short"]
)
objects["double array long"] = array.array(
    "d", objects["float list long"]
)

results = {}


Results = namedtuple("Results", "v1 v4 v5")


if __name__ == "__main__":
    repeat = 10

    for object_type, obj in objects.items():
        n = 100 if "long" in object_type else 1_000_000
        print(f"\nBenchmarking {object_type}...:")
        res_original = timeit.repeat(
            lambda: rounder.round_object(obj),
            number=n,
            repeat=repeat,
        )
        print(f"v1 done...")
        #res_v2 = timeit.repeat(
        #    lambda: rounder2.round_object(obj),
        #    number=n,
        #    repeat=repeat,
        #)
        #print(f"v2 done...")
        #res_v3 = timeit.repeat(
        #    lambda: rounder3.round_object(obj),
        #    number=n,
        #    repeat=repeat,
        #)
        #print(f"v3 done...")
        res_v4 = timeit.repeat(
            lambda: rounder4.round_object(obj),
            number=n,
            repeat=repeat,
        )
        res_v5 = timeit.repeat(
            lambda: rounder5.round_object(obj),
            number=n,
            repeat=repeat,
        )
        results[object_type] = {}
        results[object_type]["raw results"] = Results(
            res_original, res_v4, res_v5
        )
        results[object_type]["min"] = Results(
            min(res_original), min(res_v4),  min(res_v5)
        )
        results[object_type]["relative to v1"] = Results(
            1,
            min(res_original) / min(res_v4),
            min(res_original) / min(res_v5)
        )
        print(
            f"Done:\n"
            f"{rounder4.signif_object(results[object_type]['relative to v1'], 3)}"
            )

    with open("benchmarks.txt", "w") as f:
        pprint(rounder.signif_object(results, 3), stream=f)
    with open("benchmarks_relative.txt", "w") as f:
        pprint(
            rounder.signif_object(
                {_type: _res["relative to v1"] for _type, _res in results.items()},
                3),
            stream=f
        )
    
    
