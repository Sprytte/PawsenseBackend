from flask import Flask
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def create_connection(db_file):
    conn = None
    petTableSQL = "CREATE TABLE IF NOT EXISTS Pet ( \
                        pet_id integer PRIMARY KEY, \
                        name text NOT NULL, \
                        animal_type text, \
                        weight decimal \
                    );"
    petWeightTableSQL = "CREATE TABLE IF NOT EXISTS PetWeight ( \
                        weight_id integer PRIMARY KEY, \
                        pet_id integer NOT NULL, \
                        weight decimal, \
                        FOREIGN KEY (pet_id) REFERENCES Pet (pet_id) \
                    );"

    project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        create_table(conn, petTableSQL)
        create_table(conn, petWeightTableSQL)

        create_project(conn, project)
        print("Row added")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_connection(r"C:\sqlite\db\pythonsqlite.db")

    create_connection(r"projManageDB")

    app.run()


