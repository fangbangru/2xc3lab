# exp6.py
import time
import statistics
import matplotlib.pyplot as plt
from bad_sorts import create_random_list
from good_sorts import quicksort, dual_quicksort

def time_one(sort_fn, L):
    A = L.copy()
    t0 = time.perf_counter()
    sort_fn(A)
    t1 = time.perf_counter()
    return t1 - t0

def avg_time(sort_fn, n, max_value, runs):
    times = []
    for _ in range(runs):
        L = create_random_list(n, max_value)
        times.append(time_one(sort_fn, L))
    return statistics.mean(times)

def run_curve(sort_fn, lengths, max_value, runs):
    return [avg_time(sort_fn, n, max_value, runs) for n in lengths]

if __name__ == "__main__":
    # ====== 这些要写进报告（explicit outline） ======
    lengths = [1000, 2000, 4000, 8000, 12000, 16000]
    runs = 10
    max_value = 100000

    t_qs = run_curve(quicksort, lengths, max_value, runs)
    t_dqs = run_curve(dual_quicksort, lengths, max_value, runs)

    plt.figure()
    plt.plot(lengths, t_qs, marker="o", label="quicksort (single pivot)")
    plt.plot(lengths, t_dqs, marker="o", label="dual_quicksort (two pivots)")
    plt.xlabel("List length (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Experiment 6: Single-pivot vs Dual-pivot Quick Sort")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("exp6_quicksort.png", dpi=200)
    plt.close()

    print("Done. Saved: exp6_quicksort.png")
