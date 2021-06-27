from complex_numbers_v5 import *


# 1. объявляем два комплексных числа
c1 = ComplexNumber(3, 4)
c2 = ComplexNumber(-5, 1)

# 2. выводим их на экран
print("c1 = ", c1)
print("c2 = ", c2)

# 3. проверяем складывание
print("c1 + c2 = ", c1 + c2)

# 4. проверяем вычитание
print("c1 - c2 = ", c1 - c2)

# 5. проверяем умножение
print("c1 * c2 = ", c1 * c2)

# 6. проверяем деление
print("c1 / c2 = ", c1 / c2)

# 7. модуль
print("r1 = ", c1.mod())
print("r2 = ", c2.mod())

# 8. аргумент
print("fi1 = ", c1.arg())
print("fi2 = ", c2.arg())

# 9. возведение в степень
print("с1 ** 5 = ", c1 ** 5)
print("с2 ** 3 = ", c2 ** 3)
print("с1 ** 1/2 = ", c1 ** (1/2))
print("с2 ** 1/3 = ", c2 ** (1/3))

# 9. показать на комплексной плоскости
c1.show()
c2.show()

