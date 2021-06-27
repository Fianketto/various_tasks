import matplotlib.pyplot as plt
import numpy as np


# Определение функций (ВАРИАНТ 4)
def f1(x1, x2):
    return np.cos(x1) + x2 - 1.5


def f2(x1, x2):
    return 2 * x1 - np.sin(x2 - 0.5) - 1


# Массив точек для графика
delta = 0.01
x_range = np.arange(-5.0, 5.0, delta)
y_range = np.arange(-5.0, 5.0, delta)
x1p, x2p = np.meshgrid(x_range, y_range)

# Функции для графика
F1 = f1(x1p, x2p)
G1 = 0
F2 = f2(x1p, x2p)
G2 = 0


# Настройки полотна для графика
def set_plot_settings():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


# Есть 1 корень. Его приблизительное значение:
approx = (0.5, 0.5)


# Определяем частные производные функций
def df1_x1(x1, x2):
    return -np.sin(x1)


def df1_x2(x1, x2):
    return 1


def df2_x1(x1, x2):
    return 2


def df2_x2(x1, x2):
    return -np.cos(x2 - 0.5)


# Записываем метод аппроксимации Ньютона
def newton(f1, f2, df1_x1, df1_x2, df2_x1, df2_x2, x1_0, x2_0, epsilon, max_iter):
    # 1. начальное приближение
    x1_n = x1_0
    x2_n = x2_0
    for n in range(0, max_iter):
        # 2. значения функций на данной итерации
        f1_n = f1(x1_n, x2_n)
        f2_n = f2(x1_n, x2_n)
        if max(abs(f1_n), abs(f2_n)) < epsilon:
            print(f"Прошло итераций: {n}. Решение найдено")
            return x1_n, x2_n
        # 3. значения производных на данной итерации
        df1_x1_n = df1_x1(x1_n, x2_n)
        df1_x2_n = df1_x2(x1_n, x2_n)
        df2_x1_n = df2_x1(x1_n, x2_n)
        df2_x2_n = df2_x2(x1_n, x2_n)
        # 4. определители матрицы Якоби и матриц А1, А2
        detJ_n = df1_x1_n * df2_x2_n - df1_x2_n * df2_x1_n
        detA1_n = f1_n * df2_x2_n - df1_x2_n * f2_n
        detA2_n = df1_x1_n * f2_n - f1_n * df2_x1_n
        if detJ_n == 0:
            print("Нулевой определитель матрицы Якоби, решение не найдено")
            return None
        # 5. корни на следующей итерации
        x1_n = x1_n - detA1_n / detJ_n
        x2_n = x2_n - detA2_n / detJ_n
    print("Достигнуто максимальное число итераций. Решение не найдено")
    return None


# Находим более точное значение корня методом Ньютона
x1_0, x2_0 = approx
x1, x2 = newton(f1, f2, df1_x1, df1_x2, df2_x1, df2_x2, x1_0, x2_0, 1e-6, 100)
print(f"x1 = {x1}, x2 = {x2}")


# Рисуем графики и найденную точку пересечения (корень)
set_plot_settings()
plt.contour(x1p, x2p, (F1 - G1), [0], colors='red')
plt.contour(x1p, x2p, (F2 - G2), [0], colors='blue')
plt.plot(x1, x2, 'or')
plt.show()
