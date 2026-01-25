"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.

In contains traditional implementations for:
1) Quick sort
2) Merge sort
3) Heap sort

Author: Vincent Maccio
"""

# ************ Quick Sort ************
def quicksort(L):
    copy = quicksort_copy(L)
    for i in range(len(L)):
        L[i] = copy[i]


def quicksort_copy(L):
    if len(L) < 2:
        return L
    pivot = L[0]
    left, right = [], []
    for num in L[1:]:
        if num < pivot:
            left.append(num)
        else:
            right.append(num)
    return quicksort_copy(left) + [pivot] + quicksort_copy(right)

# *************************************


# ************ Merge Sort *************

def mergesort(L):
    if len(L) <= 1:
        return
    mid = len(L) // 2
    left, right = L[:mid], L[mid:]

    mergesort(left)
    mergesort(right)
    temp = merge(left, right)

    for i in range(len(temp)):
        L[i] = temp[i]


def merge(left, right):
    L = []
    i = j = 0

    while i < len(left) or j < len(right):
        if i >= len(left):
            L.append(right[j])
            j += 1
        elif j >= len(right):
            L.append(left[i])
            i += 1
        else:
            if left[i] <= right[j]:
                L.append(left[i])
                i += 1
            else:
                L.append(right[j])
                j += 1
    return L

# *************************************

# ************* Heap Sort *************

def heapsort(L):
    heap = Heap(L)
    for _ in range(len(L)):
        heap.extract_max()

class Heap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i)

    def heapify(self, i):
        largest_known = i
        if self.left(i) < self.length and self.data[self.left(i)] > self.data[i]:
            largest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)] > self.data[largest_known]:
            largest_known = self.right(i)
        if largest_known != i:
            self.data[i], self.data[largest_known] = self.data[largest_known], self.data[i]
            self.heapify(largest_known)

    def insert(self, value):
        if len(self.data) == self.length:
            self.data.append(value)
        else:
            self.data[self.length] = value
        self.length += 1
        self.bubble_up(self.length - 1)

    def insert_values(self, L):
        for num in L:
            self.insert(num)

    def bubble_up(self, i):
        while i > 0 and self.data[i] > self.data[self.parent(i)]:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            i = self.parent(i)

    def extract_max(self):
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]
        max_value = self.data[self.length - 1]
        self.length -= 1
        self.heapify(0)
        return max_value

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s

# *************************************
    
# =========================
# EXPERIMENT 5 RUNNER CODE
"""
exp5.py — Experiment 5 runner for 2XC3 Lab 1 (Good sorts)

Requirement match:
- Explicit outline: constant list length, swaps values, runs, etc.
- Graph: swaps vs time with 3 curves (quicksort/mergesort/heapsort), list length constant
- Brief discussion: written in report (this script outputs the data + plot)

Put this file in the SAME folder as:
  - good_sorts.py
  - bad_sorts.py
Run:
  python exp5.py
