from seed import connect_to_prodev
import sys

def stream_users_in_batches(batch_size):
    conn = connect_to_prodev()  # Replace with your actual DB
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data')

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    # conn.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user[3] > 25:
                yield user

def main():
    try:
        for user in batch_processing(50):
            print(user)
    except BrokenPipeError:
        sys.stderr.close()

if __name__ == '__main__':
    main()