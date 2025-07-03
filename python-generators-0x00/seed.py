import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password"
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
        user="your_user",
        password="your_password",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX (user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()

    for name, email, age in data:
        # Check for existing entry with same email
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            continue  # Skip duplicates

        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)",
            (user_id, name, email, age)
        )

    connection.commit()
    cursor.close()

def load_csv_data(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [(row[0], row[1], float(row[2])) for row in reader]

if __name__ == '__main__':
    try:
        conn = connect_db()
        create_database(conn)
        conn.close()

        conn_prodev = connect_to_prodev()
        create_table(conn_prodev)

        data = load_csv_data('user_data.csv')
        insert_data(conn_prodev, data)

        conn_prodev.close()
        print("Database seeded successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
