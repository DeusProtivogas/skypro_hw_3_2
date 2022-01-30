import sqlite3

# import prettytable

def restart_database():

    # запросы для создания таблиц

    query_create_outcome_type = """
        CREATE TABLE IF NOT EXISTS outcome_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome_type VARCHAR(20)
        )
    """

    query_create_outcome_subtype = """
        CREATE TABLE IF NOT EXISTS outcome_subtype (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome_subtype VARCHAR(20)
        )
    """


    query_create_outcome = """
        CREATE TABLE IF NOT EXISTS outcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age VARCHAR(20),
            type INTEGER,
            subtype INTEGER,
            month INTEGER,
            year INTEGER,
            FOREIGN KEY (type) REFERENCES outcome_type(id),
            FOREIGN KEY (subtype) REFERENCES outcome_subtype(id)
        )
    """

    query_create_type = """
        CREATE TABLE IF NOT EXISTS animal_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_type VARCHAR(20)
        )
    """



    query_create_colors = """
        CREATE TABLE IF NOT EXISTS colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color1 VARCHAR(20),
            color2 VARCHAR(20)
        )
    """

    query_create_breed = """
        CREATE TABLE IF NOT EXISTS breed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_breed VARCHAR(20)
        )
    """

    query_create_animals = """
        CREATE TABLE IF NOT EXISTS animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id VARCHAR(20),
            name VARCHAR(20),
            birth_date VARCHAR(20),
            animal_type INTEGER,
            breed_id INTEGER,
            color_id INTEGER,
            outcome_id INTEGER,
            FOREIGN KEY (animal_type) REFERENCES animal_type(id),
            FOREIGN KEY (breed_id) REFERENCES breed(id),
            FOREIGN KEY (color_id) REFERENCES colors(id),
            FOREIGN KEY (outcome_id) REFERENCES outcome(id)
        )
    """

    # запросы для удаления таблиц

    delete_outcome = """
        DROP TABLE outcome
    """

    delete_outcome_type = """
        DROP TABLE outcome_type
    """

    delete_outcome_subtype = """
        DROP TABLE outcome_subtype
    """

    delete_colors = """
        DROP TABLE colors
    """

    delete_breed = """
        DROP TABLE breed
    """

    delete_animal = """
        DROP TABLE animal
    """

    delete_animal_type = """
        DROP TABLE animal_type
    """


    with sqlite3.connect("animal.db") as connection:
        cursor = connection.cursor()

        #  Удаление таблиц для пересоздания (хотя бы на время учебы)

        cursor.execute(delete_outcome)
        cursor.execute(delete_outcome_type)
        cursor.execute(delete_outcome_subtype)
        cursor.execute(delete_colors)
        cursor.execute(delete_breed)
        cursor.execute(delete_animal_type)
        cursor.execute(delete_animal)

        # создание таблиц и тестирование вывода (проверка создания таблиц, названий столбцов)

        # result_query_outcome_type = ('SELECT * from outcome_type')
        cursor.execute(query_create_outcome_type)
        # table = cursor.execute(result_query_outcome_type)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_outcome_subtype = ('SELECT * from outcome_subtype')
        cursor.execute(query_create_outcome_subtype)
        # table = cursor.execute(result_query_outcome_subtype)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_outcome = ('SELECT * from outcome')
        cursor.execute(query_create_outcome)
        # table = cursor.execute(result_query_outcome)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_colors = ('SELECT * from colors')
        cursor.execute(query_create_colors)
        # table =     cursor.execute(result_query_colors)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_animal_type = ('SELECT * from animal_type')
        cursor.execute(query_create_type)
        # table = cursor.execute(result_query_animal_type)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_breed = ('SELECT * from breed')
        cursor.execute(query_create_breed)
        # table = cursor.execute(result_query_breed)
        # mytable = prettytable.from_db_cursor(table)
        # print(mytable)

        # result_query_animals = ('SELECT * from animal')
        cursor.execute(query_create_animals)

        # получаем всех животных из изначальной таблицы

        all_animals = cursor.execute('SELECT * FROM animals').fetchall()

        # счетчик животных для вывода более-менее полоски загрузки (и проверки, что цикл работает и не упал)
        # использовалось во время тестов
        # total_animals = len(all_animals)
        # i = 0

        # по одному переносим животных в новые таблицы
        for animal in all_animals:
            # Создаю словарь с данными нового животного

            new_animal_info = {}

            # Получаю breed_id если есть, иначе добавляю новый в таблицу

            check_animal_breed = f"""
                SELECT * FROM breed
                WHERE animal_breed = '{animal[5]}'
            """

            animal_breed = cursor.execute(check_animal_breed).fetchall()

            if not animal_breed: # inserting new breed in the table if such breed was not found
                ins_new_breed = f"""
                    INSERT INTO breed (animal_breed) VALUES ('{animal[5]}')
                """
                cursor.execute(ins_new_breed)
                animal_breed = cursor.execute(check_animal_breed).fetchall()
            breed_id = animal_breed[0][0]

            new_animal_info['breed'] = breed_id


            check_animal_type = f"""
                        SELECT * FROM animal_type
                        WHERE animal_type = '{animal[3]}'
                    """

            animal_type = cursor.execute(check_animal_type).fetchall()

            if not animal_type:  # inserting new animal_type in the table if such breed was not found
                ins_new_type = f"""
                            INSERT INTO animal_type (animal_type) VALUES ('{animal[3]}')
                        """
                cursor.execute(ins_new_type)
                animal_type = cursor.execute(check_animal_type).fetchall()
            type_id = animal_type[0][0]

            new_animal_info['type'] = type_id

            # Получаю color_id если есть, иначе добавляю новый в таблицу

            check_animal_colors = f"""
                        SELECT * FROM colors
                        WHERE color1 = '{animal[6]}' AND color2 = '{animal[7]}'
                    """

            animal_colors = cursor.execute(check_animal_colors).fetchall()

            if not animal_colors:  # inserting new colors in the table if such breed was not found
                ins_new_colors = f"""
                            INSERT INTO colors (color1, color2) VALUES ('{animal[6]}', '{animal[7]}')
                        """
                cursor.execute(ins_new_colors)
                animal_colors = cursor.execute(check_animal_colors).fetchall()
            colors_id = animal_colors[0][0]

            new_animal_info['colors'] = colors_id

            # Добавляю новый outcome в таблицу

            check_animal_outcome_type = f"""
                        SELECT * FROM outcome_type
                        WHERE outcome_type = '{animal[10]}'
                    """

            animal_outcome_type = cursor.execute(check_animal_outcome_type).fetchall()

            if not animal_outcome_type:  # inserting new outcome type in the table if such outcome type was not found
                ins_new_outcome_type = f"""
                            INSERT INTO outcome_type (outcome_type) VALUES ('{animal[10]}')
                        """
                cursor.execute(ins_new_outcome_type)
                animal_outcome_type = cursor.execute(check_animal_outcome_type).fetchall()
            outcome_type_id = animal_outcome_type[0][0]

            check_animal_outcome_subtype = f"""
                                SELECT * FROM outcome_subtype
                                WHERE outcome_subtype = '{animal[9]}'
                            """

            animal_outcome_subtype = cursor.execute(check_animal_outcome_subtype).fetchall()

            if not animal_outcome_subtype:  # inserting new outcome subtype in the table if such outcome subtype was not found
                ins_new_outcome_subtype = f"""
                                    INSERT INTO outcome_subtype (outcome_subtype) VALUES ('{animal[9]}')
                                """
                cursor.execute(ins_new_outcome_subtype)
                animal_outcome_subtype = cursor.execute(check_animal_outcome_subtype).fetchall()
            outcome_subtype_id = animal_outcome_subtype[0][0]

            ins_new_outcome = f"""
                INSERT INTO outcome (age, type, subtype, month, year) 
                VALUES ('{animal[1]}', '{outcome_type_id}', '{outcome_subtype_id}', '{int(animal[11])}', '{int(animal[12])}')
            """

            cursor.execute(ins_new_outcome)

            get_outcome_id = f"""
                SELECT * FROM outcome
                WHERE age = '{animal[1]}' AND
                type = '{outcome_type_id}' AND
                subtype = '{outcome_subtype_id}' AND
                month = '{int(animal[11])}' AND
                year = '{int(animal[12])}'
            """
            animal_outcome = cursor.execute(get_outcome_id).fetchall()
            outcome_id = animal_outcome[0][0]

            new_animal_info['outcome'] = outcome_id

            new_animal_info['id'] = animal[2]
            new_animal_info['name'] = str(animal[4]).replace('\'', '')
            new_animal_info['birth_date'] = animal[8]

            ins_new_animal = f"""
                INSERT INTO animal (animal_id, name, birth_date, animal_type, breed_id, color_id, outcome_id)
                VALUES ('{new_animal_info['id']}', '{new_animal_info['name']}', '{new_animal_info['birth_date']}', 
                '{new_animal_info['type']}', '{new_animal_info['breed']}', '{new_animal_info['colors']}',
                '{new_animal_info['outcome']}')
            """


            cursor.execute(ins_new_animal)

            #  Вывод степени заполнения таблицы
            # i += 1
            # print(f"{i} / {total_animals}")



