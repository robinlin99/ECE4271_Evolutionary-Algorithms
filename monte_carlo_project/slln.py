import math
import random


def q(m, n, spike):
    return 1 / (1 + (abs(m - 50)) ** spike + (abs(n - 50)) ** spike)


def main():
    spike = float(input("Enter spikiness value: "))
    N = int(input("Enter number of iterations: "))

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

    print("Computed mean = " + str(time_avg))


if __name__ == "__main__":
    main()
