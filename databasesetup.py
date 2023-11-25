import sqlite3
import json
from sqlite3 import Error

'''
create_table(conn, petTableSQL)
        create_table(conn, foodTableSQL)
        create_table(conn, bowlTableSQL)
        create_table(conn, weightTableSQL)

 petTableSQL = "CREATE TABLE IF NOT EXISTS Pet ( \
                        pet_id integer PRIMARY KEY AUTOINCREMENT, \
                        name text NOT NULL, \
                        animal_type text, \
                        weight decimal \
                    );"
    foodTableSQL = "CREATE TABLE IF NOT EXISTS PetFood ( \
                        food_id integer PRIMARY KEY AUTOINCREMENT, \
                        name text NOT NULL, \
                        kcal_per_kg integer \
                    );"
    bowlTableSQL = "CREATE TABLE IF NOT EXISTS FoodBowl ( \
                            bowl_id integer PRIMARY KEY AUTOINCREMENT, \
                            pet_id integer NOT NULL, \
                            food_id integer NOT NULL, \
                            bowl_weight decimal, \
                            FOREIGN KEY (pet_id) REFERENCES Pet (pet_id), \
                            FOREIGN KEY (food_id) REFERENCES PetFood (food_id) \
                        );"
    # Or make just one table for the weight (foodbowl and/or pet)
    weightTableSQL = "CREATE TABLE IF NOT EXISTS PetWeight ( \
                        weight_id integer PRIMARY KEY AUTOINCREMENT, \
                        pet_id integer, \
                        bowl_id integer, \
                        weight decimal, \
                        weight_change_time datetime NOT NULL, \
                        is_being_filled boolean,\
                        FOREIGN KEY (pet_id) REFERENCES Pet (pet_id), \
                        FOREIGN KEY (bowl_id) REFERENCES FoodBowl (bowl_id) \
                    );"
'''


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)


    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def select_pets(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM Pet")
        pets = c.fetchall()
        c.close()
        return json.dumps(pets)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def add_weight(db_file, t, w):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        time = "'" + t + "'"
        statement = "INSERT INTO Weight (time, weight) VALUES ({}, {})".format(time, w)
        c.execute(statement)
        conn.commit()
        c.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def select_weights(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM Weight")
        weights = c.fetchall()
        c.close()
        return json.dumps(weights)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_user_by_credentials(db_file, username, password):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        c.close()
        return user
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()