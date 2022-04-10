import random


def q(m, n, spike):
    return 1 / (1 + (abs(m - 50)) ** spike + (abs(n - 50)) ** spike)


def simulate(spike, N):
    normalization = 0
    for i in range(100):
        for j in range(100):
            normalization += q(i, j, spike)

    time_avg = 0
    for k in range(N):
        m = random.randint(0, 99)
        n = random.randint(0, 99)
        time_avg = (k * time_avg + 10000 * (m + n) * q(m, n, spike) / normalization) / (
            k + 1
        )

    return time_avg


def automated_experiment():
    combinations = [
        (0.2, 10000),
        (2, 10000),
        (11, 10000),
        (0.2, 50000),
        (2, 50000),
        (11, 50000),
        (0.2, 100000),
        (2, 100000),
        (11, 100000),
    ]

    for combination in combinations:
        spike = combination[0]
        N = combination[1]
        total_for_combination = 0
        for _ in range(10):
            total_for_combination += simulate(spike, N)

        print(
            f"Average E_p(f) for spike = {spike} and N = {N} is: {total_for_combination / 10}"
        )


def manual_experiment():
    spike = float(input("Enter spikiness value: "))
    N = int(input("Enter number of iterations: "))
    time_avg = simulate(spike, N)
    print(f"Computed mean for spike = {spike} and N = {N} is: " + str(time_avg))


def main():
    automated_experiment()


if __name__ == "__main__":
    main()