def get_animal(id):
    """
    Получаем animal по id
    :param id: id animal в таблице
    :return: animal
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM animal
            WHERE id = '{id}'
        """

        print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        print(executed)
        return executed

def get_outcome(id):
    """
    Получаем outcome по id
    :param id: id outcome в таблице
    :return: outcome
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM outcome
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed


def get_outcome_type(id):
    """
    Получаем outcome type по id
    :param id: id outcome type в таблице
    :return: outcome type
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM outcome_type
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed


def get_outcome_subtype(id):
    """
    Получаем outcome subtype по id
    :param id: id outcome subtype в таблице
    :return: outcome subtype
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM outcome_subtype
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed


def get_colors(id):
    """
    Получаем colors по id
    :param id: id colors в таблице
    :return: colors
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM colors
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed


def get_animal_type(id):
    """
    Получаем animal type по id
    :param id: id animal type в таблице
    :return: animal type
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM animal_type
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed


def get_breed(id):
    """
    Получаем breed по id
    :param id: id breed в таблице
    :return: breed
    """
    with sqlite3.connect("animal.db") as connection:
        query = f"""
            SELECT * FROM breed
            WHERE id = '{id}'
        """

        # print(query)

        cursor = connection.cursor()
        executed = cursor.execute(query).fetchall()
        # print(executed)
        return executed

