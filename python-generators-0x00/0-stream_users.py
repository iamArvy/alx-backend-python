from seed import connect_to_prodev
from itertools import islice

def stream_users():
    conn = connect_to_prodev()  # Replace with your actual DB
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data')
    for row in cursor:
        yield row

    conn.close()

def main():
    for user in islice(stream_users(), 6):
        print(user)

if __name__ == '__main__':
    main()