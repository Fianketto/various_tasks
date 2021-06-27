# Задача 25
start_num = 59999
end_num = 64000
# Здесь будем хранить кол-во делителей каждого числа
factor_count = [0 for i in range(start_num, end_num + 1)]

for i in range(start_num, end_num + 1):
    # Достаточно проверить делимость до чисел, не превышающих корня из данного числа
    upper_bound = i ** 0.5
    for j in range(1, int(upper_bound) + 1):
        if i % j == 0:
            # Если данное число i делится на j, то добавляем сразу 2 делителя (j и i/j - они оба являются делителями i)
            factor_count[i - start_num] += 2

    # Если число i является полным квадратом, то мы по ошибке учли его корень как 2 разных делителя
    # поэтому общее число делителей уменьшаем на 1
    if int(str(upper_bound-int(upper_bound))[2:]) == 0:
        factor_count[i - start_num] -= 1


# максимальное кол-во делителей
max_factor_count = max(factor_count)
num_with_max_factor_count = 0

# находим само такое число (максимальное)
for i in range(start_num, end_num + 1):
    if factor_count[i - start_num] == max_factor_count:
        num_with_max_factor_count = i

print(max_factor_count, num_with_max_factor_count)
