import random


EXIT, ADD_MATRIX, MUL_INT, MUL_MATRIX, TRANSPOSE, POWER = range(0, 6)   # Коды операций
USER_FILLING, RANDOM_FILLING = range(1, 3)                              # Коды методов заполнения матриц
OPERATIONS = list(range(0, 6))                                          # Список с кодами операций
FILLING_METHODS = list(range(1, 3))                                     # Список с кодами методов заполнения

# Подсказка при выборе операции
PROMPT_STRING_OPERATION = """
Введите номер операциии, которую Вы хотите применить:
1 - Сложение матриц
2 - Умножение матрицы на число
3 - Умножение матриц
4 - Транспонирование матрицы
5 - Возведение матрицы в степень
0 - Выход и завершение программы\n"""

# Подсказка при вводе размерности первой матрицы
PROMPT_STRING_DIMENSIONS1 = """
Введите размерность матрицы через пробел (например, 4 5)
При выборе операции возведения в степень матрица должна быть квадратной\n"""

# Подсказка при вводе размерности второй матрицы
PROMPT_STRING_DIMENSIONS2 = """
Введите размерность второй матрицы через пробел (например, 4 5)
Количество строк второй матрицы должно равняться количеству столбцов первой матрицы\n"""

# Подсказка при выборе метода заполнения матриц
PROMPT_STRING_FILLING = """
Выберите способ заполнения матриц(ы):
1 - Ввод элементов вручную
2 - Случайное заполнение\n"""

# Подсказка при ручном вводе элементов матрицы
PROMPT_STRING_GET_MATRIX = """
Введите элементы матрицы построчно. В каждой строке разделяйте элементы пробелами\n"""

# Подсказка при вводе множителя
PROMPT_STRING_MULTIPLIER = """
Введите число, на которое нужно умножить матрицу\n"""

# Подсказка при вводе степени
PROMPT_STRING_POWER = """
Введите степень, в которую нужно возвести матрицу (натуральное число)\n"""

# Сообщение об ошибке, показываемое при неверно введенных данных
ERROR_STRING = "Неверные данные. Попробуйте еще раз"


# Класс матриц для удобного применения операций
class Matrix:
    # Инициализация размерностью и элементами
    def __init__(self, m: int, n: int, arr: list):
        self.m = m
        self.n = n
        self.arr = [[arr[i][j] for j in range(n)] for i in range(m)]

    # Аккуратный вывод на экран
    def __str__(self):
        repr = ""
        for i in range(self.m):
            for j in range(self.n):
                repr += f"{self.arr[i][j]:6} "
            repr += "\n"
        return repr

    # Транспонирование
    def transpose(self):
        new_arr = [[self.arr[i][j] for i in range(self.m)] for j in range(self.n)]
        return Matrix(self.n, self.m, new_arr)

    # Сложение двух матриц
    def __add__(self, other):
        new_arr = [[self.arr[i][j] + other.arr[i][j] for j in range(self.n)] for i in range(self.m)]
        return Matrix(self.m, self.n, new_arr)

    # Умножение матрицы на число или на другую матрицу
    def __mul__(self, other):
        # Если умножается на число
        if isinstance(other, int) or isinstance(other, float):
            # То каждый элемент умножаем на число
            new_arr = [[self.arr[i][j] * other for j in range(self.n)] for i in range(self.m)]
            return Matrix(self.m, self.n, new_arr)
        # Если же умножается на матрицу
        elif isinstance(other, Matrix):
            # То элементы получаемой матрицы считаем по правилу умножения матриц
            new_arr = [[0 for j in range(other.n)] for i in range(self.m)]
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        new_arr[i][j] += self.arr[i][k] * other.arr[k][j]
            return Matrix(self.m, other.n, new_arr)

    # Возведение в степень
    def __pow__(self, power, modulo=None):
        # Возведение есть просто умножение матрицы на саму себя
        # Инициализируем "первую" степень
        m1 = Matrix(self.m, self.n, self.arr)
        # Далее в цикле умножаем необходимое число раз
        for i in range(power - 1):
            m1 = m1 * self
        return m1


# Функция для получения элементов матрицы от пользователя
def get_matrix_from_user(m: int, n: int, num: int):
    print(PROMPT_STRING_GET_MATRIX)
    print(f"Ожидаемая размерность {num + 1}-ой матрицы: {m} x {n}")
    # Инициализируем матрицу (точнее пока только список списков)
    arr = [[0 for j in range(n)] for i in range(m)]
    # В цикле читаем m строк
    for i in range(m):
        next_line = list(map(int, input().split()))
        # Если в строке НЕ n элементоа, то выбрасываем ошибку
        if len(next_line) != n:
            raise ValueError
        arr[i] = next_line
    return Matrix(m, n, arr)


# Функция для случайной генерации матрицы
def generate_random_matrix(m: int, n: int):
    arr = [[random.randint(-10, 10) for j in range(n)] for i in range(m)]
    return Matrix(m, n, arr)