"""

import os
import sys
import csv
import random
import statistics
from time import perf_counter

# --- Import your course files ---
import good_sorts
import bad_sorts

# ------------------ EXPLICIT OUTLINE (EDIT IF YOU WANT) ------------------
MAX_VALUE = 10**6

# Experiment 5 requires constant list length
N = 5000

# swaps values (how "non-sorted" the list is)
SWAPS_VALUES = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

# runs per swaps value
RUNS = 3

# fixed seed (optional, for reproducibility)
SEED = 54321

# quicksort pivot is first element; near-sorted can cause deep recursion
sys.setrecursionlimit(200000)

ALGORITHMS = [
    ("quicksort", good_sorts.quicksort),
    ("mergesort", good_sorts.mergesort),
    ("heapsort",  good_sorts.heapsort),
]
# ------------------------------------------------------------------------


def script_dir() -> str:
    """Directory of this script, so outputs always go to the right place."""
    return os.path.dirname(os.path.abspath(__file__))


def ensure_out_dir() -> str:
    out = os.path.join(script_dir(), "out")
    os.makedirs(out, exist_ok=True)
    return out


def time_one(sort_fn, base_list) -> float:
    """Time sorting on a COPY of the same base list (fairness)."""
    L = list(base_list)
    t0 = perf_counter()
    sort_fn(L)
    return perf_counter() - t0


def sanity_check():
    """Quick correctness check before doing long timing."""
    base = bad_sorts.create_random_list(50, 1000)
    expected = sorted(base)
    for name, fn in ALGORITHMS:
        test = base.copy()
        fn(test)
        if test != expected:
            raise AssertionError(f"[Sanity check FAILED] {name} did not sort correctly.")
    print("[Sanity check PASSED] all algorithms sort correctly.\n")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def summarize_raw(raw_rows):
    """
    raw_rows: list of tuples (swaps, run, algorithm, time_s)
    returns: list of tuples (swaps, algorithm, mean_time_s, stdev_time_s, count)
    """
    bucket = {}
    for swaps, run, alg, t in raw_rows:
        bucket.setdefault((swaps, alg), []).append(t)

    summary = []
    for (swaps, alg), ts in sorted(bucket.items(), key=lambda x: x[0]):
        mean = statistics.mean(ts)
        stdev = statistics.pstdev(ts) if len(ts) > 1 else 0.0
        summary.append((swaps, alg, mean, stdev, len(ts)))
    return summary


def make_plot(summary_rows, out_path):
    """
    summary_rows: list of tuples (swaps, algorithm, mean_time_s, stdev_time_s, count)
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("ERROR: matplotlib not installed. Run: python -m pip install matplotlib")
        return

    # Prepare series for each algorithm
    x = SWAPS_VALUES
    alg_to_y = {name: [] for name, _ in ALGORITHMS}

    # Turn summary into a dict for fast lookup
    lookup = {(swaps, alg): mean for swaps, alg, mean, stdev, cnt in summary_rows}

    for alg_name, _ in ALGORITHMS:
        for s in x:
            alg_to_y[alg_name].append(lookup[(s, alg_name)])

    plt.figure()
    for alg_name, y in alg_to_y.items():
        plt.plot(x, y, marker="o", label=alg_name)

    plt.xlabel("Number of random swaps")
    plt.ylabel("Mean runtime (seconds)")
    plt.title(f"Experiment 5: swaps vs time (near-sorted lists, n={N})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main():
    out_dir = ensure_out_dir()
    random.seed(SEED)

    sanity_check()

    print("=== Experiment 5: near-sorted lists, fixed length, varying swaps ===")
    print(f"n = {N} (constant)")
    print(f"swaps values = {SWAPS_VALUES}")
    print(f"runs per swaps = {RUNS}\n")

    raw = []
    for swaps in SWAPS_VALUES:
        for run in range(1, RUNS + 1):
            base = bad_sorts.create_near_sorted_list(N, MAX_VALUE, swaps)

            # Fairness: same base list -> each alg sorts a copy
            for alg_name, alg_fn in ALGORITHMS:
                dt = time_one(alg_fn, base)
                raw.append((swaps, run, alg_name, dt))

        print(f"  finished swaps={swaps}")

    raw_csv = os.path.join(out_dir, "exp5_raw.csv")
    write_csv(raw_csv, ["swaps", "run", "algorithm", "time_s"], raw)

    summary = summarize_raw(raw)
    summary_csv = os.path.join(out_dir, "exp5_summary.csv")
    write_csv(summary_csv, ["swaps", "algorithm", "mean_time_s", "stdev_time_s", "count"], summary)

    plot_path = os.path.join(out_dir, "exp5_good_sorts_swaps_vs_time.png")
    make_plot(summary, plot_path)

    print("\n[Experiment 5 DONE]")
    print("Plot:   ", plot_path)
    print("Raw:    ", raw_csv)
    print("Summary:", summary_csv)


if __name__ == "__main__":
    main()
