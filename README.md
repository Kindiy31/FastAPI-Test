# REST API для Інтернет-Магазину

Цей проект реалізує REST API для інтернет-магазину, що дозволяє керувати товарами, фільтрувати їх за категоріями, а також виконувати інші операції, такі як додавання товару, зміна ціни, резервування, продаж, і створення звітів про продані товари.

## Зміст

- [Опис завдання](#опис-завдання)
- [Функціональність API](#функціональність-api)
- [Структура проекту](#структура-проекту)
- [Інструкція по запуску](#інструкція-по-запуску)
- [Міграції бази даних](#міграції-бази-даних)


## Опис завдання

Завдання полягало в розробці REST API для інтернет-магазину з наступними вимогами:

### API має підтримувати такі операції:

- **Отримання списку товарів**
- **Фільтр товарів за категоріями та підкатегоріями**
- **Додавання товару**
- **Зміна ціни товару**
- **Старт акції (процент знижки)**
- **Видалення товару**
- **Резервування товару**
- **Скасування резерву**
- **Продаж товару**
- **Звіт про продані товари з можливістю фільтрації**

### Додаткові вимоги:

- Товар відображається у списку тільки якщо вільний залишок > 0.
- Користувачі можуть резервувати, відміняти бронювання і купувати товари.
- При резервуванні, вільний залишок товару зменшується.
- При відміні резервування, вільний залишок товару збільшується.
- Всі відповіді мають використовувати відповідні HTTP статуси (404, 400, 403 і т.д.).

## Функціональність API

### Основні методи API:

1. **GET /products** - Отримання списку товарів (з посторінковою навігацією та фільтрами).
2. **POST /products** - Додавання нового товару.
3. **PUT /products/{id}/price** - Зміна ціни товару.
4. **POST /products/{id}/promotion** - Старт акції для товару (процент знижки).
5. **DELETE /products/{id}** - Видалення товару.
6. **POST /products/{id}/reserve** - Резервування товару.
7. **DELETE /products/{id}/reserve** - Скасування резерву товару.
8. **POST /products/{id}/sell** - Продаж товару.
9. **GET /sales/report** - Отримання звіту про продані товари з можливістю фільтрації.

### Додаткові функції:

- **Посторінкова навігація** у списках товарів.
- **Міграції** бази даних за допомогою Alembic.

## Структура проекту

Проект організовано відповідно до принципів предметно-орієнтованого програмування (DDD):

- **`app/models/`** - Опис моделей бази даних.
- **`app/schemas/`** - Pydantic схеми для валідації даних.
- **`app/repositories/`** - Логіка взаємодії з базою даних.
- **`app/services/`** - Логіка бізнес-процесів.
- **`app/endpoints/`** - Опис API маршрутів.

## Інструкція по запуску

1. Клонувати репозиторій:
    ```bash
    git clone git@github.com:Kindiy31/FastAPI-Test.git
    cd FastAPI-Test
    ```

2. Встановити залежності:
    ```bash
    pip install -r requirements.txt
    ```

3. Налаштувати базу даних у файлі `.env`.

4. Запустити міграції бази даних:
    ```bash
    alembic upgrade head
    ```

5. Запустити додаток:
    ```bash
    uvicorn app.main:app --reload
    ```

6. API буде доступний за адресою [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Міграції бази даних

Для роботи з базою даних використовуються міграції за допомогою Alembic. Щоб застосувати міграції, виконайте команду:

```bash
alembic upgrade head
