import requests
import json
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as npy
from PIL import Image


# 1. Вспомогательная функция, которая по ключу будет собирать количество различных значений этого ключа
#       и возвращать отсортированный список списков (вложенный список состоит из двух элементов -
#       значение и кол-во повторений этого значения).
#       Пример: для списка
#          [{"my_key": value_a},
#           {"my_key": value_b},
#           {"my_key": value_a},
#           {"my_key": value_a},
#           {"another_key": value_a}
#          ] и ключа "my_key" эта функция вернет список [[value_a, 3], [value_b, 1]],
#          т.к. по ключу "my_key" 3 раза встречается "value_a" и 1 раз "value_b"
def get_sorted_list(keyword, input_list, deep=True):
    temp_dict = {}
    for element in input_list:
        if deep:                                        # если deep == True, то значение само является списком
            for e in element[keyword]:                  # -- для каждого значения внутри этого списка
                temp_dict[e] = temp_dict.get(e, 0) + 1  # -- увеличиваем счетчик на единицу
        else:                                           # иначе
            e = element[keyword]                        # -- для этого значения
            temp_dict[e] = temp_dict.get(e, 0) + 1      # -- увеличиваем счетчик на единицу

    temp_list = []
    for k, v in temp_dict.items():                      # преобразуем словарь в список, чтобы отсортировать
        temp_list.append([k, v])

    sorted_list = sorted(temp_list, key=lambda x: x[1], reverse=True)   # сортируем
    return sorted_list


# 2. Параметры
MIN_PAGE = 10                           # первая страница для загрузки
MAX_PAGE = 15                           # последняя страница для загрузки
ROW_COUNT = 1000                        # кол-во статей на одной странице
COUNTRY = "United States"               # страна
PRODUCT_TYPE = "Journal Article"        # тип статьи
YEAR = 2020                             # год
RESEARCH_COUNT = 2000                   # требуемое кол-во статей
TOP_SPONSOR_COUNT = 5                   # кол-во топ-спонсоров
TOP_SUBJECT_COUNT = 5                   # кол-во топ-тематик
MASK_IMAGE = "mask01.png"               # файл с маской для облака тегов
OUTPUT_IMAGE = "word_cloud.png"         # файл для сохранения облака тегов

url_root = "https://www.osti.gov/api/v1/"       # корневая ссылка
headers = {"Accept": "application/json"}        # заголовки запроса
filename = "osti_gov_data.json"                 # файл для сохранения загруженных данных
filename_2000 = "osti_gov_data_2000.json"       # файл для сохранения данных только Journal Article / USA (2000 шт)


# 3. Функция для загрузки данных
def get_data():
    all_responses = []                                                  # общий список данных
    for page_num in range(MIN_PAGE, MAX_PAGE + 1):                      # цикл по страницам
        url = url_root + f"records?page={page_num}&rows={ROW_COUNT}"    # url страницы
        resp = requests.get(url).json()                                 # загружаем страницу
        all_responses.extend(resp)                                      # добавляем загруженный данные в общий список
        print(f"got {page_num}")
    return all_responses


# 4. Функция для сохранения данных в файл
def save_data(all_responses, filename):
    with open(filename, 'w') as fout:                                   # открываем файл
        json.dump(all_responses, fout)                                  # записываем в файл


# 5. Функция для чтения данных из файла
def load_data(filename):
    with open(filename) as fin:                                         # открываем файл
        all_researches = json.load(fin)                                 # читаем из файла
    return all_researches


# 6. Загрузка с сайта, сохранение в файл, чтение из файла
#    (данные уже загружены в файл, поэтому загрузку и сохранение закомментировали)
#all_responses = get_data()
#save_data(all_responses, filename)
all_researches = load_data(filename)

# 7. Отбираем только статьи Journal Article, опубликованные в США (2000 шт)
usa_researches = []
usa_researches_2020 = []
for research in all_researches:
    if COUNTRY == research["country_publication"] and PRODUCT_TYPE == research["product_type"]:
        usa_researches.append(research)              # добавляем статью в список, если это Journal Article / USA
        if research["entry_date"][:4] == str(YEAR):
            usa_researches_2020.append(research)     # добавляем статью в список, если это Journal Article / USA / 2020
    if len(usa_researches) == RESEARCH_COUNT:        # если набрали уже 2000 статей, выходим из цикла
        break
#save_data(usa_researches, filename_2000)

# 8. Топ самых частых спонсоров
list_of_sponsors = get_sorted_list("sponsor_orgs", usa_researches)      # получаем отсортированный список спонсоров
print(f"\nТоп-{TOP_SPONSOR_COUNT} самых частых спонсоров:")
for sponsor, cnt in list_of_sponsors[:TOP_SPONSOR_COUNT]:
    print(f"{sponsor} \t-\t {cnt}")                         # печатаем топ-5 спонсоров и сколько раз они спонсировали

# 9. Облако тегов
words_dict = {}
words_list = []
subjects_list = get_sorted_list("subjects", usa_researches_2020)        # получаем отсортированный список тематик
top_subjects = [subj for subj in subjects_list[:TOP_SUBJECT_COUNT]]     # оставляем топ-5 тематик
for subj in top_subjects:                                               # для каждой тематики:
    subj[0] = ''.join([i for i in subj[0] if not i.isdigit()])          # -- удаляем цифры
    subj[0] = re.sub(r"[^\w\s]", "", subj[0]).upper()                   # -- удаляем знаки препинания
    words = subj[0].split()                                             # -- разбиваем по пробелам (оставляем отдельные слова)
    for w in words:                                                     # -- и для каждого полученного слова:
        words_dict[w] = words_dict.get(w, 0) + subj[1]                  # -- -- увеличиваем счетчик на кол-во повторений этой тематики

for k, v in words_dict.items():                                         # преобразуем словарь в список
    words_list.append((k, v))
words_list.sort(key=lambda x: x[1], reverse=True)                       # сортируем
print(f"\n\nСамые частые слова:\n{words_list}")                         # выводим топ-слов

data_set = [w[0] for w in words_list]                                   # преобразуем в список
input_string = " ".join(data_set)                                       # далее преобразуем в строку (для облака тегов)
mask_array = npy.array(Image.open(MASK_IMAGE))                          # читаем маску (форма облака)
cloud = WordCloud(background_color="white", mask=mask_array, stopwords=set(STOPWORDS))  # настройка облака тегов
cloud.generate(input_string)                                            # формируем облако тегов
cloud.to_file(OUTPUT_IMAGE)                                             # сохраняем в файл

# 10. Распределение статей по годам
#       10.1 Для начала добавим во все статьи год в качестве новой пары ключ-значение
for research in usa_researches:
    research["year_entry"] = int(research["entry_date"][:4])

#       10.2 Теперь посчитаем кол-во статей для каждого года
list_of_years = get_sorted_list("year_entry", usa_researches, False)
print("\n\nКол-во статей по годам:")
for y, cnt in list_of_years:
    print(f"{y} \t-\t {cnt}")

list_of_years.sort(key=lambda x: x[0])

#       10.3 Рисуем диаграмму
keys = [str(y[0]) for y in list_of_years]
values = [y[1] for y in list_of_years]
plt.bar(keys, values)
plt.title("Research count by year (Journal Article, USA)")
plt.xlabel("Year")
plt.ylabel("Research count")
plt.show()

