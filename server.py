import psycopg2
from dotenv import load_dotenv 
import os
from dotenv import load_dotenv

load_dotenv()

def push(email, name, password):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"insert into genboi_users(email, name, password) values('{email}', '{name}', '{password}')"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def delete_user(email):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"delete from genboi_users where email = '{email}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def get_password(email):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"select password from genboi_users where email = '{email}'"
    cursor.execute(query)
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password


def get_name(email):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"select name from genboi_users where email = '{email}'"
    cursor.execute(query)
    name = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return name

def update_data(old_email, new_email, new_name, new_password):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM genboi_users WHERE email = %s", (old_email,))
    cursor.execute("INSERT INTO genboi_users (email, name, password) VALUES (%s, %s, %s)", (new_email, new_name, new_password))
    connection.commit()
    cursor.close()
    connection.close()


def isCorrectCredentials(email, password):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"select 1 from genboi_users where email = '{email}' and password = '{password}'"
    cursor.execute(query)
    x = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return not x is None

def isEmailExists(email):
    connection = psycopg2.connect(
        host=os.getenv('SB_HOST'),
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    query = f"select 1 from genboi_users where email = '{email}'"
    cursor.execute(query)
    x = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return x is not None


if __name__ == '__main__':
    print(isEmailExists('akash@gmail.com'))