from seed import connect_to_prodev
import sys

def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data LIMIT %s OFFSET %s', (page_size, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

def main():
    try:
        for page in lazy_paginate(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()

if __name__ == '__main__':
    main()