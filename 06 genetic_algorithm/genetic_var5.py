import random


MAX_ENT = 10                    # Количество особей в популяции
MAX_GEN_CNT_WO_CHANGE = 500     # Количество поколений без изменения целевой функции для остановки алгоритма
K = 10                          # Количество поставщиков
M = 5                           # Количество товара
MUT_PROB = 0.1                  # Вероятность мутации

p = [random.randint(100, 1000) for i in range(K)]   # Цены товаров
s = [random.randint(10, 100) for i in range(K)]     # Цены доставок
outfile = open("generations_v2_res.txt", 'w')


# Функция для селекции схемой пропорционального отбора
def select(population):
    all_costs = [0 for i in range(len(population))]
    coefficients = [0 for i in range(len(population))]
    selected_individuals = []
    for i in range(len(population)):
        cost = cost_of(population[i])
        all_costs[i] = 1 / cost
    avg_cost = sum(all_costs) / len(all_costs)
    for i in range(len(population)):
        coefficients[i] = all_costs[i] / avg_cost
    for i in range(len(population)):
        for j in range(int(coefficients[i])):
            selected_individuals.append(population[i])
        if random.random() < coefficients[i] - int(coefficients[i]):
            selected_individuals.append(population[i])
    return selected_individuals


# Функция для случайного соатвления первого поколения
def get_first_population():
    first_population = [[] for i in range(MAX_ENT)]
    for i in range(MAX_ENT):
        individual = [1 for k in range(M)] + [0 for k in range(K - M)]
        random.shuffle(individual)
        first_population[i] = individual
    return first_population


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


# Целевая функция (полная стоимость)
def cost_of(individual):
    cost = 0
    if sum(individual) >= M:
        for i in range(len(individual)):
            cost += individual[i] * p[i] + individual[i] * s[i]
    else:
        # Доставку менее M товаров не рассматриваем
        cost = float('inf')
    return cost


# Составление пар из отобранных особей и получение детей
def make_children(selected_individuals):
    children = []
    for i in range(MAX_ENT):
        # Пара для скрещивания
        ind_cnt = len(selected_individuals)
        r1, r2 = random.randint(0, ind_cnt - 1), random.randint(0, ind_cnt - 1)
        parent1, parent2 = selected_individuals[r1], selected_individuals[r2]
        # Получение ребенка
        child1, child2 = cross_parents(parent1, parent2)
        # Мутации
        apply_mut(child1)
        apply_mut(child2)
        children.extend([child1, child2])
    return children


# Скрещивания двух родителей
def cross_parents(parent1, parent2):
    c = random.randint(0, K - 1)
    child1 = parent1[:c] + parent2[c:]
    child2 = parent2[:c] + parent1[c:]
    return child1, child2


# Мутации
def apply_mut(child):
    if random.random() < MUT_PROB:
        g = random.randint(0, len(child) - 1)
        child[g] = 1 - child[g]


def print_population_info(population, gen, gen_cnt_wo_change):
    all_costs = [cost_of(individual) for individual in population]
    print(f"поколение {gen + 1}, без изм: {gen_cnt_wo_change}", end="\t")
    print(f"{all_costs}\tнаименьшая цена:\t{min(all_costs)}\tлучшая особь:\t{population[0]}\tвсе особи:\t{population}")
    print(f"поколение {gen + 1}, без изм: {gen_cnt_wo_change}", end="\t", file=outfile)
    print(f"{all_costs}\tнаименьшая цена:\t{min(all_costs)}\tлучшая особь:\t{population[0]}\tвсе особи:\t{population}", file=outfile)


population = get_first_population()         # Первое поколение
gen_cnt_wo_change = 0                       # Поколений без изменения целевой функции
gen = 0                                     # Номер поколения
min_cost = min_cost_prev = 0                # Минимальное значение целевой функции на ткущем и на предыдущем поколениях
while gen_cnt_wo_change < MAX_GEN_CNT_WO_CHANGE:    # Цикл с изменением поколений
    population.sort(key=lambda x: cost_of(x))
    print_population_info(population, gen, gen_cnt_wo_change)
    # Особи, которые могут стать родителями
    selected_individuals = select(population)
    children = make_children(selected_individuals)

    # Особи, которые могут перейти в следующее поколение
    selected_children = select(children)

    # Особи, перешедшие в следующее поколение
    next_population = [None for _ in range(MAX_ENT)]
    for i in range(MAX_ENT):
        r = random.randint(0, len(selected_children) - 1)
        next_population[i] = selected_children[r][:]

    population = next_population[:]

    # Проверяем изменение целевой функции
    population.sort(key=lambda x: cost_of(x))
    min_cost = cost_of(population[0])
    if min_cost == min_cost_prev:
        gen_cnt_wo_change += 1
    else:
        min_cost_prev = min_cost
        gen_cnt_wo_change = 0
    gen += 1


# Вывод результатов
print("\nцены и особи в последнем поколении:")
for ind in population:
    print(cost_of(ind), ind)

print("\nнаименьшая цена и лучшая особь в последнем поколении:")
population.sort(key=lambda x: cost_of(x))
best_ind = population[0]
lowest_price = cost_of(best_ind)
print(lowest_price, best_ind)

print("\nтеоретическая наименьшая цена и теоретическое решение:")
expected_lowest_price, expected_solution = get_best_solution(p, s)
print(expected_lowest_price, expected_solution)

print("\nстоимости товаров и доставок:")
print(p)
print(s)

