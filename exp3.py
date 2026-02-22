# exp3.py
import time
import statistics
import matplotlib.pyplot as plt

from bad_sorts import (
    create_near_sorted_list,
    insertion_sort2,
    bubblesort2,
    selection_sort2,
)

def time_one(sort_fn, L):
    A = L.copy()
    t0 = time.perf_counter()
    sort_fn(A)
    t1 = time.perf_counter()
    return t1 - t0

def avg_time_for_swaps(sort_fn, length, max_value, swaps, runs):
    times = []
    for _ in range(runs):
        L = create_near_sorted_list(length, max_value, swaps)
        times.append(time_one(sort_fn, L))
    return statistics.mean(times)

def run_curve(sort_fn, swaps_list, length, max_value, runs):
    return [avg_time_for_swaps(sort_fn, length, max_value, s, runs) for s in swaps_list]

if __name__ == "__main__":
    
    length = 5000
    max_value = 10_000
    runs = 3
    swaps_list = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

    
    t_insert2 = run_curve(insertion_sort2, swaps_list, length, max_value, runs)
    t_bubble2 = run_curve(bubblesort2, swaps_list, length, max_value, runs)
    t_select2 = run_curve(selection_sort2, swaps_list, length, max_value, runs)

    
    plt.figure()
    plt.plot(swaps_list, t_insert2, marker="o", label="insertion_sort2")
    plt.plot(swaps_list, t_bubble2, marker="o", label="bubblesort2")
    plt.plot(swaps_list, t_select2, marker="o", label="selection_sort2")
    plt.xlabel("Number of random swaps")
    plt.ylabel("Time (seconds)")
    plt.title("Experiment 3: Runtime vs swaps (near-sorted lists)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("exp3_swaps.png", dpi=200)
    plt.close()

    print("Done. Saved: exp3_swaps.png")

