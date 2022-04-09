import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import random


def q(m, n, spike):
    return 1 / (1 + (abs(m - 50)) ** spike + (abs(n - 50)) ** spike)


def f(m, n):
    return m + n


def propose_advanced(curr, step_size):
    m = curr[0]
    n = curr[1]

    # Generate candidate neighbours based on the step size
    candidates = []
    for i in range(-step_size, step_size + 1):
        for j in range(-step_size, step_size + 1):
            candidates.append(((m + i) % 100, (n + j) % 100))

    return random.choice(candidates)


def accept_reject(curr, proposed, spike):
    proposed_q = q(proposed[0], proposed[1], spike)
    curr_q = q(curr[0], curr[1], spike)

    if proposed_q >= curr_q:
        return proposed

    if random.random() <= proposed_q / curr_q:
        return proposed

    return curr


def compute_average(p):
    f_sum = 0
    for state in p:
        f_sum += f(state[0], state[1])
    return f_sum / len(p)


def plot_3d_histogram(points, title):
    m = np.array([i[0] for i in points])
    n = np.array([i[1] for i in points])
    hist, medges, nedges = np.histogram2d(
        m, n, bins=(100, 100), range=[[0, 99], [0, 99]]
    )
    mpos, npos = np.meshgrid(medges[:-1] + medges[1:], nedges[:-1] + nedges[1:])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    mpos = mpos.flatten() / 2.0
    npos = npos.flatten() / 2.0
    zpos = np.zeros_like(mpos)

    dm = medges[1] - medges[0]
    dn = nedges[1] - nedges[0]
    dz = hist.flatten()

    cmap = cm.get_cmap("jet")
    max_height = np.max(dz)
    min_height = np.min(dz)
    rgba = [cmap((k - min_height) / max_height) for k in dz]

    ax.bar3d(mpos, npos, zpos, dm, dn, dz, color=rgba, zsort="average")
    plt.title(title)
    plt.xlabel("m")
    plt.ylabel("n")
    plt.show()


def plot_expected_histogram(spike, N):
    normalization = 0
    for i in range(100):
        for j in range(100):
            normalization += q(i, j, spike)

    points = []
    for i in range(100):
        for j in range(100):
            points.append((i, j))

    p = []
    for point in points:
        mult = int(q(point[0], point[1], spike) / normalization * N)
        p += [point] * mult
    plot_3d_histogram(p, f"Expected Histogram with N = {N} and Spikiness = {spike}")


def single_experiment():
    spike = float(input("Enter spikiness value: "))
    N = int(input("Enter number of iterations: "))
    step_size = int(input("Enter the step size for the proposal process: "))

    # Initialization
    p = [(random.randint(0, 99), random.randint(0, 99))]

    for iteration in range(N):
        p.append(accept_reject(p[-1], propose_advanced(p[-1], step_size), spike))

    print("Computed mean = " + str(compute_average(p)))
    plot_3d_histogram(
        p,
        f"Histogram for Simple Proposal Process with N = {N} and Spikiness = {spike}",
    )
    plot_expected_histogram(spike, N)


def plot_convergence(step_size):
    for plot_id, step in enumerate(step_size):
        points = step_size[step]
        averages = [
            compute_average(points[0:r_bound]) for r_bound in range(1, len(points) + 1)
        ]
        iters = list(range(1, len(points) + 1))

        plt.subplot(len(step_size), 1, plot_id + 1)
        plt.plot(iters, averages)
        plt.title(f"Step Size = {step}", fontsize=12)
        plt.ylim(0, 200)
    plt.suptitle("Convergence of Expected Value at Various Step Sizes", fontsize=16)
    plt.show()


def step_size_experiment():
    spike = float(input("Enter spikiness value: "))
    N = int(input("Enter number of iterations: "))
    step_size = dict.fromkeys(list(range(1, 20, 4)))

    for step in step_size:
        print(f"Processing step size of {step}")

        p = [(random.randint(0, 99), random.randint(0, 99))]

        for iteration in range(N):
            p.append(accept_reject(p[-1], propose_advanced(p[-1], step), spike))

        step_size[step] = p

        print(f"Computed mean for step_size = {step} is: " + str(compute_average(p)))

    plot_convergence(step_size)


def main():
    step_size_experiment()


if __name__ == "__main__":
    main()
