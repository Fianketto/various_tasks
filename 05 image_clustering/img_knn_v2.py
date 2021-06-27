from random import randint
from PIL import Image, ImageDraw


filename = 'groups.png'        # Имя файла
k = 5                       # Количество кластеров
max_iter_count = 50         # Максимльное кол-во итераций


# Функция, возвращающая id ближайшего кластера для заданного цвета (заданного пикселя)
def get_nearest_cluster_id(r, g, b, cluster_centers_colors):
    cluster_count = len(cluster_centers_colors)     # кол-во кластеров
    current_min_distance = float('inf')             # текущее минимальное расстояние
    closest_id = 0                                  # id текущего ближайшего кластера
    for i in range(cluster_count):          # считаем расстояние до каждого кластера
        r0 = cluster_centers_colors[i][0]       # красная составляющая центра кластера
        g0 = cluster_centers_colors[i][1]       # зелена составляющая центра кластера
        b0 = cluster_centers_colors[i][2]       # синяя составляющая центра кластера
        dist = 30 * (r - r0) ** 2 + 59 * (g - g0) ** 2 + 11 * (b - b0) ** 2     # расстояние до центра кластера
        if dist < current_min_distance:     # если до этого кластера расстояние меньше, то обновляем минимум
            current_min_distance = dist
            closest_id = i
    return closest_id


image = Image.open(filename)            # Загружаем изображение
width = image.size[0]                   # Ширина изображения
height = image.size[1]                  # Высота изображения
pix = image.load()                      # Все пиксели изображения

# То же самое. Эти переменные нужны, чтобы не перезаписывать исходные данные при осхранении результатов каждого шага
image2 = Image.open(filename)
draw = ImageDraw.Draw(image2)
pix2 = image2.load()


# Случайно выбираем k пикселей (точнее цвета k случайных пикселей) в качестве исходных центров кластеров
random_points = [(randint(0, width - 1), randint(0, height - 1)) for i in range(k)]     # координаты пикселей
cluster_centers_colors = [[] for i in range(k)]         # цвета центров
cluster_centers_colors_prev = [[] for i in range(k)]    # копия цветов центров (чтобы сравнивать на каждом шаге)

cluster_points = [[] for i in range(k)]                 # пиксели, принадлежащие кластерам

# Записываем цвета центров для каждого кластера
for i in range(k):
    x = random_points[i][0]
    y = random_points[i][1]
    r = pix[x, y][0]  # Красный цвет пикселя
    g = pix[x, y][1]  # Зеленый
    b = pix[x, y][2]  # Синий
    cluster_centers_colors[i] = [r, g, b]
    cluster_centers_colors_prev[i] = [r, g, b]
print(f"0 iter: {cluster_centers_colors}")


# Итерации по измнению центров кластеров
for m in range(max_iter_count):
    # находим ближайший кластер для каждого пикселя
    cluster_points = [[] for i in range(k)]
    for x in range(width):
        for y in range(height):
            r = pix[x, y][0]  # Красный цвет пикселя
            g = pix[x, y][1]  # Зеленый
            b = pix[x, y][2]  # Синий
            # id ближайшего кластера
            closest_cluster_id = get_nearest_cluster_id(r, g, b, cluster_centers_colors)
            # к этому кластеру добавляем текущий пиксель
            cluster_points[closest_cluster_id].append((x, y))

    # находим усредненный цвет для каждого кластера
    for i in range(k):
        r_avg = g_avg = b_avg = 0
        for point in cluster_points[i]:
            x = point[0]
            y = point[1]
            r = pix[x, y][0]  # Красный цвет пикселя
            g = pix[x, y][1]  # Зеленый
            b = pix[x, y][2]  # Синий
            r_avg += r
            g_avg += g
            b_avg += b
        point_count = max(1, len(cluster_points[i]))    # чтобы не было деления на 0
        # средние значения цветов
        r_avg = int(r_avg / point_count)
        g_avg = int(g_avg / point_count)
        b_avg = int(b_avg / point_count)
        # сохраняем старые значения цвеов для кластера
        r_prev, g_prev, b_prev = cluster_centers_colors[i]
        cluster_centers_colors_prev[i] = [r_prev, g_prev, b_prev]
        # записываем новые значения цветов для кластера
        cluster_centers_colors[i] = [r_avg, g_avg, b_avg]

    print(f"{m + 1} iter: {cluster_centers_colors}")

    # все пиксели каждого кластера делаем такого же цвета, что и цвет центра этого кластера
    for i in range(k):
        r, g, b = cluster_centers_colors[i]
        for point in cluster_points[i]:
            x = point[0]
            y = point[1]
            draw.point((x, y), (r, g, b))

    # сохраняем изображение на данном шаге
    image2.save(f'result_{m + 1}.png')

    # проверяем изменение кластеров
    change_exists = False
    for i in range(k):
        r_prev, g_prev, b_prev = cluster_centers_colors_prev[i]
        r, g, b = cluster_centers_colors[i]
        # если хотя бы в одном кластере цвет поменялся, то изменение присутствует
        if r != r_prev or g != g_prev or b != b_prev:
            change_exists = True
            break

    # если же изменения нет, то досрочно завершаем цикл
    if not change_exists:
        break
