# Задача 26

# Читаем файл
with open("26.txt") as fin:
    content = fin.readlines()

# Записываем прочитанные данные в массив
n, k, m = list(map(int, content[0].split()))
prices = list(map(int, content[1:]))

# Сортируем цены
prices.sort()

# Определяем бюджетные и премиум телефоны
budget_prices = prices[:k]
premium_prices = prices[-m:]

# Находим ответ
lowest_premium = premium_prices[0]
avg_budget = int(sum(budget_prices) / len(budget_prices))

print(lowest_premium)
print(avg_budget)
