import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

def load_csv_data(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [(row[0], row[1], float(row[2])) for row in reader]

def generate_uuid():
    return str(uuid.uuid4())


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword"
    )

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age TINYINT UNSIGNED NOT NULL
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

def insert_data(connection, filepath):
    data: list = load_csv_data(filepath)
    if not data:
        print("No data to insert.")
        return
    
    cursor = connection.cursor()

    for name, email, age in data:
        # Check for existing entry with same email
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            continue  # Skip duplicates

        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (generate_uuid(), name, email, age)
        )

    connection.commit()
    cursor.close()

def main():
    try:
        conn = connect_db()
        if conn.is_connected():
            create_database(conn)
            conn.close()
            print("Connected to MySQL Server version", conn.server_info)
            print("Database ALX_prodev created successfully.")

            conn_prodev = connect_to_prodev()
            if conn_prodev.is_connected():
                create_table(conn_prodev)
                insert_data(conn_prodev, 'user_data.csv')
                cursor = conn_prodev.cursor()
                cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
                if cursor.fetchone():
                    print("Database ALX_prodev is present")

                cursor.execute("SELECT * FROM user_data LIMIT 5;")
                for row in cursor.fetchall():
                    print(row)

                cursor.close()
                conn_prodev.close()
            else:
                print("Failed to connect to ALX_prodev database.")
                exit(1)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

if __name__ == '__main__':
    main()