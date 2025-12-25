from sqlalchemy import create_engine, text
from dotenv import load_dotenv 
import os 

load_dotenv()

# Handle potential postgres:// vs postgresql:// protocol mismatch
db_connection_str = os.getenv('CONN_STR')

if not db_connection_str:
    print("WARNING: 'conn_str' environment variable is not set. Using file-based SQLite (genboi.db).")
    db_connection_str = "sqlite:///genboi.db"
else:
    print("INFO: 'conn_str' found. Connecting to external database (Neon/PostgreSQL).")
    if db_connection_str.startswith("postgres://"):
        db_connection_str = db_connection_str.replace("postgres://", "postgresql://", 1)

# Create engine with pool_pre_ping to avoid TCP/IP errors on stale connections
engine = create_engine(db_connection_str, pool_pre_ping=True)

def push(email, name, password):
    try:
        with engine.connect() as connection:
            query = text("insert into genboi_users(email, name, password) values(:email, :name, :password)")
            connection.execute(query, {"email": email, "name": name, "password": password})
            connection.commit()
    except Exception as e:
        print(f"Error in push: {e}")

def delete_user(email):
    try:
        with engine.connect() as connection:
            query = text("delete from genboi_users where email = :email")
            connection.execute(query, {"email": email})
            connection.commit()
    except Exception as e:
        print(f"Error in delete_user: {e}")

def get_password(email):
    try:
        with engine.connect() as connection:
            query = text("select password from genboi_users where email = :email")
            result = connection.execute(query, {"email": email}).fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error in get_password: {e}")
        return None


def get_name(email):
    try:
        with engine.connect() as connection:
            query = text("select name from genboi_users where email = :email")
            result = connection.execute(query, {"email": email}).fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error in get_name: {e}")
        return None

def update_data(old_email, new_email, new_name, new_password):
    try:
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM genboi_users WHERE email = :old_email"), {"old_email": old_email})
            connection.execute(text("INSERT INTO genboi_users (email, name, password) VALUES (:new_email, :new_name, :new_password)"), {"new_email": new_email, "new_name": new_name, "new_password": new_password})
    except Exception as e:
        print(f"Error in update_data: {e}")


def isCorrectCredentials(email, password):
    try:
        with engine.connect() as connection:
            query = text("select 1 from genboi_users where email = :email and password = :password")
            result = connection.execute(query, {"email": email, "password": password}).fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in isCorrectCredentials: {e}")
        return False

def isEmailExists(email):
    try:
        with engine.connect() as connection:
            query = text("select 1 from genboi_users where email = :email")
            result = connection.execute(query, {"email": email}).fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in isEmailExists: {e}")
        return False

def create_table():
    try:
        with engine.connect() as connection:
            if 'sqlite' in engine.dialect.name:
                id_col = "id INTEGER PRIMARY KEY AUTOINCREMENT"
            else:
                id_col = "id SERIAL PRIMARY KEY"

            connection.execute(text(f"""
                CREATE TABLE IF NOT EXISTS genboi_users (
                    {id_col},
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """))
            connection.commit()
        print("Table 'genboi_users' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == '__main__':
    create_table()
