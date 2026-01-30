import time
import random
import matplotlib.pyplot as plt

from bad_sorts import create_random_list, bubble_sort, insertion_sort, selection_sort

def time_sort(sort_func, L):
    A = L[:]  
    t0 = time.perf_counter()
    sort_func(A)
    t1 = time.perf_counter()
    return t1 - t0

def avg_time(sort_func, n, runs, max_value):
    total = 0.0
    for _ in range(runs):
        L = create_random_list(n, max_value)
        total += time_sort(sort_func, L)
    return total / runs

def main():
    random.seed(0)

    max_value = 100000
    lengths = [100, 200, 400, 800, 1200, 1600, 2000, 2500, 3000]

    bubble_times = []
    insertion_times = []
    selection_times = []

    for n in lengths:
        runs = 20 if n <= 800 else 8
        bubble_times.append(avg_time(bubble_sort, n, runs, max_value))
        insertion_times.append(avg_time(insertion_sort, n, runs, max_value))
        selection_times.append(avg_time(selection_sort, n, runs, max_value))
        print(f"done n={n} (runs={runs})")

    plt.figure()
    plt.plot(lengths, bubble_times, label="Bubble")
    plt.plot(lengths, insertion_times, label="Insertion")
    plt.plot(lengths, selection_times, label="Selection")
    plt.xlabel("List length (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Experiment 1: Bad Sorts Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("exp1_bad_sorts.png", dpi=200)
    plt.show()

if __name__ == "__main__":
    main()
