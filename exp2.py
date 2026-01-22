# exp2.py
import time
import statistics
import matplotlib.pyplot as plt
from bad_sorts import create_random_list, bubble_sort, selection_sort, bubblesort2, selection_sort2

def time_one(sort_fn, L):
    A = L.copy()
    t0 = time.perf_counter()
    sort_fn(A)
    t1 = time.perf_counter()
    return t1 - t0

def avg_time(sort_fn, length, max_value, runs):
    times = []
    for _ in range(runs):
        L = create_random_list(length, max_value)
        times.append(time_one(sort_fn, L))
    return statistics.mean(times)

def run_curve(sort_fn, lengths, max_value, runs):
    return [avg_time(sort_fn, n, max_value, runs) for n in lengths]

def plot_two_curves(lengths, t_a, label_a, t_b, label_b, title, out_png):
    plt.figure()
    plt.plot(lengths, t_a, marker="o", label=label_a)
    plt.plot(lengths, t_b, marker="o", label=label_b)
    plt.xlabel("List length (n)")
    plt.ylabel("Time (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

if __name__ == "__main__":
    lengths = [200, 400, 600, 800, 1000, 1200, 1400, 1600] 
    runs = 5                               
    max_value = 10_000                       

    
    t_bubble = run_curve(bubble_sort, lengths, max_value, runs)
    t_bubble2 = run_curve(bubblesort2, lengths, max_value, runs)

    plot_two_curves(
        lengths, t_bubble, "bubble_sort", t_bubble2, "bubblesort2",
        "Experiment 2: Bubble Sort vs bubblesort2", "exp2_bubble.png"
    )

    
    t_sel = run_curve(selection_sort, lengths, max_value, runs)
    t_sel2 = run_curve(selection_sort2, lengths, max_value, runs)

    plot_two_curves(
        lengths, t_sel, "selection_sort", t_sel2, "selection_sort2",
        "Experiment 2: Selection Sort vs selection_sort2", "exp2_selection.png"
    )

    print("Done. Saved: exp2_bubble.png, exp2_selection.png")
