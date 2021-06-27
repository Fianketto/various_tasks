from math import exp, sin, cos, pi
import cmath
import matplotlib.pyplot as plt
import numpy as np

'''
Линейное диф. ур-ие 2го порядка с пост. коэф-ами
y'' + py' + qy = 0
'''


def solve(p, q, x1, y1, x2, y2, show_graph=False):
    print(f"\n\nРешаем уравнение y'' + {p}y' + {q} = 0")
    print(f"Граничные условия:\ny({x1}) = {y1}\ny({x2}) = {y2}")
    D = p * p - 4 * q
    if D > 0:
        func = solve_d_gt_0(p, q, x1, y1, x2, y2)
    elif D == 0:
        func = solve_d_eq_0(p, q, x1, y1, x2, y2)
    else:
        func = solve_d_lt_0(p, q, x1, y1, x2, y2)

    if show_graph:
        # Массив точек для графика
        x = np.linspace(-3, 3, 1000)
        y = func(x)

        # Настройки полотна для графика
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # Рисуем график
        plt.plot(x, y, 'r')
        plt.plot(x1, y1, 'or')
        plt.show()


def solve_d_gt_0(p, q, x1, y1, x2, y2):
    D = p * p - 4 * q
    print(f"\nD = {D} > 0")

    lmb1 = (-p + D ** 0.5) / 2
    lmb2 = (-p - D ** 0.5) / 2

    C1 = (y2 - y1 * exp(lmb2 * x2 - lmb2 * x1)) / (exp(lmb1 * x2) - exp(lmb1 * x1 + lmb2 * x2 - lmb2 * x1))
    C2 = (y1 - C1 * exp(lmb1 * x1)) / exp(lmb2 * x1)
    C1 = round(C1, 3)
    C2 = round(C2, 3)
    lmb1 = round(lmb1, 3)
    lmb2 = round(lmb2, 3)

    print(f"lmb1 = {lmb1}, lmb2 = {lmb2}")
    print(f"C1 = {C1}, C2 = {C2}")
    print(f"Решение: y = {C1}*exp({lmb1}*x) + {C2}*exp({lmb2}*x)")

    def func(x):
        return C1 * np.exp(lmb1 * x) + C2 * np.exp(lmb2 * x)

    return func


def solve_d_eq_0(p, q, x1, y1, x2, y2):
    D = p * p - 4 * q
    print(f"\nD = 0")
    lmb = -p / 2

    if x1 == 0:
        C1 = y1 / exp(lmb * x1)
        C2 = (y2 - C1 * exp(lmb * x2)) / (x2 * exp(lmb * x2))
    else:
        C1 = (y2 / exp(lmb * x2) - y1 * x2 / (x1 * exp(lmb * x1))) / (1 - x2 / x1)
        C2 = (y1 - C1 * exp(lmb * x1)) / (x1 * exp(lmb * x1))
    C1 = round(C1, 3)
    C2 = round(C2, 3)
    lmb = round(lmb, 3)

    print(f"lmb = {lmb}")
    print(f"C1 = {C1}, C2 = {C2}")
    print(f"Решение: y = {C1}*exp({lmb}*x) + {C2}*x*exp({lmb}*x)")

    def func(x):
        return C1 * np.exp(lmb * x) + C2 * x * np.exp(lmb * x)

    return func


def solve_d_lt_0(p, q, x1, y1, x2, y2):
    D = p * p - 4 * q
    print(f"\nD = {D} < 0")
    lmb = (-p + cmath.sqrt(D)) / 2
    a = lmb.real
    b = lmb.imag

    if sin(b * x1) == 0:
        C1 = y1 / (exp(a * x1) * cos(b * x1))
        C2 = (y2 / exp(a * x2) - C1 * cos(b * x2)) / sin(b * x2)
    elif cos(b * x2) == 0:
        C2 = y2 / (exp(a * x2) * sin(b * x2))
        C1 = (y1 / exp(a * x1) - C2 * sin(b * x1)) / cos(b * x1)
    else:
        f = y2 / (cos(b * x2) * exp(a * x2))
        g = (sin(b * x2) * y1) / (cos(b * x2) * sin(b * x1) * exp(a * x1))
        h = 1 - sin(b * x2) * cos(b * x1) / cos(b * x2)
        C1 = (f - g) / h
        C2 = (y1 / exp(a * x1) - C1 * cos(b * x1)) / sin(b * x1)

    C1 = round(C1, 3)
    C2 = round(C2, 3)
    a = round(a, 3)
    b = round(b, 3)

    print(f"lmb = {a} + {b}i")
    print(f"C1 = {C1}, C2 = {C2}")
    print(f"Решение: y = exp({a}*x) * ({C1}*cos({b}*x) + {C2}*sin({b}*x))")

    def func(x):
        return np.exp(a * x) * (C1 * np.cos(b * x) + C2 * np.sin(b * x))

    return func


show_examples = True
get_user_data = False

if show_examples:
    # 1. D > 0
    solve(1, -2, 0, 16, 3, 6 * exp(3) + 10 * exp(-6), show_graph=True)

    # 2. D = 0
    solve(-2, 1, 0, 2, 1, 5 * exp(1), show_graph=True)

    # 3. D < 0
    solve(-2, 10, 0, 5, pi / 6, 4 * exp(pi / 6), show_graph=True)

if get_user_data:
    print("Для решения уравнения y'' + py' + qy = 0 введите коэффициенты и граничные условия"
          "\ny(x1) = y1"
          "\ny(x2) = y2"
          )
    p = float(input("p = "))
    q = float(input("q = "))
    x1 = float(input("x1 = "))
    y1 = float(input("y1 = "))
    x2 = float(input("x2 = "))
    y2 = float(input("y2 = "))

    solve(p, q, x1, y1, x2, y2, show_graph=True)
