# Дипломная работа. Автоматизация тестирования Kinopoisk

Автоматизация UI- и API тестов из финальной работы по ручному тестированию сервиса "Кинопоиск".

---

## Содержание

- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)
- [Используемые технологии](#используемые-технологии)
- [Тесты](#тесты)
- [Запуск тестов](#запуск-тестов)
- [Просмотр отчетов Allure](#просмотр-отчетов-allure)
- [Маркеры для pytest](#маркеры-для-pytest)
- [Добавление скриншотов в отчёт Allure](#добавление-скриншотов-в-отчёт-allure)

---

## Описание проекта

Проект содержит автоматизированные UI и API тесты для сервиса “Кинопоиск”.  
UI-тесты реализованы с использованием Selenium и паттерна PageObject.  
API-тесты выполняются через HTTP-запросы с помощью библиотеки requests.

---

## Структура проекта

Graduate_work/
├── .gitignore             # Настройки игнорирования файлов Git
├── pages/                 # Page Object, например, MainPage.py
├── tests/
│   ├── test_ui.py         # UI тесты (Selenium + Pytest + Allure)
│   └── test_api.py        # API тесты (requests + Pytest + Allure)
├── config.py              # Конфигурация (ключи, URL и др.)
├── requirements.txt       # Список зависимостей
└── README.md              # Этот файл


---

## Используемые технологии

- Python 3.x
- Selenium WebDriver
- Pytest
- Allure Report
- requests
- webdriver_manager

---

## Тесты

### UI тесты

- Поиск фильма по валидному названию
- Поиск с невалидными символами  
- Негативные проверки поиска  
- Проверка активности кнопки “Смотреть фильм”  
- Проверка авторизации по телефону  

### API тесты

- Поиск фильма по ID и названию  
- Проверка негативных сценариев (неверный ID, отсутствие токена)  
- Фильтрация фильмов по рейтингу и жанру  

---

## Запуск тестов

### Подготовка окружения

python -m venv venv

Windows PowerShell:
.\venv\Scripts\Activate.ps1

или CMD:
venv\Scripts\activate.bat

pip install -r requirements.txt

### Запуск UI тестов

pytest -m ui --alluredir=allure-results/ui

---

## Просмотр отчетов Allure

После прогона тестов запускайте:

allure serve allure-results/ui

<img width="1615" height="866" alt="Test_ui" src="https://github.com/user-attachments/assets/8417d2cf-7eb6-4717-8949-1eaaa44e2ed0" />

или

allure serve allure-results/api

<img width="1605" height="788" alt="Test_api" src="https://github.com/user-attachments/assets/1885f2d4-a1de-4592-bae9-f63e302dc1d8" />

для визуального просмотра результатов.
---

## Маркеры для pytest

В `pytest.ini` прописаны следующие маркеры:

[pytest]
markers =
ui: пометка UI-тестов
api: пометка API-тестов
positive_test: позитивные тесты
negative_test: негативные тесты

---

## Добавление скриншотов в отчёт Allure

Чтобы добавить скриншот в Allure отчет (например, при провале теста UI), используйте в коде следующий подход:

import allure

В момент, когда нужно прикрепить скриншот:
with allure.step("Прикрепить скриншот страницы"):
allure.attach.file(
'path/to/screenshot.png',
name="Скриншот ошибки",
attachment_type=allure.attachment_type.PNG
)

### Общие рекомендации:

- Скриншоты делайте через Selenium `.get_screenshot_as_file('path.png')` или `.get_screenshot_as_png()`.
- Если используете `.get_screenshot_as_png()`, можно прикрепить сразу из байтов:

with allure.step("Добавить скриншот из памяти"):
png = driver.get_screenshot_as_png()
allure.attach(png, name="Скриншот ошибки", attachment_type=allure.attachment_type.PNG)

- Рекомендуется сохранять скриншоты в отдельную папку, например, `screenshots/`.
- Скриншоты удобно прикреплять в блоке `except` при ловле ошибок.
