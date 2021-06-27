import matplotlib.pyplot as plt
import numpy as np


def aitken(x_input, y_input, xx):
    # 0. Для начала сортируем точки по возрастанию x
    n = len(x_input)
    all_points = [[x_input[i], y_input[i]] for i in range(n)]               # координаты всех точек в одном списке
    all_points.sort(key=lambda p: p[0])                                     # сортируем
    x, y = [p[0] for p in all_points], [p[1] for p in all_points]           # заново переписываем в отдельные списки

    # 1. В список yy будут записаны значения, которые вернет функция
    yy = [0.0] * len(xx)
    print(f"x={x}\ny={y}")

    # 2. Определим функции
    # 2.1. многочлен Лагранжа
    def get_L(x0, xi, xi1, yi, yi1):
        Lx = 1 / (xi1 - xi) * (yi * (xi1 - x0) - yi1 * (xi - x0))
        return Lx

    # 2.2. Значение y для заданной точки x0
    def get_y_of(x0):
        L = [0.0 for _ in range(n - 1)]
        for i in range(n - 1):
            L[i] = get_L(x0, x[i], x[i + 1], y[i], y[i + 1])

        for k in range(2, n):
            L_prev = L[:]
            for i in range(n - k):
                L[i] = get_L(x0, x[i], x[i + k], L_prev[i], L_prev[i + 1])

        return L[0]

    # 3. Для каждого x из списка xx вычисляем значение y
    for i in range(len(xx)):
        x_new = xx[i]
        y_new = get_y_of(x_new)
        yy[i] = y_new

    # 4. Рисуем график
    # 4.1. Параметры оси
    max_x = max(x + xx)
    min_x = min(x + xx)
    # 4.2. Настройки полотна для графика
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # 4.3. Точки кубического сплайна
    x_graph = np.linspace(min_x, max_x, 1000)
    y_graph = [get_y_of(x_i) for x_i in x_graph]

    # 4.4. Рисуем график
    plt.plot(x_graph, y_graph, 'r', label='Aitken interpolation')
    plt.plot(x, y, 'or', label='x')
    plt.plot(xx, yy, 'ob', label='xx')
    ax.legend()
    plt.show()

    return yy


# Пример вызова функции
x = [8.8, 1, 1.5, 2.9, 4.4, 8, 10, 12]
y = [3, 20, 5, 6, 9, 15, 9, 12]
xx = [2, 6, 2, 12.5]
yy = aitken(x, y, xx)


