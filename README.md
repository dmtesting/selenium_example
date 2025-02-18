# Для начала работы нужно установить python3 и pip

Далее

- pip install pytest
- pip install pytest-bdd
- pip install selenium
- pip install gherkin-official

# Запуск тестов

pytest -s -m dev_regression

## Запуск одного теста

pytest -s -m some_test_name

Рабочий пример:
pytest -s -m test_example
