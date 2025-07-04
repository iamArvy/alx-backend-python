from seed import connect_to_prodev

def stream_user_ages():
    conn = connect_to_prodev()  # Replace with actual DB path
    cursor = conn.cursor()
    cursor.execute('SELECT age FROM user_data')

    for row in cursor:
        yield row[0]  # assuming age is in the first (and only) column

    conn.close()

def calculate_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

def main():
    calculate_average_age()

if __name__ == '__main__':
    main()