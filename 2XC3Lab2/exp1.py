import matplotlib.pyplot as plt
from graph import create_random_graph, has_cycle

def run_exp1(i=100, m=200, j_values=None, out_png="exp1_cycle_probability.png"):
    if j_values is None:
        j_values = list(range(0, 201, 10))  # 0,10,...,200

    probs = []
    for j in j_values:
        cycle_count = 0
        for _ in range(m):
            G = create_random_graph(i, j)
            if has_cycle(G):
                cycle_count += 1
        prob = cycle_count / m
        probs.append(prob)
        print(f"j={j:3d}, cycle_prob={prob:.3f}")

    plt.figure()
    plt.plot(j_values, probs, marker="o")
    plt.xlabel("Number of edges (j)")
    plt.ylabel("Probability of having a cycle")
    plt.title(f"Experiment 1: Cycle probability (i={i}, m={m})")
    plt.grid(True)
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    print(f"\nSaved figure to: {out_png}")

    return j_values, probs

if __name__ == "__main__":
    run_exp1()