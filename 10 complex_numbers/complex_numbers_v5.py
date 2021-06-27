from math import atan2, sin, cos, pi
import matplotlib.pyplot as plt


class ComplexNumber:
    # инициализация комплексного числа
    def __init__(self, a, b):
        self.a = a  # действительная часть
        self.b = b  # мнимая часть

    # запись в тригонометрической форме
    def __repr__(self):
        r = round(self.mod(), 3)                        # модуль числа
        fi = round(self.arg() / pi, 3)                  # аргумент числа (в терминах pi)
        fi = round(fi, 3)                               # округляем для удобного отображения
        return f"{r} * (cos({fi}pi) + i*sin({fi}pi))"

    # 1. сложение
    def __add__(self, other):
        return ComplexNumber(self.a + other.a, self.b + other.b)    # то складываем соответствующие части

    # 2. вычитание
    def __sub__(self, other):
        return ComplexNumber(self.a - other.a, self.b - other.b)

    # 3. умножение в тригонометрической форме
    def __mul__(self, other):
        r1, r2 = self.mod(), other.mod()                            # модули чисел
        fi1, fi2 = self.arg(), other.arg()                          # аргументы чисел
        r3 = r1 * r2                                                # модуль произведения
        fi3 = fi1 + fi2                                             # аргумент произведения
        a3, b3 = r3 * cos(fi3), r3 * sin(fi3)                       # действительная и мнимая части произведения
        return ComplexNumberAlgebraic(a3, b3)

    # 4. деление в тригонометрической форме
    def __truediv__(self, other):
        r1, r2 = self.mod(), other.mod()                            # модули чисел
        fi1, fi2 = self.arg(), other.arg()                          # аргументы чисел
        r3 = r1 / r2                                                # модуль произведения
        fi3 = fi1 - fi2                                             # аргумент произведения
        a3, b3 = r3 * cos(fi3), r3 * sin(fi3)                       # действительная и мнимая части произведения
        return ComplexNumberAlgebraic(a3, b3)

    # 5. возведение в степень с использованием формулы Муавра
    def __pow__(self, n):
        r = self.mod()                      # модуль числа
        fi = self.arg()                     # аргумент чисела
        r2 = r ** n                         # модуль результирующего числа
        fi2 = fi * n                        # аргумент результирующего числа
        a2, b2 = r2 * cos(fi2), r2 * sin(fi2)  # действительная и мнимая части результирующего числа
        return ComplexNumberAlgebraic(a2, b2)

    # Модуль комплексного числа
    def mod(self):
        return round((self.a**2 + self.b**2) ** 0.5, 3)

    # Аргумент комплексного числа
    def arg(self):
        return round(atan2(self.b, self.a), 3)

    # Показать точку на комплексной плоскости
    def show(self):
        # создаем окно
        fig = plt.figure()
        # добавляем плоскость для рисования
        ax = fig.add_subplot(1, 1, 1)
        # добавляем сетку
        ax.grid(which='both')
        # добавляем оси и настраиваем их
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        # добавляем деления
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # рисуем точку
        ax.plot([self.a], [self.b], 'or')
        # устанавливаем диапазон осей
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        # добавляем подписи
        ax.set_xlabel('Re', loc='right')
        ax.set_ylabel('Im', loc='top')
        # выводим на экран
        plt.show()


class ComplexNumberAlgebraic(ComplexNumber):
    # запись в алгебраической форме
    def __repr__(self):
        a_repr = round(self.a, 3)
        b_repr = abs(round(self.b, 3))
        sign = "+" if self.b >= 0 else "-"
        return f"{a_repr} {sign} {b_repr}*i"

