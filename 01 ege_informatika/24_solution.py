# Задача 24
# открываем файл
with open("24.txt") as input_file:
    # читаем первую (единственную) строку
    content = input_file.readlines()[0]

# разбиваем строку по разделительным символам Y или Z, чтобы оставить только подряд идущие символы X
array_of_strings = re.split('[YZ]', content)

# Для каждой полученной строки считаем длину
array_of_lengths = []
for s in array_of_strings:
    array_of_lengths.append(len(s))

# То же самое можно сделать быстрее:
# array_of_lengths = list(map(len, array_of_strings))

# Берем максимальное значение длины - это и есть ответ
max_length = max(array_of_lengths)
print(max_length)