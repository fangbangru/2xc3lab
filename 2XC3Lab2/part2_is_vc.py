import random
import matplotlib.pyplot as plt

from graph import create_random_graph, MVC, MIS

def experiment_mis_vc_relation(n=10, runs=300, seed=0):
    random.seed(seed)
    max_m = n * (n - 1) // 2

    m_values = list(range(0, max_m + 1, 2))
    avg_sum = []
    avg_mvc = []
    avg_mis = []

    for m in m_values:
        s_sum = 0
        s_mvc = 0
        s_mis = 0

        for _ in range(runs):
            G = create_random_graph(n, m)
            mvc = len(MVC(G))
            mis = len(MIS(G))
            s_sum += (mvc + mis)
            s_mvc += mvc
            s_mis += mis

        avg_sum.append(s_sum / runs)
        avg_mvc.append(s_mvc / runs)
        avg_mis.append(s_mis / runs)

    # Plot 1
    plt.figure()
    plt.plot(m_values, avg_sum, marker="o")
    plt.axhline(y=n, linestyle="--")
    plt.xlabel("Number of edges (m)")
    plt.ylabel("Average |MVC| + |MIS|")
    plt.title(f"MIS & MVC relationship: average(|MVC|+|MIS|) (n={n}, runs={runs})")
    plt.grid(True)
    plt.show()

    # Plot 2
    plt.figure()
    plt.plot(m_values, avg_mvc, marker="o", label="Average |MVC|")
    plt.plot(m_values, avg_mis, marker="o", label="Average |MIS|")
    plt.xlabel("Number of edges (m)")
    plt.ylabel("Average size")
    plt.title(f"Average |MVC| and |MIS| vs m (n={n}, runs={runs})")
    plt.grid(True)
    plt.legend()
    plt.show()

    deviations = [abs(x - n) for x in avg_sum]
    print("Max deviation of avg(|MVC|+|MIS|) from n:", max(deviations))

if __name__ == "__main__":
    experiment_mis_vc_relation(n=10, runs=300, seed=0)