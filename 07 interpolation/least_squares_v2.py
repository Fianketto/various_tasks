import matplotlib.pyplot as plt
import numpy as np
import random


def least_squares(x, y):
    n = len(x)
    s1 = s2 = s3 = s4 = 0
    f1 = f2 = f3 = 0
    for i in range(n):
        s1 += x[i]
        s2 += x[i]**2
        s3 += x[i]**3
        s4 += x[i]**4
        f1 += y[i]
        f2 += y[i] * x[i]
        f3 += y[i] * x[i]**2

    A = [[s2, s1, n], [s3, s2, s1], [s4, s3, s2]]
    f = [f1, f2, f3]

    [a, b, c] = np.linalg.solve(A, f)
    return [a, b, c]


# Пример вызова функции
n = 50          # количество точек
min_x = 0       # левый конец отрезка для генерации точек
max_x = 10      # правый конец отрезка для генерации точек
delta = 5       # максимально случайное отклонение ординаты токи от истинного значения (т.е. от x**2)

x = [0.0 for i in range(n)]
y = [0.0 for i in range(n)]

for i in range(n):
    x[i] = random.random() * (max_x - min_x) + min_x        # случайные x
    y[i] = x[i]**2 + random.random() * delta * 2 - delta    # случайные y

a, b, c = least_squares(x, y)                               # находим коэффициенты параболы


def get_y_of(x):
    return a * x**2 + b * x + c


# Рисуем график
# Параметры оси
# Настройки полотна для графика
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# 5.3. Точки аппроксимирующей параболы
x_graph = np.linspace(min_x, max_x, 1000)
y_graph = [get_y_of(x_i) for x_i in x_graph]

plt.plot(x_graph, y_graph, 'r', label='Least squares approximation')
plt.plot(x, y, 'or', label='x')
ax.legend()
plt.show()
