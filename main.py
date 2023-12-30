import sqlite3

def create_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return connection

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)

def add_country(connection, country):
    sql = '''INSERT INTO countries (title) VALUES (?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, country)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def add_city(connection, city):
    sql = '''INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def add_student(connection, student):
    sql = '''INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, student)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

countries = '''
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)'''

cities = '''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    area FLOAT DEFAULT 0,
    country_id INTEGER DEFAULT NULL REFERENCES countries(id) ON DELETE NO ACTION
)'''

students = '''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    city_id INTEGER DEFAULT NULL REFERENCES cities(id) ON DELETE NO ACTION
)'''

db_file = 'students.db'

countries_list = ['Kyrgyzstan', 'Russia', 'Italy']
cities_list = [('Bishkek', 3.2, 1), ('Osh', 2.7, 1), ('Moscow', 8.7, 2), ('Novosibirsk', 2.5, 2), ('Krasnoyarsk', 5.9, 2), ('Rome', 4.9, 3), ('Venice', 3.8, 3)]
students_list = [('Alice', 'Hogwards', 3), ('Nurlan', 'Toktobekov', 1), ('Rinat', 'Nigatullin', 5), ('Kosaka', 'Mokava', 1), ('Nettle', 'Perkin', 7), ('Katie', 'Veryaskina', 3), ('Eva', 'Elvion', 7), ('Adol', 'Meta', 2), ('Nikita', 'Saharov', 3), ('Umar', 'Zhumaev', 1), ('Malik', 'Abdurahmanov', 1), ('Ivan', 'Vernovsky', 6), ('Natalya', 'Valueva', 5), ('Jinny', 'Minter', 7), ('Keros', 'Faster', 6)]

connect = create_connection(db_file)
if connect is not None:
    print("Done!")
    # create_table(connect, countries)
    # for i in countries_list:
    #     add_country(connect, (i, ))
    # create_table(connect, cities)
    # for i in cities_list:
    #     i = tuple(i)
    #     add_city(connect, i)
    # create_table(connect, students)
    # for i in students_list:
    #     i = tuple(i)
    #     add_student(connect, i)

def show_students(connection, city_id):
    sql = '''SELECT 
        st.first_name, 
        st.last_name, 
        (SELECT co.title FROM countries AS co WHERE co.id = (SELECT country_id FROM cities WHERE id = st.city_id)),
        (SELECT ci.title FROM cities AS ci WHERE ci.id = st.city_id),
        (SELECT ci.area FROM cities AS ci WHERE ci.id = st.city_id)
    FROM students AS st
    WHERE st.city_id IN (SELECT id FROM cities WHERE id = ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (city_id, ))
        rows_list = cursor.fetchall()
        sql = '''SELECT title FROM cities WHERE id = ?'''
        cursor.execute(sql, (city_id, ))
        city = cursor.fetchone()
        print(f'\nПолный список студентов в городе {city[0]}')
        for row in rows_list:
            print(f'Имя: {row[0]}, Фамилия: {row[1]}, Страна: {row[2]}, Город: {row[3]}, Площадь {row[4]} млн.кв.км')
    except sqlite3.Error as e:
        print(e)

def show_cities(connection):
    sql = '''SELECT * FROM cities'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows_list = cursor.fetchall()
        return rows_list
    except sqlite3.Error as e:
        print(e)

try:
    cities = show_cities(connect)
    city_id = input('Выбери id города по списке ниже, для вывода студентов(0 выдаст выход из запроса):'
                    f'\n{", ".join([f"{i[0]}. {i[1]}" for i in cities])}'
                    f'\nid города:')
    if city_id == '0':
        print('Вы успешно вышли из запроса')
    else:
        show_students(connect, city_id)
except:
    print('Неверный ответ для запроса!')