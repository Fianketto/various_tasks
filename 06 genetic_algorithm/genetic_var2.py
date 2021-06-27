import random

MAX_ENT = 10                    # Особи популяции
ITER_COUNT_NO_CHANGE = 400      # Итерации без изменения целевой функции
K = 10                          # Поставщики
M = 5                           # Товары
MUTATE_P = 0.05                 # Вероятность мутации
s = [random.randint(10, 100) for _ in range(K)]     # Цены на доставки
p = [random.randint(100, 1000) for _ in range(K)]   # Цены на товары
outfile = open("generations_v4_res.txt", 'w')


# Схема пропорционального отбора
def proportional_selection(all_solutions):
    sol_count = len(all_solutions)
    all_prices = [0 for _ in range(sol_count)]
    selected_solutions = []
    avg_price = 0
    for i in range(sol_count):
        all_prices[i] = 1 / get_price(all_solutions[i])
        avg_price += all_prices[i]
    avg_price /= sol_count
    all_coeffs = [all_prices[i] / avg_price for i in range(sol_count)]
    for i in range(sol_count):
        for j in range(int(all_coeffs[i])):
            selected_solutions.append(all_solutions[i])
        prob = all_coeffs[i] - int(all_coeffs[i])
        if random.random() < prob:
            selected_solutions.append(all_solutions[i])
    return selected_solutions


# Генерация первого поколения
def generate_solutions():
    all_solutions = []
    for i in range(MAX_ENT):
        solution = [1]*M + [0]*(K - M)
        random.shuffle(solution)
        all_solutions.append(solution)
    return all_solutions


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


# Целевая функция
def get_price(solution):
    price = 0
    sol_count = len(solution)
    for i in range(sol_count):
        price += solution[i] * p[i] + solution[i] * s[i]
    # Целевую функцию на доставке менее M товаров искуственно завышааем
    if sum(solution) < M:
        price = 10**10
    return price


# Составление пар из особей + потомки
def get_new_solutions(selected_solutions):
    new_solutions = []
    sol_count = len(selected_solutions)
    for i in range(MAX_ENT):
        # Пара для скрещивания
        r1 = random.randint(0, sol_count - 1)
        r2 = random.randint(0, sol_count - 1)
        sol1 = selected_solutions[r1]
        sol2 = selected_solutions[r2]
        # Потомки
        new_sol1, new_sol2 = single_point_cross(sol1, sol2)
        new_solutions += [new_sol1, new_sol2]
    return new_solutions


# Скрещивания двух родителей
def single_point_cross(sol1, sol2):
    j = random.randint(0, K - 1)
    new_sol1 = sol1[:j] + sol2[j:]
    new_sol2 = sol2[:j] + sol1[j:]
    return new_sol1, new_sol2


# Мутации
def mutate(solution):
    r = random.random()
    if r < MUTATE_P:
        a = random.randint(0, len(solution) - 1)
        b = random.randint(0, len(solution) - 1)
        solution[a], solution[b] = solution[b], solution[a]


def print_population_info(population, gen, gen_cnt_wo_change):
    all_costs = [get_price(individual) for individual in population]
    print(f"поколение {gen + 1}, без изм: {gen_cnt_wo_change}", end="\t")
    print(f"{all_costs}\tнаименьшая цена:\t{min(all_costs)}\tлучшая особь:\t{population[0]}\tвсе особи:\t{population}")
    print(f"поколение {gen + 1}, без изм: {gen_cnt_wo_change}", end="\t", file=outfile)
    print(f"{all_costs}\tнаименьшая цена:\t{min(all_costs)}\tлучшая особь:\t{population[0]}\tвсе особи:\t{population}", file=outfile)


iter_no_change = 0                              # Всего итераций без изменения целеыой функции
generation = 0                                  # Поколение
min_price1 = 0                                  # Целевая функция текущего поколения
min_price2 = 0                                  # Целевая функция предыдущего поколения

all_solutions = generate_solutions()               # Генерация исходных решений

while iter_no_change < ITER_COUNT_NO_CHANGE:        # Основной цикл
    all_solutions.sort(key=lambda x: get_price(x))
    print_population_info(all_solutions, generation, iter_no_change)
    # Потенциальные родители
    selected_solutions = proportional_selection(all_solutions)
    # Потомки
    new_solutions = get_new_solutions(selected_solutions)
    for sol in new_solutions:
        mutate(sol)
    # Особи, которые могут перейти в следующее поколение
    selected_new_solutions = proportional_selection(new_solutions)
    # Особи, перешедшие в следующее поколение
    all_solutions_next = []
    for i in range(MAX_ENT):
        r = random.randint(0, len(selected_new_solutions) - 1)
        all_solutions_next.append(selected_new_solutions[r][:])
    all_solutions = all_solutions_next[:]

    # Изменение целевой функции
    all_solutions.sort(key=lambda x: get_price(x))
    min_price1 = get_price(all_solutions[0])
    if min_price1 == min_price2:
        iter_no_change += 1
    else:
        min_price2 = min_price1
        iter_no_change = 0
    generation += 1


# Вывод результатов
print("\nцены и особи в последнем поколении:")
for ind in all_solutions:
    print(get_price(ind), ind)

print("\nнаименьшая цена и лучшая особь в последнем поколении:")
all_solutions.sort(key=lambda x: get_price(x))
best_ind = all_solutions[0]
lowest_price = get_price(best_ind)
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
