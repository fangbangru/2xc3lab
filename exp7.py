# exp7.py
import time
import statistics
import matplotlib.pyplot as plt

from bad_sorts import create_random_list
from good_sorts import mergesort, bottom_up_mergesort

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
    # ====== 写进报告的实验参数（explicit outline） ======
    lengths = [1000, 2000, 4000, 8000, 12000, 16000]
    runs = 10
    max_value = 100000

    t_rec = run_curve(mergesort, lengths, max_value, runs)
    t_bu = run_curve(bottom_up_mergesort, lengths, max_value, runs)

    plt.figure()
    plt.plot(lengths, t_rec, marker="o", label="mergesort (recursive)")
    plt.plot(lengths, t_bu, marker="o", label="bottom_up_mergesort (iterative)")
    plt.xlabel("List length (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Experiment 7: Recursive vs Bottom-up Merge Sort")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("exp7_mergesort.png", dpi=200)
    plt.close()

    print("Done. Saved: exp7_mergesort.png")
