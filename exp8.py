import importlib.util, random, time, statistics
import matplotlib.pyplot as plt


good_path = "good_sorts.py"
bad_path  = "bad_sorts.py"

spec = importlib.util.spec_from_file_location("good_sorts", good_path)
good = importlib.util.module_from_spec(spec); spec.loader.exec_module(good)

spec2 = importlib.util.spec_from_file_location("bad_sorts", bad_path)
bad = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(bad)

def time_one(algo, arr):
    L = arr[:]  # copy
    start = time.perf_counter_ns()
    algo(L)
    end = time.perf_counter_ns()
    return (end - start) / 1e6  # ms

def run_experiment(n_values, runs=200, max_value=10000, seed=0):
    random.seed(seed)
    t_ins, t_mer, t_qui = [], [], []
    for n in n_values:
        ins_runs, mer_runs, qui_runs = [], [], []
        for _ in range(runs):
            arr = [random.randint(0, max_value) for _ in range(n)]
            ins_runs.append(time_one(bad.insertion_sort2, arr))
            mer_runs.append(time_one(good.mergesort, arr))
            qui_runs.append(time_one(good.quicksort, arr))
        t_ins.append(statistics.median(ins_runs))
        t_mer.append(statistics.median(mer_runs))
        t_qui.append(statistics.median(qui_runs))
    return t_ins, t_mer, t_qui

n_values = list(range(5, 151, 5))
runs = 200

t_ins, t_mer, t_qui = run_experiment(n_values, runs=runs)

crossover_n = None
for i, n in enumerate(n_values):
    if t_ins[i] > min(t_mer[i], t_qui[i]):
        crossover_n = n
        break
print("Crossover n ≈", crossover_n)

plt.figure()
plt.plot(n_values, t_ins, label="Insertion sort (median)")
plt.plot(n_values, t_mer, label="Merge sort (median)")
plt.plot(n_values, t_qui, label="Quick sort (median)")
plt.xlabel("List length (n)")
plt.ylabel("Median time (ms)")
plt.title(f"Experiment 8: Insertion vs Merge vs Quick (random lists, {runs} runs)")
plt.legend()
plt.grid(True)
plt.show()