while True:     # Зацикливание всей программы (Основной цикл)
    matrix_count = 1            # Количество требуемых матриц. По умолчанию 1. Для умножения и сложения - 2
    dim = [[1, 1], [1, 1]]      # Размерности матриц. По умолчанию обе матрицы 1х1 (далее уточняются у пользователя)
    matrices = [None, None]     # Сами матрицы
    multiplier = 0              # Множитель
    power = 0                   # Степень

    # 1. Выбор операции
    while True:     # Не выходим из этого цикла, пока пользователь не введет валидный номер операцию
        try:
            operation_num = int(input(PROMPT_STRING_OPERATION))
            if operation_num in OPERATIONS:     # Если выбран валидный номер, то выходим. В иных случаях - повтор!
                break
            else:
                print(ERROR_STRING)
        except:
            print(ERROR_STRING)

    if operation_num == EXIT:   # Если введено 0 - выходим из основного цикла (завершается программа)
        break

    # 2. Ввод размерности матрицы
    while True:     # Не выходим из этого цикла, пока пользователь не введет валидную размерность
        try:
            dim[0] = list(map(int, input(PROMPT_STRING_DIMENSIONS1).split()))
            # condition1 - выбрана операция, отличная от возведения в степень, и оба измерения положительны
            # condition2 - выбрано возведение в степень, измерения положительны и равны
            condition1 = operation_num != POWER and len(dim[0]) == 2 and dim[0][0] > 0 and dim[0][1] > 0
            condition2 = operation_num == POWER and len(dim[0]) == 2 and 0 < dim[0][0] == dim[0][1]
            if condition1 or condition2:
                break
            else:
                print(ERROR_STRING)
        except:
            print(ERROR_STRING)

    # 3. Ввод дополнительных данных
    # 3.1 Если выбрано умножение, то нужно ввести еще размерность второй матрицы
    if operation_num == MUL_MATRIX:
        matrix_count = 2
        while True:     # Не выходим из этого цикла, пока пользователь не введет валидную размерность второй матрицы
            try:
                dim[1] = list(map(int, input(PROMPT_STRING_DIMENSIONS2).split()))
                if len(dim[1]) == 2 and dim[1][0] == dim[0][1] and dim[1][1] > 0:
                    break
                else:
                    print(ERROR_STRING)
            except:
                print(ERROR_STRING)
    # 3.2 Если выбрано сложение матриц, то нужна вторая матрица такой же размерности
    elif operation_num == ADD_MATRIX:
        matrix_count = 2
        dim[1][0], dim[1][1] = dim[0][0], dim[0][1]
    # 3.3 Если выбрано умножение на число, то нужно ввести это число
    elif operation_num == MUL_INT:
        while True:     # Не выходим из этого цикла, пока пользователь не введет валидный множитель (целое число)
            try:
                multiplier = int(input(PROMPT_STRING_MULTIPLIER))
                break
            except:
                print(ERROR_STRING)
    # 3.3 Если выбрано возведение в степень, то нужно ввести натуральную степень
    elif operation_num == POWER:
        while True:     # Не выходим из этого цикла, пока пользователь не введет валидную степень (натуральное число)
            try:
                power = int(input(PROMPT_STRING_POWER))
                if power > 0:
                    break
                else:
                    print(ERROR_STRING)
            except:
                print(ERROR_STRING)

    # 3. Выбор способа заполнения
    while True:     # Не выходим из этого цикла, пока пользователь не введет валидный номер метода заполнения (1 или 2)
        try:
            filling_method = int(input(PROMPT_STRING_FILLING))
            if filling_method in FILLING_METHODS:
                break
            else:
                print(ERROR_STRING)
        except:
            print(ERROR_STRING)

    # 4. Заполнение матриц
    if filling_method == USER_FILLING:  # Если выбрано ручное заполнение
        for i in range(matrix_count):   # То для одной или двух матриц требуем ввести элементы
            while True:     # Не выходим из этого цикла, пока пользователь не введет валидную матрицу
                try:
                    # Если введена невалидная матрица, то функция get_matrix_from_user() выбросит ошибку и мы попадем в
                    # except, и тогда не выйдем из цикла
                    matrices[i] = get_matrix_from_user(dim[i][0], dim[i][1], i)
                    break
                except:
                    print(ERROR_STRING)
    elif filling_method == RANDOM_FILLING:
        for i in range(matrix_count):
            matrices[i] = generate_random_matrix(dim[i][0], dim[i][1])

    # 5. Получение результата
    if operation_num == ADD_MATRIX:
        result_matrix = matrices[0] + matrices[1]
        print(f"Матрица A:\n{matrices[0]}\n\nМатрица B:\n{matrices[1]}\nОперация: сложение")
    elif operation_num == MUL_INT:
        result_matrix = matrices[0] * multiplier
        print(f"Матрица A:\n{matrices[0]}\n\nМножитель:\n{multiplier}\nОперация: умножение на число")
    elif operation_num == MUL_MATRIX:
        result_matrix = matrices[0] * matrices[1]
        print(f"Матрица A:\n{matrices[0]}\n\nМатрица B:\n{matrices[1]}\nОперация: умножение")
    elif operation_num == TRANSPOSE:
        result_matrix = matrices[0].transpose()
        print(f"Матрица A:\n{matrices[0]}\nОперация: транспонирование")
    elif operation_num == POWER:
        result_matrix = matrices[0] ** power
        print(f"Матрица A:\n{matrices[0]}\n\nСтепень:\n{power}\nОперация: возведение в степень")

    print(f"Результат:\n{result_matrix}\n======================================")
