import numpy as np
import random
import math
import matplotlib.pyplot as plt
'''
Monte carlo simulation for randomly throwing darts at a dark board.
(Circle within a square)
'''

# N = 10000000 # 10 million
N = 1000
R = 1

def in_circle(x_p, y_p, r):

    d = math.sqrt((x_p ** 2) + (y_p ** 2))

    return d <= r

def run_monte_carlo_simulation():

    results = []
    for n in [10 ** p for p in range(6)]:
        print(n)

        hits = []
        for _ in range(n):
            x = random.randint(R * -100, R *100) / 100
            y = random.randint(R * -100, R *100) / 100
            hit = in_circle(x, y, R)
            hits.append(hit)

        ratio = (sum(hits) / len(hits)) * 100
        results.append((n, ratio))

    print(results)
    return results

if __name__ == "__main__":

    res = [(10, 70.0), (100, 76.0), (1000, 79.4), (10000, 77.75999999999999), (100000, 77.778), (1000000, 77.7767), (10000000, 77.75034)]
    x_val = [i + 1 for i, x in enumerate(res)]
    y_val = [y[1] for y in res]

    plt.plot(x_val, y_val)
    plt.plot(x_val,y_val,'or')
    plt.title("Monte carlo simulation for points inside a circle within a square of radius R")
    plt.xlabel("Simulations (10^x)")
    plt.ylabel("Hit ratio (%)")
    plt.show()