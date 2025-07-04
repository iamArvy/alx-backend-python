# ALX ProDev Python Generators

This repository contains Python scripts for managing and processing user data stored in a MySQL database. It demonstrates the use of Python generators for memory-efficient data operations.

---

## 📁 Contents

### ✅ `seed.py`

Initializes the MySQL database and seeds it with data from `user_data.csv`.

* **Creates** the `ALX_prodev` database (if not exists)
* **Creates** the `user_data` table with the following fields:

  * `user_id` (UUID, Primary Key)
  * `name` (VARCHAR, Not Null)
  * `email` (VARCHAR, Not Null)
  * `age` (DECIMAL, Not Null)
* **Loads** data from `user_data.csv` into the database, skipping duplicates

---

### ✅ `0-stream_users.py`

Streams user rows one by one using a Python generator for efficient memory usage.

```python
def stream_users()
```

---

### ✅ `1-batch_processing.py`

Streams user data in batches using a generator.

```python
def stream_users_in_batches(batch_size)
def batch_processing(batch_size)
```

Filters users over age 25 from each batch using no more than 3 loops.

---

### ✅ `2-lazy_paginate.py`

Simulates lazy pagination from the database.

```python
def paginate_users(page_size, offset)
def lazy_paginate(page_size)
```

Lazily fetches each page from the database only when needed using a generator.

---

### ✅ `4-stream_ages.py`

Calculates the average user age using a generator in a memory-efficient way.

```python
def stream_user_ages()
def calculate_average_age()
```

Uses at most two loops and **does not** use SQL's `AVG()` function.

---

## 📓 Sample CSV Format

Make sure your `user_data.csv` file is in the same directory and follows this format:

```csv
name,email,age
Alice Smith,alice@example.com,30
Bob Jones,bob@example.com,22
Charlie Ray,charlie@example.com,27
```

---

## 📃 Requirements

* Python 3.x
* MySQL Server
- Other dependencies listed in the requirements.txt file
  Install all Python dependencies by running:

  ```bash
  pip install -r requirements.txt
  ```

---

## ⚙️ Setup Instructions

1. Update MySQL credentials in .env
2. Run the seeding script:

   ```bash
   python seed.py
   ```
3. Run any of the data processing scripts to stream or analyze users.
