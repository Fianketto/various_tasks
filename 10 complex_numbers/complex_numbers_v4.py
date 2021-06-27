from math import atan2
import matplotlib.pyplot as plt


class ComplexNumber:
    # инициализация комплексного числа
    def __init__(self, a, b):
        self.a = a  # действительная часть
        self.b = b  # мнимая часть

    # запись в алгебраической форме
    def __repr__(self):
        a_repr = round(self.a, 3)
        b_repr = abs(round(self.b, 3))
        sign = "+" if self.b >= 0 else "-"
        return f"{a_repr} {sign} {b_repr}*i"

    # 1. сложение
    def __add__(self, other):
        return ComplexNumber(self.a + other.a, self.b + other.b)    # то складываем соответствующие части

    # 2. вычитание
    def __sub__(self, other):
        return ComplexNumber(self.a - other.a, self.b - other.b)

    # 3. умножение
    def __mul__(self, other):
        new_a = self.a * other.a - self.b * other.b                 # формула для действительной части произведения
        new_b = self.a * other.b + self.b * other.a                 # формула для мнимой части произведения
        return ComplexNumber(new_a, new_b)

    # 4. деление
    def __truediv__(self, other):
        den = other.a**2 + other.b**2
        new_a = (self.a * other.a + self.b * other.b) / den         # формула для действительной части частного
        new_b = (self.b * other.a - self.a * other.b) / den         # формула для мнимой части частного
        return ComplexNumber(new_a, new_b)

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

