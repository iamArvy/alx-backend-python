# GitHub Org Client – Python Unit & Integration Testing

This project provides a comprehensive testing suite for a GitHub Organization client written in Python 3. It demonstrates best practices for unit testing, integration testing, and mocking external API calls using `unittest`, `parameterized`, and `unittest.mock`.

## ✅ Features

* Access nested dictionary data with error handling
* Fetch JSON from remote APIs
* Memoize class method results for performance
* Client class to interact with GitHub organization data
* Full unit and integration test coverage

## 🧪 Test Coverage

This repository includes tests for:

### `utils.py`

* `access_nested_map`: Safely access nested dictionary values
* `get_json`: Fetch and parse JSON data from a URL
* `memoize`: Decorator to cache method results

### `client.py`

* `GithubOrgClient`: Fetch org metadata, repositories, and filter by license

## 🧬 Technologies

* **Python 3.7+**
* **Ubuntu 18.04 LTS**
* `unittest`
* `parameterized`
* `unittest.mock`

## 📁 Folder Structure

```
.
├── client.py                # GitHubOrgClient class
├── utils.py                 # Utility functions and memoize decorator
├── test_client.py           # Unit and integration tests for client.py
├── test_utils.py            # Unit tests for utils.py
├── fixtures.py              # Fixture data for integration testing
└── README.md
```

## 🔧 Requirements

* All files begin with `#!/usr/bin/env python3`
* PEP8 compliant (using `pycodestyle==2.5`)
* Each file ends with a new line
* All functions, classes, and modules are documented
* All functions are type-annotated
* All Python scripts are executable

## 🚀 Running Tests

```bash
# Install dependencies
pip install parameterized pycodestyle

# Run all tests
python3 test_utils.py
python3 test_client.py
```

## 🔍 Lint Check

```bash
pycodestyle .
```

## 👨‍💻 Author

Built as a hands-on Python testing exercise. Demonstrates real-world testing for classes that interact with APIs and internal logic with strict compliance to standards.
