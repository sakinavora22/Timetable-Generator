# utility helper functions
# provides timing measurement and algorithm complexity lookup

import time


def measure_time(func, *args):
    # runs a function and measures how long it takes in milliseconds
    # returns a tuple: (result_of_function, elapsed_time_in_ms)
    # uses perf_counter for high precision timing
    start = time.perf_counter()
    result = func(*args)
    elapsed = (time.perf_counter() - start) * 1000
    return result, round(elapsed, 4)


def get_complexity(algorithm):
    # returns the time complexity string for a given algorithm name
    # used to include complexity info in the api response
    complexities = {
        "greedy": "O(n log n)",
        "backtracking": "O(S^n)",
        "dp": "O(n * W)",
        "graph_coloring": "O(V + E)",
        "priority_queue": "O(n log n)",
        "sorting": "O(n log n)",
        "sjf": "O(n log n)"
    }
    return complexities.get(algorithm, "Unknown")
