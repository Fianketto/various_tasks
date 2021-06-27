import random


MAX_ENT = 10        # Кол-во особей в популяции
GEN_COUNT = 500     # Кол-во поколений
K = 10              # Кол-во поставщиков
M = 5               # Необходимое кол-во единиц товара (M <= K)
T = 0.6             # Коэффициент для отбора усечением
P_MUTATE = 0.05     # Вероятность мутации

p = [random.randint(100, 1000) for _ in range(K)]   # Стоимость товаров
s = [random.randint(10, 100) for _ in range(K)]     # Стоимость доставок
population = [[0 for _ in range(K)] for i in range(MAX_ENT)]    # Текущая популяция
outfile = open("generations_res.txt", 'w')


def initialize_population():
    pop = [[] for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        individual = [0 for _ in range(K)]
        temp_arr = [j for j in range(K)]
        for m in range(M):
            r = random.randint(0, len(temp_arr) - 1)
            individual[temp_arr[r]] = 1
            del temp_arr[r]
        pop[i] = individual
    return pop


# Теоретическое лучшее решение, чтобы можно было сравнить с результатом ГА
def get_best_solution(p, s):
    full_cost = [p[i] + s[i] for i in range(K)]
    full_cost_sorted = sorted(full_cost)[:M]
    best_solution = [0 for _ in range(K)]
    i = 0
    while sum(best_solution) < M:
        if full_cost[i] in full_cost_sorted:
            best_solution[i] = 1
        i += 1
    lowest_price = sum(full_cost_sorted)
    return lowest_price, best_solution


# Целевая функция - общая стоимость. Ее хотим минимизировать
def get_cost(individual):
    cost = 0
    # Решение поствки менее M товаров считаем неподходящей
    if sum(individual) < M:
        cost = float('inf')
    else:
        for i in range(len(individual)):
            cost += individual[i] * (p[i] + s[i])
    return cost


# Функция для скрещивания двух родителей
def cross(parent1, parent2):
    child1 = [0 for _ in range(K)]
    child2 = [0 for _ in range(K)]
    for i in range(len(parent1)):   # Для каждой хромосомы решаем, из какого родителя брать
        r = random.random()
        if r < 0.5:                 # С вероятностью 50% 1ый ребенок наследует от 1го родителя, 2ой - от 2ого
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        else:                       # С вероятностью 50% - наоборот
            child1[i] = parent2[i]
            child2[i] = parent1[i]
    mutate(child1)                  # Мутации
    mutate(child2)
    return child1, child2


# Функция для вызова мутаций (перестановка битов)
def mutate(child):
    r = random.random()
    if r < P_MUTATE:
        c1 = random.randint(0, len(child) - 1)
        c2 = random.randint(0, len(child) - 1)
        child[c1], child[c2] = child[c2], child[c1]     # Меняем хромосомы местами


def show_pop(pop, caption):
    sorted_pop = sorted(pop, key=lambda x: get_cost(x))
    arr = [get_cost(ind) for ind in pop]
    print(f"{caption}\t{arr}\tнаименьшая цена:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}")
    print(f"{caption}\t{arr}\tнаименьшая цена:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}", file=outfile)


population = initialize_population()    # Инициализация популяции
# Цикл по поколениям
for gen in range(GEN_COUNT):
    # 1. Отбираем особей для становления потенциальными родителями
    show_pop(population, f"поколение {gen + 1}")
    population.sort(key=lambda x: get_cost(x))
    cnt = int(T * len(population))
    population_for_cross = population[:cnt]     # В этом списке сохранили особей, из которых будем отбирать родителей

    children = []
    for _ in range(MAX_ENT):
        # 2. Отбираем родителей для скрещивания
        r1 = random.randint(0, len(population_for_cross) - 1)
        r2 = random.randint(0, len(population_for_cross) - 1)
        parent1 = population_for_cross[r1]
        parent2 = population_for_cross[r2]
        # 3. Скрещиваем родителей
        child1, child2 = cross(parent1, parent2)
        children.append(child1)
        children.append(child2)

    # 4. Отбираем особей для селекции
    population_for_selection = population[:] + children[:]
    population_for_selection.sort(key=lambda x: get_cost(x))
    cnt = max(int(T * len(population_for_selection)), MAX_ENT)
    population_for_selection = population_for_selection[:cnt]

    # 5. Отбираем особей для следующего поколения
    next_population = [None for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        r = random.randint(0, len(population_for_selection) - 1)
        next_population[i] = population_for_selection[r][:]

    population = next_population[:]


# Вывод результатов
print("\nцены и особи в последнем поколении:")
for ind in population:
    print(get_cost(ind), ind)

print("\nнаименьшая цена и лучшая особь в последнем поколении:")
population.sort(key=lambda x: get_cost(x))
best_ind = population[0]
lowest_price = get_cost(best_ind)
print(lowest_price, best_ind)

print("\nтеоретическая наименьшая цена и теоретическое решение:")
expected_lowest_price, expected_solution = get_best_solution(p, s)
print(expected_lowest_price, expected_solution)

print("\nстоимости товаров и доставок:")
print(p)
print(s)

print(lowest_price, best_ind, file=outfile)
print(expected_lowest_price, expected_solution, file=outfile)
print(p, file=outfile)
print(s, file=outfile)
