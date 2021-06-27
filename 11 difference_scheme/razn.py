from math import sin, cos, atan
import matplotlib.pyplot as plt


#   1. Функция g
def get_g(u: float, x: float):
    g = 3*u + 10 * u**3 + x**2                  # Пример на странице 34
    #g = A_coef * u * abs(u) - C_coef            # Вариант 1
    #g = A_coef * (2 * u + sin(u)) - C_coef      # Вариант 3
    #g = A_coef * (2 * u + atan(u)) - C_coef     # Вариант 9

    return g


#   2. Производная функции g
def get_derivative_of_g(u: float):
    dg = 3 + 30 * u**2                  # Пример на странице 34
    #dg = A_coef * 2 * abs(u)            # Вариант 1
    #dg = A_coef * (2 + cos(u))          # Вариант 3
    #dg = A_coef * (2 + 1 / (u**2 + 1))  # Вариант 9

    return dg


#   3.  Функция для решения системы методом подгонки
#       применяется, когда матрица коэффициентов системы имеет трехдиагональный вид
def tridiagonal_matrix_algorithm(A, d):
    """
    :param A: матрица коэффициентов
    :param d: вектор свободных членов
    :return: решение в виде вектора x
    """
    # 3.1. кол-во строк/столбцов
    n = len(d)
    # 3.2. необходимые коэффициенты прогонки
    b = [A[i][i] for i in range(n)]
    a = [0] + [A[i][i - 1] for i in range(1, n)]
    c = [A[i][i + 1] for i in range(n - 1)] + [0]
    y = [0 for _ in range(n)]
    x = [0 for _ in range(n)]
    alpha = [0 for _ in range(n)]
    beta = [0 for _ in range(n)]

    # 3.3. инициализация коэффициентов
    y[0] = b[0]
    alpha[0] = -c[0] / y[0]
    beta[0] = d[0] / y[0]

    # 3.4. прямой ход прогонки
    for i in range(1, n - 1):
        y[i] = b[i] + a[i] * alpha[i - 1]
        alpha[i] = -c[i] / y[i]
        beta[i] = (d[i] - a[i] * beta[i - 1]) / y[i]

    y[n - 1] = b[n - 1] + a[n - 1] * alpha[n - 2]
    beta[n - 1] = (d[n - 1] - a[n - 1] * beta[n - 2]) / y[n - 1]

    # 3.5.  обратный ход прогонки
    x[n - 1] = beta[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i + 1] + beta[i]

    return x


#   4. Функция для инициализации матрицы коэффициентов A
def initialize_matrix_A(row_count: int):
    # 4.1. Объявляем матрицу
    A = [[] for _ in range(row_count)]

    # 4.2. Первая и последняя строки
    first_row = [2, -1] + [0] * (row_count - 2)
    last_row = [0] * (row_count - 2) + [-1, 2]
    A[0] = first_row
    A[row_count - 1] = last_row

    # 4.3. Остальные строки (получаеются смещением (-1, 2, -1) вправо
    for i in range(1, row_count - 1):
        A[i] = [0]*(i - 1) + [-1, 2, -1] + [0]*(row_count - 2 - i)

    return A


#   5. Функция для получения вектора H
def get_H(u: list, x: list, h: float):
    row_count = len(u)
    H = [0.0 for _ in range(row_count)]
    for i in range(row_count):
        row = get_g(u[i], x[i]) * h**2
        H[i] = row
    return H


#   6. Функция для получения матрицы Якоби J (или H штрих в обозначениях методички)
def get_J(u: list):
    row_count = len(u)
    J = [[0 for j in range(row_count)] for i in range(row_count)]
    for i in range(row_count):
        J[i][i] = get_derivative_of_g(u[i])
    return J


#   7. Далее идут вспомогательные функции

