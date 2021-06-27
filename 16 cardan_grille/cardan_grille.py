import random


k = 4                                               # Сторона квадрата, из которого формируем решетку
max_len = 4 * k**2                                  # Количество клеток в решетке
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"      # Алфавит
ALPHABET_LEN = len(ALPHABET)                        # Длина алфавита


# Функция для получения координат y,x (i,j) клетки с номером n в квадрате square_num относительно этого квадрата
def get_relative_coordinates(n, square_num):
    y = n // k
    x = n % k
    if square_num == 1:
        y, x = k - 1 - x, y
    elif square_num == 2:
        y, x = k - 1 - y, k - 1 - x
    elif square_num == 3:
        y, x = x, k - 1 - y
    return x, y


# Функция для получения координат y,x (i,j) клетки с номером n в квадрате square_num относительно всей решетки
def get_absolute_coordinates(n, square_num):
    x, y = get_relative_coordinates(n, square_num)
    if square_num == 1:
        x += k
    elif square_num == 2:
        x += k
        y += k
    elif square_num == 3:
        y += k
    return x, y


# Функция для инициализации четырех квадратов (A, B, C, D):
# записывем номера клеток в каждый из квадратов в нужном порядке
def initialize_grids():
    A = [[j + i * k for j in range(k)] for i in range(k)]
    B = [[None for j in range(k)] for i in range(k)]
    C = [[None for j in range(k)] for i in range(k)]
    D = [[None for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            B[i][j] = A[k - 1 - j][i]
            C[i][j] = A[k - 1 - i][k - 1 - j]
            D[i][j] = A[j][k - 1 - i]
    return A, B, C, D


# Функция для разбивки сообщения на буквы
def initialize_message(my_text):
    message = []
    for c in my_text.upper():
        if c in ALPHABET:
            message.append(c)
    print(f"\nИсходное сообщение:\n{my_text}")
    print(f"\nВ сообщении оставляем только буквы:\n{message}")
    return message


# Функция для генерации ключа - последовательности номеров квадратов (0-A, 1-B, 2-C, 3-D)
def generate_key():
    key_string = [random.randint(0, 3) for i in range(k ** 2)]
    print(f"\nГенерируем ключ для шифровки:\n{''.join(map(str, key_string))}")
    return key_string


# Функция для разделения сообщения на 4 части
def split_message(message):
    message_parts = [[] for i in range(4)]
    print("\nРазбиваем сообщение на 4 части:")
    for i in range(4):
        message_parts[i] = message[i * k ** 2: (i + 1) * k ** 2]
        part_len = len(message_parts[i])
        if part_len < k ** 2:
            random_letters = [ALPHABET[random.randint(0, ALPHABET_LEN - 1)] for j in range(k ** 2 - part_len)]
            message_parts[i] += random_letters
        print(message_parts[i])
    if len(message) > max_len:
        print("Внимание, сообщение слишком длинное и будет зашифровано не полностью")
    elif len(message) < max_len:
        print("Внимание, в конец сообщения добавлены случайные буквы")
    return message_parts


# Функция для шифровки сообщения
def encrypt_message(message_parts):
    print("\nЗашифровываем сообщение:")
    encrypted_message_letters = [[None for j in range(2 * k)] for i in range(2 * k)]
    encrypted_message = ["" for i in range(2 * k)]
    i = 0
    for m in range(4):                              # Цикл для каждого из 4х частей сообщения
        for n in range(k ** 2):                     # Цикл по всем буквам части сообщения
            c = message_parts[m][n]
            square_num = (key_string[n] + m) % 4    # Здесь происходит поворот решетки (номера квадратов в ключе циклично изменяем)
            x, y = get_absolute_coordinates(n, square_num)
            encrypted_message_letters[y][x] = c     # В нужную клетку записываем текущую букву
            i += 1
    for i, row in enumerate(encrypted_message_letters):     # Преобразуем массив букв в массив строк для удобства
        encrypted_message[i] = "".join(row)
        print(encrypted_message[i])
    print("-------- г о т о в о !  с о о б щ е н и е  з а ш и ф р о в а н о ! --------")
    return encrypted_message


# Функция для расшифровки сообщения по ключу
def decrypt_message(encrypted_message, key_string):
    print("\nНачинаем расшифровывать сообщение")
    for row in encrypted_message:
        print(row)
    print(f"Ипользуем ключ {key_string}")
    decrypted_message = ""
    i = 0
    for m in range(4):                              # Цикл для каждого из 4х частей сообщения
        for n in range(k ** 2):                     # Цикл по всем буквам части сообщения
            square_num = (key_string[n] + m) % 4    # Здесь происходит поворот решетки
            x, y = get_absolute_coordinates(n, square_num)
            decrypted_message += encrypted_message[y][x]    # Добавляем в итоговое сообщение букву из нужной клетки
            i += 1
    print(f"\nРасшифрованное сообщение:\n{decrypted_message}")
    print("-------- г о т о в о !  с о о б щ е н и е  р а с ш и ф р о в а н о ! --------")

    return decrypted_message


# НАЧАЛО АЛГОРИТМА
action = int(input("Приветствую! Введите номер действия, которое Вы хотите совершить:\n1 - зашифровать сообщение\n2 - расшифровать сообщение\n"))
if action == 1:
    my_text = input("Введите сообщение для шифровки (на русском)\n").strip()    # Сообщение для шифровки
    A, B, C, D = initialize_grids()                                             # Инициализация квадратов
    key_string = generate_key()                                                 # Генерация ключа

    # 1. Шифровка
    message = initialize_message(my_text)               # Начальные преобразования сообщения
    message_parts = split_message(message)              # Разделение сообщения на 4 части
    encrypted_message = encrypt_message(message_parts)  # Шифровка
elif action == 2:
    # 2. Расшифровка
    '''
Для примера можно ввести ключ:
2203000333010233
и сообщение:
РОБЛКШОЫ
ЛЬШОДРРЮ
ВЕОСМПТЭ
ББИФЬЯЁИ
ДЕЦИЩУЩЙ
ШСЖЕККДР
ЕФБИРЕРИ
НОООЮВЕН
    '''
    PROMPT_MESSAGE1 = f"Введите ключ, состоящий из {k**2} цифр в диапазоне 0-3 (без пробелов)\n"
    PROMPT_MESSAGE2 = f"Введите зашифрованное сообщение ({2*k} строк, по {2*k} букв в каждой строке)\n"
    key_string_new = list(map(int, input(PROMPT_MESSAGE1).strip()))                 # Задаем ключ
    encrypted_message_new = [input(PROMPT_MESSAGE2).strip().upper()]                # Задаем зашифрованное сообщение
    for i in range(2*k - 1):
        encrypted_message_new.append(input().strip().upper())
    decrypted_message = decrypt_message(encrypted_message_new, key_string_new)      # Расшифровка
else:
    print("Введено неверное число")
