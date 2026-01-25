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


if __name__ == "__main__":
    import os
    import csv
    import random
    import statistics
    import sys
    from time import perf_counter

    import matplotlib.pyplot as plt

    import bad_sorts
    # NOTE: we're inside good_sorts.py, so quicksort/mergesort/heapsort are available.

    # -------- Explicit outline (matches lab requirement) --------
    OUT_DIR = "out"
    MAX_VALUE = 10**6

    # List length MUST be constant for Experiment 5
    EXP5_N = 5000

    # Swaps values tested
    EXP5_SWAPS = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]

    # Number of runs per swaps value
    EXP5_RUNS = 3

    # Seed for reproducibility (optional)
    EXP5_SEED = 54321

    # Quicksort pivot is first element; near-sorted can cause deep recursion
    sys.setrecursionlimit(200000)
    # ----------------------------------------------------------

    def ensure_out_dir():
        os.makedirs(OUT_DIR, exist_ok=True)

    def time_one(sort_fn, base_list):
        """Time sort_fn on a COPY of base_list (fair comparison)."""
        L = list(base_list)
        t0 = perf_counter()
        sort_fn(L)
        t1 = perf_counter()
        return t1 - t0

    def write_csv(path, header, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    def summarize(rows):
        """
        rows: list of dicts with keys: swaps, algorithm, time_s
        returns: list of dicts: swaps, algorithm, mean_time_s, stdev_time_s, count
        """
        buckets = {}
        for r in rows:
            key = (r["swaps"], r["algorithm"])
            buckets.setdefault(key, []).append(r["time_s"])

        out = []
        for (swaps, alg), times in sorted(buckets.items(), key=lambda x: x[0]):
            mean = statistics.mean(times)
            stdev = statistics.pstdev(times) if len(times) > 1 else 0.0
            out.append({
                "swaps": swaps,
                "algorithm": alg,
                "mean_time_s": mean,
                "stdev_time_s": stdev,
                "count": len(times),
            })
        return out

    # ---- Run Experiment 5 ----
    ensure_out_dir()
    random.seed(EXP5_SEED)

    algorithms = [
        ("quicksort", quicksort),
        ("mergesort", mergesort),
        ("heapsort", heapsort),
    ]

    raw = []
    print("=== Experiment 5: near-sorted lists (fixed n), varying swaps ===")
    print(f"  n fixed at {EXP5_N}")
    for swaps in EXP5_SWAPS:
        for run in range(1, EXP5_RUNS + 1):
            base = bad_sorts.create_near_sorted_list(EXP5_N, MAX_VALUE, swaps)

            # Fairness: time each algorithm on SAME base list (copy inside time_one)
            for alg_name, alg_fn in algorithms:
                dt = time_one(alg_fn, base)
                raw.append({
                    "swaps": swaps,
                    "run": run,
                    "algorithm": alg_name,
                    "time_s": dt,
                })
        print(f"  finished swaps={swaps}")

    # Save raw CSV
    raw_path = os.path.join(OUT_DIR, "exp5_raw.csv")
    write_csv(
        raw_path,
        ["swaps", "run", "algorithm", "time_s"],
        [[r["swaps"], r["run"], r["algorithm"], r["time_s"]] for r in raw]
    )

    # Save summary CSV
    summ = summarize(raw)
    summ_path = os.path.join(OUT_DIR, "exp5_summary.csv")
    write_csv(
        summ_path,
        ["swaps", "algorithm", "mean_time_s", "stdev_time_s", "count"],
        [[s["swaps"], s["algorithm"], s["mean_time_s"], s["stdev_time_s"], s["count"]] for s in summ]
    )

    # Plot: swaps vs mean runtime (3 curves), n constant
    plt.figure()
    for alg_name, _ in algorithms:
        xs = EXP5_SWAPS
        ys = []
        for s in xs:
            entry = next(row for row in summ if row["swaps"] == s and row["algorithm"] == alg_name)
            ys.append(entry["mean_time_s"])
        plt.plot(xs, ys, marker="o", label=alg_name)

    plt.xlabel("Number of random swaps")
    plt.ylabel("Mean runtime (seconds)")
    plt.title(f"Experiment 5: Good sorts runtime vs swaps (near-sorted lists, n={EXP5_N})")
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(OUT_DIR, "exp5_good_sorts_swaps_vs_time.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()

    print("\n[Experiment 5 DONE]")
    print(f"  Plot:   {plot_path}")
    print(f"  Raw:    {raw_path}")
    print(f"  Summary:{summ_path}")