#   7.1. Суммирование матриц
def get_sum_of_matrices(M1, M2):
    row_count = len(M1)
    M3 = [[0 for j in range(row_count)] for i in range(row_count)]
    for i in range(row_count):
        for j in range(row_count):
            M3[i][j] = M1[i][j] + M2[i][j]
    return M3


#   7.2. Суммирование векторов
def get_sum_of_vectors(v1, v2):
    row_count = len(v1)
    v3 = [0 for _ in range(row_count)]
    for i in range(row_count):
        v3[i] = v1[i] + v2[i]
    return v3


#   7.3. Произведение матрицы и вектора
def get_product_of_matrix_and_vector(M, v):
    row_count = len(M)
    prod = [0 for _ in range(row_count)]
    for i in range(row_count):
        for j in range(row_count):
            prod[i] += M[i][j] * v[j]
    return prod


#   7.1. Произвдение вектора и скалярной величины
def get_product_of_vector_and_scalar(v, s):
    row_count = len(v)
    v2 = [s * v[i] for i in range(row_count)]
    return v2


#   8. Функция для проверки того, что все координаты вектора поправки по абс. величине меньше точности eps
def is_less_than_eps(y: list, eps: float):
    is_less = True
    for i in range(len(y)):
        if abs(y[i]) >= eps:
            is_less = False
            break
    return is_less


#   9. Функция для нахождения решения методом Ньютона
def newton_method(A: list, u: list, x: list, h: float):
    u0 = u                                              # вектор решений на текущей итерации
    J = get_J(u0)                                       # матрица Якоби
    A_new = get_sum_of_matrices(A, J)                   # итоговая матрица коэффициентов перед y
    H = get_H(u0, x, h)                                 # вектор H
    prod = get_product_of_matrix_and_vector(A, u0)      # 1-ый шаг вычисления вектора свободных членов
    d = get_sum_of_vectors(prod, H)                     # 2-ой шаг вычисления вектора свободных членов
    d = get_product_of_vector_and_scalar(d, -1)         # итоговый вектор свободных членов
    y = tridiagonal_matrix_algorithm(A_new, d)          # решаем методом прогонки и получаем y - вектор поправки
    return y


#   10. Функция для рисования графика
def draw_graph(x: list, u: list):
    # 10.1. Настройки полотна для графика
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # 10.2. Точки для рисования
    x_graph = [0.0] + x + [1.0]
    y_graph = [0.0] + u + [0.0]

    # 10.3. Рисуем график
    plt.plot(x_graph, y_graph, 'or', label='u = u(x)')
    plt.xlabel("x")
    plt.ylabel("u(x)")
    ax.legend()
    plt.show()


#   11. Ход алгоритма =================================================================================================

#   11.1. Начальные данные
h = 0.03                                 # задаем шаг
eps = 10**(-8)                          # задаем точность
n = int(1 / h) + 1                      # вычисляем кол-во узлов

A_coef = float(input("Введите A\n"))    # запрашиваем коэффициент A
C_coef = float(input("Введите C\n"))    # запрашиваем коэффициент C

x = [h * i for i in range(1, n - 1)]   # координаты узлов
u = [0 for i in range(n - 2)]           # вектор, в который запишем значения функции u в этих узлах (в начале нулевой)

A = initialize_matrix_A(n - 2)          # инициализируем матрицу коэффициентов для заданного n
iter = 0                                # текущая итераци для метода Ньютона
max_iter = 20000                        # максимальное кол-во итераций
enough = False                          # переменная для хранения информации о том, что вектор поправок стал достаточно мал


#   11.2. Запускаем основной цикл для метода Ньютона
while iter < max_iter and not enough:
    y = newton_method(A, u, x, h)       # ищем вектор поправок методом Ньютона
    if is_less_than_eps(y, eps):
        enough = True
    u = get_sum_of_vectors(u, y)        # обновляем вектор u, прибавляя поправку
    iter += 1
    print(iter)


#   11.3. Печатаем полученное решение
for ui in u:
    print(ui)


#   11.4. Рисуем график
draw_graph(x, u)
