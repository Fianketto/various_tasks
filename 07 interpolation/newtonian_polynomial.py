import matplotlib.pyplot as plt
import numpy as np


def newtonian_polynomial(x, y, xx):
    n = len(x)
    h = x[1] - x[0]

    # 1. В список yy будут записаны значения, которые вернет функция
    yy = [0.0] * len(xx)
    print(f"x={x}\ny={y}")

    # 2. Конечные разности
    dy = [[] for i in range(n)]
    dy[0] = y[:]
    for i in range(1, n):
        for j in range(n - i):
            dy[i].append(dy[i - 1][j + 1] - dy[i - 1][j])

    # 3. Вспомогательная функция - факториал
    def factorial(m):
        result = 1
        for i in range(1, m + 1):
            result *= i
        return result

    # 4. Значение y для заданной точки x0
    def get_y_of(x0):
        P = 0
        for i in range(n):
            f = 1
            for j in range(i):
                f *= (x0 - x[j])
            P += f * dy[i][0] / (h**i * factorial(i))
        return P

    # 5. Для каждого x из списка xx вычисляем значение y
    for i in range(len(xx)):
        x_new = xx[i]
        y_new = get_y_of(x_new)
        yy[i] = y_new

    # 6. Рисуем график
    # 6.1. Параметры оси
    max_x = max(x + xx)
    min_x = min(x + xx)
    # 6.2. Настройки полотна для графика
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # 6.3. Точки кубического сплайна
    x_graph = np.linspace(min_x, max_x, 1000)
    y_graph = [get_y_of(x_i) for x_i in x_graph]

    # 6.4. Рисуем график
    plt.plot(x_graph, y_graph, 'r', label='Newtonian polynomial')
    plt.plot(x, y, 'or', label='x')
    plt.plot(xx, yy, 'ob', label='xx')
    ax.legend()
    plt.show()

    return yy


# Пример вызова функции. Шаг h расположения иксов должен быть одинаковым
x = [1, 3, 5, 7, 9, 11, 13, 15]
y = [3, 20, 5, 6, 9, 15, 9, 12]
xx = [2.5, 4.5, 5, 10, 1.2, 14.5, 9.9, 4.4, 5.9]


yy = newtonian_polynomial(x, y, xx)


