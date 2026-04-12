# SQL Master Guide: Полное руководство и шпаргалка

## Оглавление
1. [Основы SQL](#основы-sql)
2. [Продвинутые темы](#продвинутые-темы)
3. [MySQL Специфика](#mysql-специфика)
4. [PostgreSQL Специфика](#postgresql-специфика)
5. [Справочник команд](#справочник-команд)

---

## Основы SQL

### Введение в SQL

**SQL (Structured Query Language)** — стандартизированный язык программирования для работы с реляционными базами данных.

#### Ключевые концепции
- **Реляционная модель**: Данные организованы в таблицы (relations) со строками и столбцами.
- **Первичный ключ (Primary Key)**: Уникальный идентификатор строки.
- **Внешний ключ (Foreign Key)**: Ссылка на первичный ключ другой таблицы.
- **Нормализация**: Процесс организации данных для уменьшения избыточности.

#### Популярные СУБД
- **MySQL**: Популярная открытая СУБД, известная скоростью и простотой.
- **PostgreSQL**: Мощная открытая СУБД с поддержкой сложных запросов и расширений.
- **SQLite**: Легковесная встроенная СУБД.
- **Oracle, SQL Server**: Проприетарные корпоративные решения.

---

### SELECT: Выборка данных

Базовый оператор для получения данных из базы.

#### Синтаксис
```sql
SELECT column1, column2, ...
FROM table_name;
```

#### Выбор всех колонок
```sql
SELECT * FROM users;
```

#### DISTINCT: Уникальные значения
```sql
SELECT DISTINCT country FROM users;
```

#### LIMIT: Ограничение количества строк
```sql
SELECT * FROM products LIMIT 10;
```

#### Псевдонимы (AS)
```sql
SELECT first_name AS name, email AS contact FROM users;
```

---

### WHERE: Фильтрация данных

Используется для выбора записей, соответствующих условиям.

#### Операторы сравнения
- `=` (равно)
- `<>` или `!=` (не равно)
- `>`, `<`, `>=`, `<=`

#### Примеры
```sql
SELECT * FROM users WHERE age > 18;
SELECT * FROM products WHERE price = 100;
```

#### Логические операторы
- `AND`: Оба условия истинны.
- `OR`: Хотя бы одно условие истинно.
- `NOT`: Инверсия условия.

```sql
SELECT * FROM users WHERE age > 18 AND country = 'Russia';
```

#### LIKE: Поиск по шаблону
- `%`: Любое количество символов.
- `_`: Один символ.

```sql
SELECT * FROM users WHERE name LIKE 'A%'; -- Начинается на A
SELECT * FROM users WHERE email LIKE '%@gmail.com';
```

#### BETWEEN: Диапазон значений
```sql
SELECT * FROM products WHERE price BETWEEN 10 AND 50;
```

#### IN: Список значений
```sql
SELECT * FROM users WHERE country IN ('Russia', 'USA', 'Germany');
```

#### IS NULL: Проверка на пустоту
```sql
SELECT * FROM users WHERE phone IS NULL;
```

---

### ORDER BY: Сортировка

Сортирует результат запроса.

#### Синтаксис
```sql
SELECT * FROM products ORDER BY price DESC;
```

#### Сортировка по нескольким полям
```sql
SELECT * FROM users ORDER BY country ASC, age DESC;
```

---

### INSERT: Добавление данных

Добавляет новые строки в таблицу.

#### Вставка одной строки
```sql
INSERT INTO users (name, email, age)
VALUES ('Ivan', 'ivan@example.com', 25);
```

#### Вставка нескольких строк
```sql
INSERT INTO users (name, email, age)
VALUES 
    ('Petr', 'petr@example.com', 30),
    ('Anna', 'anna@example.com', 22);
```

#### Вставка из другой таблицы
```sql
INSERT INTO active_users
SELECT * FROM users WHERE last_login > '2023-01-01';
```

---

### UPDATE: Обновление данных

Изменяет существующие записи.

#### Синтаксис
```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

#### Пример
```sql
UPDATE users
SET age = 26, email = 'new@example.com'
WHERE name = 'Ivan';
```

> **Важно:** Всегда используйте `WHERE`, иначе обновятся все строки!

---

### DELETE: Удаление данных

Удаляет строки из таблицы.

#### Синтаксис
```sql
DELETE FROM table_name WHERE condition;
```

#### Пример
```sql
DELETE FROM users WHERE id = 5;
```

#### Сравнение с TRUNCATE
- `DELETE`: Удаляет строки по условию, можно откатить, медленнее.
- `TRUNCATE`: Удаляет всю таблицу полностью, быстрее, сбрасывает автоинкремент.

```sql
TRUNCATE TABLE users;
```

---

## Продвинутые темы

### JOIN: Соединение таблиц

Объединяет строки из двух или более таблиц.

#### Типы соединений
1. **INNER JOIN**: Только совпадающие строки.
2. **LEFT JOIN**: Все строки левой таблицы + совпадения правой.
3. **RIGHT JOIN**: Все строки правой таблицы + совпадения левой.
4. **FULL OUTER JOIN**: Все строки обеих таблиц.
5. **CROSS JOIN**: Декартово произведение.

#### Пример INNER JOIN
```sql
SELECT u.name, o.order_date
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

#### Пример LEFT JOIN
```sql
SELECT u.name, o.order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- Покажет всех пользователей, даже без заказов
```

---

### Агрегатные функции и группировка

Функции для вычислений над наборами данных.

#### Основные функции
- `COUNT()`: Количество строк.
- `SUM()`: Сумма значений.
- `AVG()`: Среднее значение.
- `MIN()`: Минимальное значение.
- `MAX()`: Максимальное значение.

#### GROUP BY: Группировка
```sql
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country;
```

#### HAVING: Фильтрация групп
```sql
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country
HAVING COUNT(*) > 10;
```

---

### Подзапросы

Запрос внутри другого запроса.

#### Подзапрос в WHERE
```sql
SELECT name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);
```

#### EXISTS: Проверка существования
```sql
SELECT name FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

#### Коррелированный подзапрос
```sql
SELECT name, 
       (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count
FROM users u;
```

---

### Оконные функции

Выполняют вычисления над набором строк, связанных с текущей.

#### Синтаксис
```sql
FUNCTION() OVER (PARTITION BY ... ORDER BY ...)
```

#### ROW_NUMBER: Нумерация строк
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

#### RANK и DENSE_RANK
- `RANK()`: Пропускает номера при равных значениях.
- `DENSE_RANK()`: Не пропускает номера.

#### LAG и LEAD: Доступ к соседним строкам
```sql
SELECT date, sales,
       LAG(sales, 1) OVER (ORDER BY date) as prev_sales
FROM daily_sales;
```

#### Накопительный итог
```sql
SELECT date, sales,
       SUM(sales) OVER (ORDER BY date) as total_sales
FROM daily_sales;
```

---

### CTE (Common Table Expressions)

Временные именованные наборы результатов.

#### Обычный CTE
```sql
WITH high_salary_users AS (
    SELECT * FROM users WHERE salary > 100000
)
SELECT * FROM high_salary_users;
```

#### Рекурсивный CTE
```sql
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```

---

### Индексы и оптимизация

Индексы ускоряют поиск данных.

#### Типы индексов
- **B-Tree**: Стандартный, для диапазонов и сортировки.
- **Hash**: Для точного совпадения (=).
- **GiST/GIN**: Для полнотекстового поиска и массивов (PostgreSQL).

#### Создание индекса
```sql
CREATE INDEX idx_users_email ON users(email);
```

#### EXPLAIN: Анализ плана выполнения
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

#### Советы по оптимизации
1. Используйте индексы на полях в `WHERE` и `JOIN`.
2. Избегайте `SELECT *`, выбирайте только нужные колонки.
3. Используйте `LIMIT` для больших выборок.
4. Анализируйте планы выполнения через `EXPLAIN`.

---

### Транзакции

Последовательность операций как единое целое.

#### Свойства ACID
- **Atomicity (Атомарность)**: Всё или ничего.
- **Consistency (Согласованность)**: Переход из одного валидного состояния в другое.
- **Isolation (Изоляция)**: Параллельные транзакции не мешают друг другу.
- **Durability (Долговечность)**: Сохранение после завершения.

#### Управление транзакциями
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- Или ROLLBACK для отмены
```

#### Уровни изоляции
1. **Read Uncommitted**: Чтение "грязных" данных.
2. **Read Committed**: Чтение только закоммиченных (по умолчанию в PostgreSQL).
3. **Repeatable Read**: Гарантированное повторное чтение.
4. **Serializable**: Полная изоляция.

---

### Хранимые процедуры и функции

#### Создание процедуры (PostgreSQL)
```sql
CREATE OR REPLACE PROCEDURE transfer_money(
    from_id INT, to_id INT, amount DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE accounts SET balance = balance - amount WHERE id = from_id;
    UPDATE accounts SET balance = balance + amount WHERE id = to_id;
END;
$$;
```

#### Вызов процедуры
```sql
CALL transfer_money(1, 2, 100);
```

#### Создание функции
```sql
CREATE OR REPLACE FUNCTION get_user_name(user_id INT)
RETURNS TEXT AS $$
DECLARE
    name_val TEXT;
BEGIN
    SELECT name INTO name_val FROM users WHERE id = user_id;
    RETURN name_val;
END;
$$ LANGUAGE plpgsql;
```

---

## MySQL Специфика

### Установка и подключение

#### Установка на Ubuntu
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### Подключение
```bash
mysql -u root -p
```

#### Создание пользователя и БД
```sql
CREATE DATABASE mydb;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydb.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

### Особенности MySQL

#### Движки хранения
- **InnoDB**: Транзакции, внешние ключи (по умолчанию).
- **MyISAM**: Быстрое чтение, нет транзакций.

#### Специфические типы данных
- `TINYINT(1)`: Часто используется для булевых значений.
- `ENUM`: Перечисление значений.
- `SET`: Множество значений.

#### Функции
- `NOW()`: Текущая дата и время.
- `IFNULL(val, replacement)`: Замена NULL.
- `LIMIT`: Обязательно для обновления/удаления с сортировкой.

#### Шпаргалка команд MySQL
| Команда | Описание |
|---------|----------|
| `SHOW DATABASES;` | Список баз данных |
| `USE db_name;` | Выбор базы |
| `SHOW TABLES;` | Список таблиц |
| `DESCRIBE table;` | Структура таблицы |
| `SHOW PROCESSLIST;` | Активные процессы |
| `KILL process_id;` | Убить процесс |

---

## PostgreSQL Специфика

### Установка и подключение

#### Установка на Ubuntu
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Подключение
```bash
sudo -u postgres psql
```

#### Создание пользователя и БД
```sql
CREATE DATABASE mydb;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE mydb TO user;
```

### Особенности PostgreSQL

#### Продвинутые типы данных
- `JSONB`: Бинарный JSON с индексацией.
- `ARRAY`: Массивы любого типа.
- `UUID`: Уникальные идентификаторы.
- `HSTORE`: Ключ-значение.

#### Расширения
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Поиск по подстроке
```

#### Специфические функции
- `CURRENT_TIMESTAMP`: Текущее время.
- `COALESCE(val, replacement)`: Замена NULL (стандарт).
- `STRING_AGG()`: Конкатенация строк.
- `::type`: Быстрое приведение типов (`'123'::int`).

#### Шпаргалка команд PostgreSQL
| Команда | Описание |
|---------|----------|
| `\l` | Список баз данных |
| `\c db_name` | Подключение к базе |
| `\dt` | Список таблиц |
| `\d table` | Описание таблицы |
| `\du` | Список пользователей |
| `\q` | Выход |

---

## Справочник команд

### Категории команд

#### DDL (Data Definition Language)
- `CREATE`: Создание объектов.
- `ALTER`: Изменение структуры.
- `DROP`: Удаление объектов.
- `TRUNCATE`: Очистка таблицы.

#### DML (Data Manipulation Language)
- `INSERT`: Вставка данных.
- `UPDATE`: Обновление данных.
- `DELETE`: Удаление данных.

#### DQL (Data Query Language)
- `SELECT`: Выборка данных.

#### DCL (Data Control Language)
- `GRANT`: Предоставление прав.
- `REVOKE`: Отзыв прав.

#### TCL (Transaction Control Language)
- `COMMIT`: Фиксация транзакции.
- `ROLLBACK`: Откат транзакции.
- `SAVEPOINT`: Точка сохранения.

### Типы данных (Стандартные)

| Тип | Описание | Пример |
|-----|----------|--------|
| `INT` | Целое число | 100 |
| `DECIMAL(p, s)` | Точное число | 10.50 |
| `VARCHAR(n)` | Строка переменной длины | 'Hello' |
| `TEXT` | Длинный текст | 'Long text...' |
| `DATE` | Дата | '2023-01-01' |
| `TIMESTAMP` | Дата и время | '2023-01-01 12:00:00' |
| `BOOLEAN` | Логический тип | TRUE/FALSE |

### Полезные функции

#### Строковые
- `LENGTH(str)`: Длина строки.
- `UPPER(str) / LOWER(str)`: Регистр.
- `SUBSTRING(str, start, len)`: Подстрока.
- `TRIM(str)`: Удаление пробелов.
- `CONCAT(a, b)`: Конкатенация.

#### Числовые
- `ROUND(num, decimals)`: Округление.
- `FLOOR(num) / CEIL(num)`: Округление вниз/вверх.
- `ABS(num)`: Модуль.

#### Даты
- `NOW()`: Текущие дата и время.
- `DATE_PART('year', date)`: Извлечение части даты.
- `AGE(date1, date2)`: Разница между датами.

---

*Документ сгенерирован автоматически для проекта SQL Master Guide.*
