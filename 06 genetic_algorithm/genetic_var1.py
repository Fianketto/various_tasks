from random import random, randint, shuffle


MAX_ENT = 10    # Особи в одном поколении
GENERATION_CNT = 500    # Всего поколений
P_MUT = 0.1     # Вероятность мутации
T = 0.75    # Коэффициент отбора усечением


K = 10  # Число поставщиков
M = 5   # Число товаров
# Генерация цен на товары и на доставки
p = [randint(100, 1000) for _ in range(K)]   # Цены товаров
s = [randint(10, 100) for _ in range(K)]     # Цены доставок

outfile = open("generations_v3_res.txt", 'w')


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


# Сумма цен у выбранных поставщиков (целевая функция)
def target_func(individual):
    total_price = 0
    if individual.count(1) < M:
        total_price = float('inf')
    else:
        for i in range(len(individual)):
            seller_price = individual[i] * (p[i] + s[i])
            total_price += seller_price
    return total_price


# Скрещивание двух особей и получение двух потомков
def crossbreeding(p1, p2):
    c1 = [0] * K
    c2 = [0] * K
    for i in range(len(p1)):
        if random() < 0.5:  # Наследование от 1го или 2го родителя
            c1[i], c2[i] = p1[i], p2[i]
        else:
            c1[i], c2[i] = p2[i], p1[i]
    return c1, c2


# Мутация
def mutation(child):
    for g in range(K):
        if random() < P_MUT:
            g = randint(0, K - 1)
            child[g] = 1 - child[g]
    return child


def show_pop(pop, caption):
    sorted_pop = sorted(pop, key=lambda x: target_func(x))
    arr = [target_func(ind) for ind in pop]
    print(f"{caption}\t{arr}\tнаименьшая цена:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}")
    print(f"{caption}\t{arr}\tнаименьшая цена:\t{min(arr)}\tлучшая особь:\t{sorted_pop[0]}\tвсе особи:\t{sorted_pop}", file=outfile)


current_population = []
for i in range(MAX_ENT):
    goods_count = randint(M, M + 2)
    individual = [1] * goods_count + [0] * (K - goods_count)
    shuffle(individual)
    current_population.append(individual)

for generation_num in range(GENERATION_CNT):
    # 1. population_selected1 - потенциальные родители
    show_pop(current_population, f"поколение {generation_num + 1}")
    current_population.sort(key=lambda x: target_func(x))
    selected_ind_count = int(T * MAX_ENT)
    population_selected1 = current_population[:selected_ind_count]

    # 2. children - потомки
    children = []
    for i in range(MAX_ENT):
        temp_pop = population_selected1[:]
        shuffle(temp_pop)
        parent1, parent2 = temp_pop[0], temp_pop[1]
        child1, child2 = crossbreeding(parent1, parent2)
        children += [mutation(child1), mutation(child2)]

    # 3. population_selected2 - особи для селекции
    population_selected2 = population_selected1[:] + children[:]
    population_selected2.sort(key=lambda x: target_func(x))
    selected_ind_count = max(int(T * len(population_selected2)), MAX_ENT)
    population_selected2 = population_selected2[:selected_ind_count]

    # 4. next_population - следующее поколение
    next_population = []
    for i in range(MAX_ENT):
        r = randint(0, len(population_selected2) - 1)
        next_population.append(population_selected2[r][:])

    current_population = next_population[:]


# Вывод результатов
print("\nцены и особи в последнем поколении:")
for ind in current_population:
    print(target_func(ind), ind)

print("\nнаименьшая цена и лучшая особь в последнем поколении:")
current_population.sort(key=lambda x: target_func(x))
best_ind = current_population[0]
lowest_price = target_func(best_ind)
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

