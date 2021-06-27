import sqlite3


CREATE_TABLE = True
ADD_DATA_1 = True
ADD_DATA_2 = True
CHANGE_NAME = True
DELETE_PERSON = True

SELECT_DATA_1 = True
SELECT_DATA_2 = True
SELECT_DATA_3 = True


def create_conn(db_file_name):
    connection = sqlite3.connect(db_file_name)
    return connection


def create_table(conn, sql_create_table):
    cursor = conn.cursor()
    cursor.execute(sql_create_table)


def create_person(connection, person):
    sql = ''' INSERT INTO Person(name, gender, age, registered)
              VALUES(?,?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, person)
    connection.commit()
    return cursor.lastrowid


def create_company(connection, company):
    sql = ''' INSERT INTO Company(name) VALUES(?) '''
    cursor = connection.cursor()
    cursor.execute(sql, company)
    connection.commit()
    return cursor.lastrowid


def create_linkpc(connection, linkpc):
    sql = ''' INSERT INTO LinkPC(person_id, company_id, salary)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, linkpc)
    connection.commit()
    return cursor.lastrowid


def update_person_name(connection, person):
    sql = ''' UPDATE Person
              SET name = ?
              WHERE id = ?'''
    cursor = connection.cursor()
    cursor.execute(sql, person)
    connection.commit()


def delete_person(connection, person_id):
    sql = 'DELETE FROM Person WHERE id=?'
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute(sql, person_id)
    connection.commit()


def select_data_1(connection):
    sql_select = """SELECT p.name, p.age, link.salary
                    FROM Person p LEFT JOIN LinkPC link
                    ON p.id = link.Person_id
                    WHERE p.gender = 'female'
                    """
    cursor = connection.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()

    print("\nВсе женщины с их зарплатой:")
    for row in rows:
        print(row[0], row[2])


def select_data_2(connection):
    sql_select = """SELECT gender, count(*)
                    FROM Person
                    GROUP BY gender
                    ORDER BY gender DESC
                    """
    cursor = connection.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()

    print("\nКоличество мужчин и женщин в БД:")
    for row in rows:
        print(row[0], row[1])


def select_data_3(connection):
    sql_select = """SELECT c.name as company_name
                    FROM LinkPC link LEFT JOIN Company c
                    ON c.id = link.Company_id
                    GROUP BY c.name
                    HAVING count(*) > 3
                    """
    cursor = connection.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()

    print("\nКомпании, в которых работало более 3 сотрудников:")
    for row in rows:
        print(row[0])
    if not rows:
        print("--- отсутствуют")


# 0. Добавление БД и подключение к ней
# (Создать базу данных test.db ...)
connection = create_conn("test.db")


# 1. Добавление таблиц
# (... состоящую из трех таблиц Person, Company, LincPC)
sql_create_table_person = """CREATE TABLE IF NOT EXISTS Person (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name varchar(80) NOT NULL,
                                gender varchar(6) NOT NULL,
                                age integer NOT NULL,
                                registered text NOT NULL
                            );"""

sql_create_table_company = """CREATE TABLE IF NOT EXISTS Company (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name varchar(80) NOT NULL
                            );"""

sql_create_table_linkpc = """CREATE TABLE IF NOT EXISTS LinkPC (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                person_id integer,
                                company_id integer,
                                salary integer,
                                FOREIGN KEY (person_id) REFERENCES Person (id) on delete cascade,
                                FOREIGN KEY (company_id) REFERENCES Company (id) on delete cascade
                            );"""
if connection is not None and CREATE_TABLE:
    create_table(connection, sql_create_table_person)
    create_table(connection, sql_create_table_company)
    create_table(connection, sql_create_table_linkpc)


# 2. Заполнение таблиц исходными данными
# (... Далее необходимо заполнить таблицу следующими данными)
if connection is not None and ADD_DATA_1:
    person_1 = ('Mccormick Roy', 'male', 42, '2020-04-25')
    person_2 = ('Ericka Cummings', 'female', 35, '2020-01-01')
    person_3 = ('Ruiz Cooper', 'male', 20, '2019-12-20')

    company_1 = ('Sendit',)
    company_2 = ('Interse',)
    company_3 = ('Online Anywhere',)

    linkpc_1 = (1, 1, 23000)
    linkpc_2 = (2, 1, 25000)
    linkpc_3 = (3, 2, 30000)

    create_person(connection, person_1)
    create_person(connection, person_2)
    create_person(connection, person_3)

    create_company(connection, company_1)
    create_company(connection, company_2)
    create_company(connection, company_3)

    create_linkpc(connection, linkpc_1)
    create_linkpc(connection, linkpc_2)
    create_linkpc(connection, linkpc_3)


# 3. Дополнительные данные
# (Далее необходимо выполнить следующие запросы)
if connection is not None and ADD_DATA_2:
    # (Добавить 3 пользователя в таблицу «Person»)
    person_4 = ('Sasha', 'male', 25, '2020-01-01')
    person_5 = ('Masha', 'female', 26, '2020-01-02')
    person_6 = ('Dasha', 'female', 27, '2020-01-03')
    create_person(connection, person_4)
    create_person(connection, person_5)
    create_person(connection, person_6)

    # (Добавить 2 компании в таблицу «Company»)
    company_4 = ('Sberbank',)
    company_5 = ('Rosbank',)
    create_company(connection, company_4)
    create_company(connection, company_5)

    # (Добавить связи между пользователя и компаниями через таблицу «LinkPC»)
    linkpc_4 = (4, 2, 50000)
    linkpc_5 = (5, 2, 55000)
    linkpc_6 = (6, 2, 60000)
    create_linkpc(connection, linkpc_4)
    create_linkpc(connection, linkpc_5)
    create_linkpc(connection, linkpc_6)


# 4. Изменить имя
# (Изменить имя пользователя №1 на другое)
if connection is not None and CHANGE_NAME:
    person = ('Tommy', 1)
    update_person_name(connection, person)


# 5. Удалить пользователя
# (Удалить пользователя №2 – что произошло?)
# (Ответ - удалились также данные о пользователе №2 из таблицы LinkPC)
if connection is not None and DELETE_PERSON:
    person_id = (2,)
    delete_person(connection, person_id)


# 6. Вывести данные
# (Вывести таблицу, в которой будут указаны все женщины с их зарплатой)
if connection is not None and SELECT_DATA_1:
    select_data_1(connection)


# 7. Вывести данные
# (Вывести, сколько мужчин и женщин в базе данных)
if connection is not None and SELECT_DATA_2:
    select_data_2(connection)


# 8. Вывести данные
# (Вывести компании, в которых работало больше 3 сотрудников)
if connection is not None and SELECT_DATA_3:
    select_data_3(connection)

