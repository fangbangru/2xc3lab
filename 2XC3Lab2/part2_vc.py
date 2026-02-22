import random
import matplotlib.pyplot as plt

from graph import create_random_graph, MVC, approx1, approx2, approx3


def mean_ratios_for_m(n, m, runs):
    """
    Returns (mean_r1, mean_r2, mean_r3) for fixed n,m over 'runs' random graphs.
    Where rk = |approxk(G)| / |MVC(G)|.
    """
    s1 = s2 = s3 = 0.0

    for _ in range(runs):
        G = create_random_graph(n, m)
        opt = len(MVC(G))

        # if no edges, opt=0; define ratio as 1.0 (all methods "perfect")
        if opt == 0:
            r1 = r2 = r3 = 1.0
        else:
            r1 = len(approx1(G)) / opt
            r2 = len(approx2(G)) / opt
            r3 = len(approx3(G)) / opt

        s1 += r1
        s2 += r2
        s3 += r3

    return s1 / runs, s2 / runs, s3 / runs


def worst_ratio_approx1_for_m(n, m, runs):
    """Empirical worst-case max(|approx1|/|MVC|) among 'runs' random graphs."""
    worst = 1.0
    for _ in range(runs):
        G = create_random_graph(n, m)
        opt = len(MVC(G))
        ratio = 1.0 if opt == 0 else (len(approx1(G)) / opt)
        if ratio > worst:
            worst = ratio
    return worst


def plot_mean_curves(n, runs, step, seed, title_suffix=""):
    random.seed(seed)
    max_m = n * (n - 1) // 2
    m_values = list(range(0, max_m + 1, step))

    r1s, r2s, r3s = [], [], []
    for m in m_values:
        r1, r2, r3 = mean_ratios_for_m(n, m, runs)
        r1s.append(r1)
        r2s.append(r2)
        r3s.append(r3)

    plt.figure()
    plt.plot(m_values, r1s, marker="o", label="approx1 (max degree)")
    plt.plot(m_values, r2s, marker="o", label="approx2 (random vertex)")
    plt.plot(m_values, r3s, marker="o", label="approx3 (random edge)")
    plt.xlabel("Number of edges (m)")
    plt.ylabel("E[ |approx| / |MVC| ]")
    plt.title(f"VC Approximation Quality (n={n}, runs={runs}){title_suffix}")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_worstcase_curve(n, runs, step, seed):
    random.seed(seed)
    max_m = n * (n - 1) // 2
    m_values = list(range(0, max_m + 1, step))

    worsts = []
    for m in m_values:
        worsts.append(worst_ratio_approx1_for_m(n, m, runs))

    plt.figure()
    plt.plot(m_values, worsts, marker="o")
    plt.xlabel("Number of edges (m)")
    plt.ylabel("max over samples of |approx1| / |MVC|")
    plt.title(f"Approx1 Empirical Worst-case (n={n}, runs={runs})")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Keep n small: MVC is exponential
    seed = 0

    # FIG 1
    plot_mean_curves(n=8, runs=300, step=2, seed=seed)

    # FIG 2
    plot_mean_curves(n=10, runs=200, step=3, seed=seed, title_suffix=" (different n)")

    # FIG 3
    plot_worstcase_curve(n=8, runs=400, step=2, seed=seed)