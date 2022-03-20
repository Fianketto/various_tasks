import random
import datetime
import sqlite3
import pandas as pd


# Переключатели нужны, чтобы повторно не добавлять данные в таблицы
CREATE_TABLES = False
ADD_USERS = False
ADD_TARIFFS = False
ADD_SERVICES = False
ADD_EVENTS = False


def create_conn(db_file_name):
    """Подключение к БД"""
    connection = sqlite3.connect(db_file_name, check_same_thread=False)
    return connection


def create_table(conn, sql_create_table):
    """Добавление новых таблиц"""
    cursor = conn.cursor()
    cursor.execute(sql_create_table)


def create_user(connection, user):
    """Добавление абонента"""
    sql = ''' INSERT INTO Users(current_balance, add_date, age, live_city, last_active_datetime, tariff)
              VALUES(?,?,?,?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()
    return cursor.lastrowid


def create_tariff(connection, tariff):
    """Добавление тарифа"""
    sql = '''   INSERT INTO Tariffs(name, start_date, end_date, minutes_count, sms_count, traffic_count)
                VALUES(?,?,?,?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, tariff)
    connection.commit()
    return cursor.lastrowid


def create_service(connection, service):
    """Добавление типа услуги"""
    sql = ''' INSERT INTO Services(name)
              VALUES(?) '''
    cursor = connection.cursor()
    cursor.execute(sql, service)
    connection.commit()
    return cursor.lastrowid


