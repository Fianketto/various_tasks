import matplotlib.pyplot as plt
import numpy as np


# функция f(x, y) есть правая часть уравнения y' = f(x, y)
def f(x, y):
    return 0.5 * ((8 + 12 * np.cos(x)) * np.exp(2 * x) / y - 3 * y * np.cos(x))


# аналитическое решение
def sol(x):
    return 2 * (np.exp(2 * x)) ** 0.5


a = 0
b = 2
n = 5
y_0 = 2
h = (b - a) / n

x = [a + i * h for i in range(n + 1)]
y1 = [a] * (n + 1)      # в y1 запишем аналитическое решение
y2 = [a] * (n + 1)      # в y2 запишем решение усов. методом Эйлера
y3 = [a] * (n + 1)      # в y3 запишем решение методом Рунге-Кутта 4-го порядка

y1[0] = y2[0] = y3[0] = y_0

for i in range(0, n):
    # Аналитическое решение
    y1[i + 1] = sol(x[i + 1])

    # Решение усов. методом Эйлера
    y2[i + 1] = y2[i] + h * f(x[i] + h/2, y2[i] + h/2 * f(x[i], y1[i]))

    # Решение методом Рунге-Кутта 4-го порядка
    k1 = f(x[i], y3[i])
    k2 = f(x[i] + h/2, y3[i] + h/2 * k1)
    k3 = f(x[i] + h/2, y3[i] + h/2 * k2)
    k4 = f(x[i] + h, y3[i] + h * k3)
    y3[i + 1] = y3[i] + h/6 * (k1 + 2*k2 + 2*k3 + k4)


# Рисуем график
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.plot(x, y1, 'r', label='Analytical solution')
plt.plot(x, y2, 'b', label='Improved Euler')
plt.plot(x, y3, 'g', label='Runge-Kutta (IV)')

ax.legend()
plt.show()
