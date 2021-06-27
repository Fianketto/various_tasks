# Задача 27

# Читаем файл
with open("C.txt") as fin:
    content = fin.readlines()

# Записываем прочитанные данные в массив
n = int(content[0])
arr = list(map(int, content))[1:]


all_even = []       # Все четные числа
all_odd = []        # Все нечетные числа

div37_even = []     # Четные числа, кратные 37
div37_odd = []      # Нечетные числа, кратные 37


arr.sort(reverse=True)
for e in arr:
    if e % 2 == 0:
        all_even.append(e)
        if e % 37 == 0:
            div37_even.append(e)
    else:
        all_odd.append(e)
        if e % 37 == 0:
            div37_odd.append(e)


# Пару с макимальной суммой и разной четностью можно получить
# либо из: максимальное четное + максимальное нечетное, кратное 37
# либо из: максимальное нечетное + максимальное четное, кратное 37
try:
    o1, e1 = div37_odd[0], all_even[0]
except IndexError:
    o1, e1 = 0, 0

try:
    o2, e2 = all_odd[0], div37_even[0]
except IndexError:
    o2, e2 = 0, 0

# первая и вторая пары.
# находим максимальное
first_pair_sum = o1 + e1
second_pair_sum = o2 + e2
if first_pair_sum > second_pair_sum:
    print(o1, e1)
elif first_pair_sum < second_pair_sum:
    print(o2, e2)
# если пары имеют одинаковую сумму, то берем пару с наименьшим числом
else:
    min_element = min(o1, e1, o2, e2)
    if min_element in [o1, e1]:
        print(o1, e1)
    else:
        print(o2, e2)