def create_event(connection, event):
    """Добавление события"""
    sql = '''   INSERT INTO Events(event_datetime, user_id, service_id, volume)
                VALUES(?,?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, event)
    connection.commit()
    return cursor.lastrowid


def select_users_dates(connection, user_id):
    """Выбор даты добавления и даты последнего события для заданного абонента
    Эти данные нужны для того, чтобы далее сгенерировать события только в указанном временном промежутке
    """
    sql_select = """SELECT add_date, last_active_datetime
                    FROM Users
                    WHERE id = ?
                    """
    cursor = connection.cursor()
    cursor.execute(sql_select, (user_id, ))
    rows = cursor.fetchall()
    return rows[0]


def select_all_events(connection):
    """Выбор всех событий"""
    sql_select = """SELECT * FROM Events"""
    cursor = connection.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    return rows


def select_user_ids(connection):
    """Выбор всех ID абонентов"""
    sql_select = """SELECT distinct id FROM Users"""
    cursor = connection.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    return rows


# 0. Добавление БД и подключение к ней
connection = create_conn("megafon.db")

# 1. Добавление таблиц
sql_create_table_users = """CREATE TABLE IF NOT EXISTS Users (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                current_balance real NOT NULL,
                                add_date datetime NOT NULL,
                                age integer NOT NULL,
                                live_city text NOT NULL,
                                last_active_datetime datetime NOT NULL,
                                tariff integer NOT NULL
                            );"""

sql_create_table_tariffs = """CREATE TABLE IF NOT EXISTS Tariffs (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name varchar(80) NOT NULL,
                                start_date date NOT NULL,
                                end_date date NOT NULL,
                                minutes_count integer NOT NULL,
                                sms_count integer NOT NULL,
                                traffic_count integer NOT NULL
                            );"""

sql_create_table_services = """CREATE TABLE IF NOT EXISTS Services (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name varchar(80) NOT NULL
                            );"""

sql_create_table_events = """CREATE TABLE IF NOT EXISTS Events (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                event_datetime datetime NOT NULL,
                                user_id integer NOT NULL,
                                service_id integer NOT NULL,
                                volume integer NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES Users (id) on delete cascade,
                                FOREIGN KEY (service_id) REFERENCES Services (id) on delete cascade
                            );"""

if connection is not None and CREATE_TABLES:
    create_table(connection, sql_create_table_users)
    create_table(connection, sql_create_table_tariffs)
    create_table(connection, sql_create_table_services)
    create_table(connection, sql_create_table_events)


# 2. Заполнение таблиц данными
# Границы для генерации даты добавления абонента
MIN_DATE = datetime.datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp()
MAX_DATE = datetime.datetime.strptime('2022-03-18 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp()
# Кол-во тарифов
TARIFF_COUNT = 3
# Кол-во абонентов
USER_COUNT = 100
# Границы для генерации возраста абонента
MIN_AGE = 18
MAX_AGE = 70
# Список городов для случайного выбора
CITIES = ['Москва', 'Волгоград', 'Санкт-Петербург', 'Сочи', 'Хабаровск', 'Екатеринбург', 'Новосибирск']


if connection is not None:
    # Добавление абонентов
    if ADD_USERS:
        for i in range(USER_COUNT):
            # Генерируем случайные данные
            cur_balance = round(random.random() * 1000, 2)
            start_date = datetime.datetime.fromtimestamp(random.randint(MIN_DATE, MAX_DATE))
            age = random.randint(MIN_AGE, MAX_AGE)
            city = random.choice(CITIES)
            last_active_datetime = datetime.datetime.fromtimestamp(random.randint(start_date.timestamp(), MAX_DATE))
            tariff = random.randint(1, TARIFF_COUNT)
            user = (cur_balance, start_date, age, city, last_active_datetime, tariff)
            # И добавляем в таблицу
            create_user(connection, user)

    # Добавление тарифов
    if ADD_TARIFFS:
        tariff_01 = ('Безлимитный', '2020-01-01 00:00:00', '2030-12-31 23:59:59', 700, 250, 51200)
        tariff_02 = ('Стандартный', '2018-01-01 00:00:00', '2030-12-31 23:59:59', 250, 100, 10240)
        tariff_03 = ('Минимальный', '2016-01-01 00:00:00', '2021-12-31 23:59:59', 50, 50, 2048)
        for tariff in [tariff_01, tariff_02, tariff_03]:
            create_tariff(connection, tariff)

    # Добавление типов услуг
    if ADD_SERVICES:
        service_01 = ('Звонок', )
        service_02 = ('СМС', )
        service_03 = ('Трафик', )
        for service in [service_01, service_02, service_03]:
            create_service(connection, service)

    # Добавление событий
    if ADD_EVENTS:
        all_events = []
        # Для каждого абонента
        for i in range(USER_COUNT):
            user_id = i + 1
            # Сначала получаем дату добавления абонента и дату последнего события
            dates = select_users_dates(connection, user_id)
            add_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d %H:%M:%S').timestamp()
            last_active_datetime = datetime.datetime.strptime(dates[1], '%Y-%m-%d %H:%M:%S').timestamp()

            # Количество событий определенных типов
            event_01_count = random.randint(50, 100)
            event_02_count = random.randint(5, 10)
            event_03_count = random.randint(500, 1000)

            # Генерация звонков
            service_id = 1
            for j in range(event_01_count):
                event_datetime = random.randint(add_date, last_active_datetime)
                volume = random.randint(1, 20)
                event = (event_datetime, user_id, service_id, volume)
                all_events.append(event)

            # Генерация смс
            service_id = 2
            for j in range(event_02_count):
                event_datetime = random.randint(add_date, last_active_datetime)
                volume = random.randint(1, 3)
                event = (event_datetime, user_id, service_id, volume)
                all_events.append(event)

            # Генерация трафика
            service_id = 3
            for j in range(event_03_count):
                event_datetime = random.randint(add_date, last_active_datetime)
                volume = random.randint(1, 40)
                event = (event_datetime, user_id, service_id, volume)
                all_events.append(event)

            # Еще одно событие, кдата которого будет совпадать с датой последней активности
            last_event = (last_active_datetime, user_id, 1, random.randint(1, 20))
            all_events.append(last_event)

        # Сортируем по дате события
        all_events.sort(key=lambda x: x[0])
        # Преобразуем timestamp в строку даты-времени
        all_events = list(map(lambda x: (datetime.datetime.fromtimestamp(x[0]), x[1], x[2], x[3]), all_events))
        # Добавляем события в таблицу
        for event in all_events:
            create_event(connection, event)


# 3. Чтение и группировка
# Читаем все события
all_events = select_all_events(connection)
# Преобразуем в DataFrame
df = pd.DataFrame(all_events)
# Переименовываем столбцы
df.rename(columns={0: 'event_id',
                   1: 'event_datetime',
                   2: 'user_id',
                   3: 'service_id',
                   4: 'volume'
                   }, inplace=True)
# Добавляем дату без времени
df['day'] = df['event_datetime'].str[:10]
# Добавляем новые столбцы для удобства группировки
df['serv_01_vol'] = df.volume * df.service_id.apply(lambda x: 1 if x == 1 else 0)
df['serv_02_vol'] = df.volume * df.service_id.apply(lambda x: 1 if x == 2 else 0)
df['serv_03_vol'] = df.volume * df.service_id.apply(lambda x: 1 if x == 3 else 0)

# Группируем
df_gr = df.groupby(['user_id', 'day'], as_index=False).agg({'serv_01_vol': 'sum', 'serv_02_vol': 'sum', 'serv_03_vol': 'sum'})
#print(df_gr)

