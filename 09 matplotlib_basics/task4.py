import numpy as np
import matplotlib.pyplot as plt


try:
    x_param = float(input("введите x\n"))
    n = np.arange(1, 11)
    y = x_param ** n / n

    fig, ax = plt.subplots()
    ax.bar(n, y)
    plt.xticks(n)

    plt.show()
except ValueError:
    print("непраильное число")

