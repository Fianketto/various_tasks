import random


MAX_ENT = 100               # Кол-во особей в популяции
GEN_COUNT = 500             # Кол-во поколений
K = 10                      # Кол-во городов
T = 0.5                     # Коэффициент для отбора усечением
P_MUTATE = 0.1              # Вероятность возникновения мутации
P_MUTATE_CONTINUE = 0.5     # Вероятость продолжения мутации

matrix = [
    [0, 5, 1, 7, 5, 9, 1, 9, 2, 9],
    [5, 0, 3, 5, 7, 3, 2, 1, 5, 7],
    [1, 3, 0, 7, 5, 7, 4, 1, 2, 6],
    [7, 5, 7, 0, 5, 1, 2, 4, 3, 9],
    [5, 7, 5, 5, 0, 8, 2, 2, 1, 8],
    [9, 3, 7, 1, 8, 0, 2, 6, 8, 3],
    [1, 2, 4, 2, 2, 2, 0, 4, 2, 1],
    [9, 1, 1, 4, 2, 6, 4, 0, 4, 2],
    [2, 5, 2, 3, 1, 8, 2, 4, 0, 8],
    [9, 7, 6, 9, 8, 3, 1, 2, 8, 0]
]

population = [[0 for _ in range(K)] for i in range(MAX_ENT)]    # Текущая популяция
best_individual_of_all = None
least_distance_of_all = float('inf')
gen_num_with_best_ind = 0


def initialize_population():
    pop = [[] for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        individual = [j for j in range(K)]
        random.shuffle(individual)
        pop[i] = individual
    return pop


# Целевая функция - общее пройденное расстояние
def get_distance(individual):
    dist = 0
    for i in range(K):
        from_city = individual[i]
        to_city = individual[(i + 1) % K]
        dist += matrix[from_city][to_city]
    return dist


# Функция для скрещивания двух родителей
def cross(parent1, parent2):
    child1 = [-1 for _ in range(K)]
    child2 = [-1 for _ in range(K)]
    child1 = _cross(parent1, parent2, child1)
    child2 = _cross(parent2, parent1, child2)

    return child1, child2


def _cross(parent1, parent2, child):
    c_left, c_right = 0, K - 1
    p1_left, p2_right = 0, K - 1
    cities_used = 0

    while cities_used < K:
        p1_used = False
        while not p1_used:
            if parent1[p1_left] not in child:
                child[c_left] = parent1[p1_left]
                c_left += 1
                p1_used = True
            p1_left += 1
        cities_used += 1

        p2_used = False
        while not p2_used:
            if parent2[p2_right] not in child:
                child[c_right] = parent2[p2_right]
                c_right -= 1
                p2_used = True
            p2_right -= 1
        cities_used += 1

    return child


# Функция для вызова мутаций (перестановка городов)
def mutate(child):
    r = random.random()
    r2 = 0
    if r < P_MUTATE:
        while r2 < P_MUTATE_CONTINUE:
            c1 = random.randint(0, len(child) - 1)
            c2 = random.randint(0, len(child) - 1)
            child[c1], child[c2] = child[c2], child[c1]     # Меняем города местами
            r2 = random.random()


def show_pop(pop, caption):
    sorted_pop = sorted(pop, key=lambda x: get_distance(x))
    arr = [get_distance(ind) for ind in pop]
    print(f"{caption}, расстояния особей:\t{arr}\tнаименьшее расстояние:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}")
    #print(f"{caption}\t{arr}\tнаименьшая цена:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}", file=outfile)


population = initialize_population()    # Инициализация популяции
# Цикл по поколениям
for gen in range(GEN_COUNT):
    # 1. Отбираем особей для становления потенциальными родителями
    show_pop(population, f"поколение {gen + 1}")
    population.sort(key=lambda x: get_distance(x))
    if get_distance(population[0]) < least_distance_of_all:
        best_individual_of_all = population[0]
        least_distance_of_all = get_distance(population[0])
        gen_num_with_best_ind = gen

    cnt = int(T * len(population))
    population_for_cross = population[:cnt]     # В этом списке сохранили особей, из которых будем отбирать родителей

    children = []
    for _ in range(MAX_ENT * 10):
        # 2. Отбираем родителей для скрещивания
        r1 = random.randint(0, len(population_for_cross) - 1)
        r2 = random.randint(0, len(population_for_cross) - 1)
        parent1 = population_for_cross[r1]
        parent2 = population_for_cross[r2]
        # 3. Скрещиваем родителей
        child1, child2 = cross(parent1, parent2)
        mutate(child1)
        mutate(child2)
        children.append(child1)
        children.append(child2)

    # 4. Отбираем особей для селекции
    population_for_selection = population[:] + children[:]
    population_for_selection.sort(key=lambda x: get_distance(x))
    cnt = max(int(T * len(population_for_selection)), MAX_ENT)
    population_for_selection = population_for_selection[:cnt]

    # 5. Отбираем особей для следующего поколения
    next_population = [None for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        r = random.randint(0, len(population_for_selection) - 1)
        next_population[i] = population_for_selection[r][:]

    population = next_population[:]



    #input("Нажмите для следующего поколения")


# Вывод результатов
print("\nрасстояния и особи в последнем поколении:")
for ind in population:
    print(get_distance(ind), ind)

print("\nнаименьшее расстояние и лучшая особь в последнем поколении:")
population.sort(key=lambda x: get_distance(x))
best_ind = population[0]
least_dist = get_distance(best_ind)
print(least_dist, best_ind)

print("\nнаименьшее расстояние и лучшая особь за все поколения:")
print(least_distance_of_all, best_individual_of_all, "поколение ", gen_num_with_best_ind)

