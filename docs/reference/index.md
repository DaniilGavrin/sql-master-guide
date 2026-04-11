# Справочник SQL команд

Полный справочник всех основных команд SQL с примерами использования.

## 📑 Содержание

- [DDL (Data Definition Language)](#ddl-data-definition-language)
- [DML (Data Manipulation Language)](#dml-data-manipulation-language)
- [DQL (Data Query Language)](#dql-data-query-language)
- [DCL (Data Control Language)](#dcl-data-control-language)
- [TCL (Transaction Control Language)](#tcl-transaction-control-language)

---

## DDL (Data Definition Language)

Команды для определения структуры базы данных.

### CREATE TABLE

Создание новой таблицы.

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    salary NUMERIC(10, 2) CHECK (salary > 0),
    hire_date DATE DEFAULT CURRENT_DATE,
    dept_id INTEGER REFERENCES departments(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### ALTER TABLE

Изменение существующей таблицы.

```sql
-- Добавить столбец
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- Изменить тип столбца
ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12, 2);

-- Добавить ограничение
ALTER TABLE employees ADD CONSTRAINT chk_email CHECK (email LIKE '%@%');

-- Удалить столбец
ALTER TABLE employees DROP COLUMN phone;

-- Переименовать столбец
ALTER TABLE employees RENAME COLUMN first_name TO fname;

-- Переименовать таблицу
ALTER TABLE employees RENAME TO staff;
```

### DROP TABLE

Удаление таблицы.

```sql
DROP TABLE employees;
DROP TABLE IF EXISTS employees; -- Без ошибки, если таблицы нет
DROP TABLE IF EXISTS employees CASCADE; -- Удалить зависимые объекты
```

### CREATE INDEX

Создание индекса.

```sql
CREATE INDEX idx_last_name ON employees(last_name);
CREATE UNIQUE INDEX idx_unique_email ON employees(email);
CREATE INDEX idx_multi ON employees(dept_id, salary DESC);
```

### DROP INDEX

Удаление индекса.

```sql
DROP INDEX idx_last_name;
```

### CREATE VIEW

Создание представления.

```sql
CREATE VIEW active_employees AS
SELECT id, name, salary, dept_id
FROM employees
WHERE status = 'active';

-- Использование
SELECT * FROM active_employees WHERE salary > 50000;
```

### DROP VIEW

Удаление представления.

```sql
DROP VIEW active_employees;
```

### CREATE SEQUENCE

Создание последовательности.

```sql
CREATE SEQUENCE employee_id_seq START WITH 1 INCREMENT BY 1;

-- Использование
INSERT INTO employees (id, name) VALUES (nextval('employee_id_seq'), 'Иван');
```

---

## DML (Data Manipulation Language)

Команды для манипуляции данными.

### INSERT

Добавление данных.

```sql
-- Одна строка
INSERT INTO employees (name, salary, dept_id)
VALUES ('Иван Петров', 75000, 10);

-- Несколько строк
INSERT INTO employees (name, salary, dept_id)
VALUES 
    ('Мария Иванова', 80000, 20),
    ('Петр Сидоров', 70000, 10),
    ('Анна Козлова', 85000, 30);

-- Из другой таблицы
INSERT INTO employees_archive
SELECT * FROM employees
WHERE hire_date < '2020-01-01';

-- RETURNING возвращающие вставленные данные
INSERT INTO employees (name, salary)
VALUES ('Новый сотрудник', 60000)
RETURNING id, name;
```

### UPDATE

Обновление данных.

```sql
-- Обновление всех строк
UPDATE employees SET salary = salary * 1.1;

-- Обновление с условием
UPDATE employees 
SET salary = salary * 1.1 
WHERE dept_id = 10;

-- Обновление нескольких столбцов
UPDATE employees 
SET salary = salary + 5000, 
    updated_at = NOW()
WHERE id = 123;

-- Обновление из другой таблицы
UPDATE employees e
SET salary = e.salary * 1.1
FROM departments d
WHERE e.dept_id = d.id AND d.budget > 1000000;

-- RETURNING
UPDATE employees 
SET salary = salary + 5000 
WHERE dept_id = 10
RETURNING id, name, salary;
```

### DELETE

Удаление данных.

```sql
-- Удаление всех строк
DELETE FROM employees;

-- Удаление с условием
DELETE FROM employees WHERE dept_id = 10;

-- Удаление с USING
DELETE FROM employees e
USING departments d
WHERE e.dept_id = d.id AND d.status = 'closed';

-- RETURNING
DELETE FROM employees 
WHERE hire_date < '2015-01-01'
RETURNING id, name;
```

### TRUNCATE

Быстрое удаление всех строк.

```sql
TRUNCATE TABLE employees;
TRUNCATE TABLE employees RESTART IDENTITY; -- Сбросить автоинкремент
TRUNCATE TABLE employees, departments CASCADE; -- Несколько таблиц
```

---

## DQL (Data Query Language)

Команды для выборки данных.

### SELECT

Базовый запрос.

```sql
-- Все столбцы
SELECT * FROM employees;

-- Конкретные столбцы
SELECT id, name, salary FROM employees;

-- С выражениями
SELECT name, salary * 12 AS annual_salary FROM employees;

-- DISTINCT
SELECT DISTINCT dept_id FROM employees;

-- Сортировка
SELECT * FROM employees ORDER BY salary DESC;

-- Ограничение
SELECT * FROM employees LIMIT 10 OFFSET 20;
```

### WHERE

Фильтрация данных.

```sql
-- Операторы сравнения
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE salary BETWEEN 50000 AND 100000;
SELECT * FROM employees WHERE dept_id IN (10, 20, 30);
SELECT * FROM employees WHERE name LIKE 'Иван%';
SELECT * FROM employees WHERE email IS NOT NULL;

-- Логические операторы
SELECT * FROM employees 
WHERE dept_id = 10 AND salary > 70000;

SELECT * FROM employees 
WHERE dept_id = 10 OR dept_id = 20;

SELECT * FROM employees 
WHERE NOT (salary < 50000);
```

### JOIN

Объединение таблиц.

```sql
-- INNER JOIN
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- RIGHT JOIN
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;

-- FULL OUTER JOIN
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;

-- CROSS JOIN
SELECT * FROM table1 CROSS JOIN table2;

-- Self JOIN
SELECT e.name, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### GROUP BY

Группировка данных.

```sql
SELECT dept_id, COUNT(*), AVG(salary)
FROM employees
GROUP BY dept_id;

-- С HAVING
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 60000;

-- Группировка по нескольким столбцам
SELECT dept_id, position, COUNT(*)
FROM employees
GROUP BY dept_id, position;
```

### Подзапросы

Вложенные запросы.

```sql
-- В WHERE
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- В FROM
SELECT dept_id, avg_salary
FROM (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) AS dept_stats
WHERE avg_salary > 60000;

-- В SELECT
SELECT 
    name,
    salary,
    (SELECT AVG(salary) FROM employees) AS company_avg
FROM employees;
```

### UNION

Объединение результатов.

```sql
-- UNION (без дубликатов)
SELECT name FROM employees
UNION
SELECT name FROM contractors;

-- UNION ALL (с дубликатами)
SELECT name FROM employees
UNION ALL
SELECT name FROM contractors;
```

---

## DCL (Data Control Language)

Команды управления доступом.

### GRANT

Предоставление прав.

```sql
-- Права на таблицу
GRANT SELECT ON employees TO user_read;
GRANT INSERT, UPDATE ON employees TO user_write;
GRANT ALL PRIVILEGES ON employees TO admin;

-- Права на схему
GRANT USAGE ON SCHEMA public TO user_read;

-- Права на функцию
GRANT EXECUTE ON FUNCTION calculate_bonus TO user_write;

-- Всем пользователям
GRANT SELECT ON employees TO PUBLIC;
```

### REVOKE

Отзыв прав.

```sql
REVOKE SELECT ON employees FROM user_read;
REVOKE INSERT, UPDATE ON employees FROM user_write;
REVOKE ALL PRIVILEGES ON employees FROM admin;
```

---

## TCL (Transaction Control Language)

Команды управления транзакциями.

### BEGIN / COMMIT / ROLLBACK

```sql
-- Начало транзакции
BEGIN;
-- или
START TRANSACTION;

-- Операции
UPDATE employees SET salary = salary * 1.1 WHERE dept_id = 10;
INSERT INTO log (action, created_at) VALUES ('raise', NOW());

-- Подтверждение
COMMIT;

-- Отмена
ROLLBACK;
```

### SAVEPOINT

Точки сохранения.

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT after_first;

UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Что-то пошло не так...
ROLLBACK TO after_first;

-- Исправление
UPDATE accounts SET balance = balance + 100 WHERE id = 3;

COMMIT;
```

### SET TRANSACTION

Настройка транзакции.

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION READ ONLY;
SET TRANSACTION DEFFERED;
```

---

## 📊 Типы данных

### Числовые

| Тип | Описание | Диапазон |
|-----|----------|----------|
| SMALLINT | 2 байта | -32768 до 32767 |
| INTEGER | 4 байта | -2×10⁹ до 2×10⁹ |
| BIGINT | 8 байт | -9×10¹⁸ до 9×10¹⁸ |
| DECIMAL(p,s) | Точное число | p цифр, s после запятой |
| REAL | 4 байта | Приблизительное |
| DOUBLE PRECISION | 8 байт | Высокая точность |

### Строковые

| Тип | Описание |
|-----|----------|
| CHAR(n) | Фиксированная длина |
| VARCHAR(n) | Переменная длина до n |
| TEXT | Неограниченная длина |

### Дата и время

| Тип | Описание |
|-----|----------|
| DATE | Дата (год, месяц, день) |
| TIME | Время (часы, минуты, секунды) |
| TIMESTAMP | Дата и время |
| TIMESTAMPTZ | Дата и время с часовым поясом |
| INTERVAL | Промежуток времени |

### Логический

| Тип | Значения |
|-----|----------|
| BOOLEAN | TRUE, FALSE, NULL |

### JSON

| Тип | Описание |
|-----|----------|
| JSON | Текстовое представление |
| JSONB | Бинарное (быстрее для запросов) |

---

## 🔧 Полезные функции

### Строковые

```sql
LENGTH('text')           -- Длина строки
UPPER('text')            -- В верхний регистр
LOWER('TEXT')            -- В нижний регистр
SUBSTRING('text', 1, 3)  -- Подстрока
TRIM(' text ')           -- Удалить пробелы
REPLACE('text', 'e', 'a')-- Замена
CONCAT('Hello', ' ', 'World') -- Конкатенация
```

### Числовые

```sql
ROUND(3.14159, 2)   -- Округление
CEIL(3.14)          -- Округление вверх
FLOOR(3.14)         -- Округление вниз
ABS(-5)             -- Модуль
RANDOM()            -- Случайное число
```

### Дата и время

```sql
NOW()                        -- Текущая дата и время
CURRENT_DATE                 -- Текущая дата
EXTRACT(YEAR FROM NOW())     -- Извлечь год
AGE(timestamp1, timestamp2)  -- Разница дат
DATE_TRUNC('month', NOW())   -- Усечь до месяца
```

### Агрегатные

```sql
COUNT(*)          -- Количество строк
SUM(column)       -- Сумма
AVG(column)       -- Среднее
MIN(column)       -- Минимум
MAX(column)       -- Максимум
STRING_AGG(col, ',') -- Конкатенация строк
```

### Оконные

```sql
ROW_NUMBER() OVER (ORDER BY col)     -- Номер строки
RANK() OVER (ORDER BY col)           -- Ранг с пропусками
DENSE_RANK() OVER (ORDER BY col)     -- Ранг без пропусков
LAG(col, 1) OVER (ORDER BY col)      -- Предыдущее значение
LEAD(col, 1) OVER (ORDER BY col)     -- Следующее значение
```

---

**Это полный справочник основных команд SQL!** Используйте его как шпаргалку при работе с базами данных.
