import matplotlib.pyplot as plt
from graph import create_random_graph, is_connected

def run_exp2(i=100, m=200, j_values=None, out_png="exp2_connected_probability.png"):
    if j_values is None:
        j_values = (
            list(range(0, 101, 10)) +
            list(range(110, 401, 20)) +
            list(range(420, 801, 40))
        )
        j_values = sorted(set(j_values))

    probs = []
    for j in j_values:
        connected_count = 0
        for _ in range(m):
            G = create_random_graph(i, j)
            if is_connected(G):
                connected_count += 1
        prob = connected_count / m
        probs.append(prob)
        print(f"j={j:3d}, connected_prob={prob:.3f}")

    # Plot
    plt.figure()
    plt.plot(j_values, probs, marker="o")
    plt.xlabel("Number of edges (j)")
    plt.ylabel("Probability of being connected")
    plt.title(f"Experiment 2: Connected probability (i={i}, m={m})")
    plt.grid(True)
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    print(f"\nSaved figure to: {out_png}")

    return j_values, probs

if __name__ == "__main__":
    run_exp2()