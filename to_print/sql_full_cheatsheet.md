# Полная шпаргалка по SQL (Версия 1.0.4)

## 1. Основные операторы (DML)

### SELECT – Выборка данных
```sql
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name;
SELECT DISTINCT column FROM table_name;
SELECT column AS alias FROM table_name;
```

### WHERE – Фильтрация
```sql
SELECT * FROM table WHERE column = value;
SELECT * FROM table WHERE column > 100;
SELECT * FROM table WHERE column BETWEEN 10 AND 20;
SELECT * FROM table WHERE column IN (val1, val2);
SELECT * FROM table WHERE column LIKE 'pattern%';
SELECT * FROM table WHERE column ILIKE 'pattern%'; -- PostgreSQL (регистронезависимый)
SELECT * FROM table WHERE column IS NULL;
SELECT * FROM table WHERE column IS NOT NULL;
SELECT * FROM table WHERE column REGEXP '^pattern'; -- MySQL/PostgreSQL
```

### INSERT – Вставка данных
```sql
INSERT INTO table (col1, col2) VALUES (val1, val2);
INSERT INTO table SELECT * FROM other_table;
INSERT INTO table (col1) VALUES (val1), (val2), (val3); -- Множественная вставка
```

### UPDATE – Обновление данных
```sql
UPDATE table SET col1 = val1 WHERE condition;
UPDATE table SET col1 = val1, col2 = val2 WHERE condition;
UPDATE table1 SET col1 = table2.col1 FROM table2 WHERE table1.id = table2.id; -- JOIN update
```

### DELETE – Удаление данных
```sql
DELETE FROM table WHERE condition;
DELETE FROM table; -- Удаляет все строки (но не таблицу)
TRUNCATE TABLE table; -- Быстрое удаление всех строк с сбросом счетчиков
```

---

## 2. Сортировка и ограничение выборки

### ORDER BY – Сортировка
```sql
SELECT * FROM table ORDER BY column ASC;
SELECT * FROM table ORDER BY column DESC;
SELECT * FROM table ORDER BY col1 ASC, col2 DESC;
SELECT * FROM table ORDER BY RAND(); -- Случайный порядок (MySQL)
SELECT * FROM table ORDER BY RANDOM(); -- Случайный порядок (PostgreSQL)
```

### LIMIT / OFFSET – Ограничение выборки
```sql
SELECT * FROM table LIMIT 10;
SELECT * FROM table LIMIT 10 OFFSET 5;
SELECT * FROM table FETCH FIRST 10 ROWS ONLY; -- Стандарт SQL:2008
SELECT * FROM table OFFSET 5 ROWS FETCH NEXT 10 ROWS ONLY;
```

### TOP (T-SQL / MS Access)
```sql
SELECT TOP 10 * FROM table;
SELECT TOP 10 PERCENT * FROM table;
```

---

## 3. Агрегатные функции

### Базовые агрегаты
```sql
SELECT COUNT(*) FROM table;
SELECT COUNT(column) FROM table; -- Не считает NULL
SELECT SUM(column) FROM table;
SELECT AVG(column) FROM table;
SELECT MIN(column) FROM table;
SELECT MAX(column) FROM table;
SELECT GROUP_CONCAT(column) FROM table; -- MySQL
SELECT STRING_AGG(column, ',') FROM table; -- PostgreSQL/SQL Server
SELECT LISTAGG(column, ',') WITHIN GROUP (ORDER BY column) FROM table; -- Oracle
```

### GROUP BY – Группировка
```sql
SELECT department, COUNT(*), AVG(salary) 
FROM employees 
GROUP BY department;
```

### HAVING – Фильтрация групп
```sql
SELECT department, COUNT(*) 
FROM employees 
GROUP BY department 
HAVING COUNT(*) > 5;
```

### ROLLUP / CUBE / GROUPING SETS
```sql
SELECT department, role, COUNT(*) 
FROM employees 
GROUP BY ROLLUP(department, role); -- Иерархические итоги

SELECT department, role, COUNT(*) 
FROM employees 
GROUP BY CUBE(department, role); -- Все комбинации

SELECT department, role, COUNT(*) 
FROM employees 
GROUP BY GROUPING SETS ((department), (role), ()); -- Выборочные наборы
```

---

## 4. Объединение таблиц (JOINs)

### INNER JOIN – Внутреннее соединение
```sql
SELECT a.col1, b.col2 
FROM tableA a 
INNER JOIN tableB b ON a.id = b.a_id;
```

### LEFT / RIGHT JOIN – Внешние соединения
```sql
SELECT a.col1, b.col2 
FROM tableA a 
LEFT JOIN tableB b ON a.id = b.a_id; -- Все из A + совпадения из B

SELECT a.col1, b.col2 
FROM tableA a 
RIGHT JOIN tableB b ON a.id = b.a_id; -- Все из B + совпадения из A
```

### FULL OUTER JOIN – Полное внешнее соединение
```sql
SELECT a.col1, b.col2 
FROM tableA a 
FULL OUTER JOIN tableB b ON a.id = b.a_id; -- Все записи из обеих таблиц
```

### CROSS JOIN – Декартово произведение
```sql
SELECT * FROM tableA CROSS JOIN tableB;
-- или
SELECT * FROM tableA, tableB;
```

### SELF JOIN – Соединение таблицы с самой собой
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

## 5. Подзапросы (Subqueries)

### Подзапрос в WHERE
```sql
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products);
```

### Подзапрос в FROM (Derived Table)
```sql
SELECT dept, avg_sal 
FROM (SELECT department AS dept, AVG(salary) AS avg_sal 
      FROM employees GROUP BY department) AS subq
WHERE avg_sal > 50000;
```

### Подзапрос в SELECT
```sql
SELECT name, 
       (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count
FROM users;
```

### EXISTS / NOT EXISTS
```sql
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

### ANY / ALL
```sql
SELECT * FROM products 
WHERE price > ANY (SELECT price FROM products WHERE category = 'A');

SELECT * FROM products 
WHERE price > ALL (SELECT price FROM products WHERE category = 'A');
```

---

## 6. Оконные функции (Window Functions)

### ROW_NUMBER / RANK / DENSE_RANK
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
       RANK() OVER (ORDER BY salary DESC) AS rank_num,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_num
FROM employees;
```

### NTILE – Разделение на группы
```sql
SELECT name, salary,
       NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
```

### LAG / LEAD – Доступ к предыдущей/следующей строке
```sql
SELECT name, salary,
       LAG(salary, 1) OVER (ORDER BY salary) AS prev_salary,
       LEAD(salary, 1) OVER (ORDER BY salary) AS next_salary
FROM employees;
```

### FIRST_VALUE / LAST_VALUE
```sql
SELECT name, department, salary,
       FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_in_dept,
       LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC 
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS lowest_in_dept
FROM employees;
```

### SUM / AVG как оконные функции
```sql
SELECT name, salary,
       SUM(salary) OVER (ORDER BY hire_date) AS running_total,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

---

## 7. Операции с множествами (Set Operations)

### UNION – Объединение без дубликатов
```sql
SELECT city FROM customers
UNION
SELECT city FROM suppliers;
```

### UNION ALL – Объединение с дубликатами
```sql
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;
```

### INTERSECT – Пересечение (общие значения)
```sql
SELECT city FROM customers
INTERSECT
SELECT city FROM suppliers;
```

### EXCEPT / MINUS – Разность множеств
```sql
SELECT city FROM customers
EXCEPT
SELECT city FROM suppliers; -- PostgreSQL/SQL Server

SELECT city FROM customers
MINUS
SELECT city FROM suppliers; -- Oracle
```

---

## 8. Работа со строками

### Конкатенация
```sql
SELECT first_name || ' ' || last_name AS full_name FROM users; -- PostgreSQL/Oracle
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users; -- MySQL/SQL Server
SELECT first_name + ' ' + last_name AS full_name FROM users; -- T-SQL (старый стиль)
```

### Длина и регистр
```sql
SELECT LENGTH(column) FROM table; -- PostgreSQL/Oracle
SELECT CHAR_LENGTH(column) FROM table; -- Стандарт SQL
SELECT LOWER(column) FROM table;
SELECT UPPER(column) FROM table;
SELECT INITCAP(column) FROM table; -- Первая буква заглавная (Oracle/PostgreSQL)
```

### Извлечение подстрок
```sql
SELECT SUBSTRING(column FROM 1 FOR 5) FROM table; -- Стандарт SQL
SELECT SUBSTR(column, 1, 5) FROM table; -- Oracle/MySQL
SELECT SUBSTRING(column, 1, 5) FROM table; -- SQL Server/PostgreSQL
```

### Поиск и замена
```sql
SELECT POSITION('sub' IN column) FROM table; -- Стандарт SQL
SELECT INSTR(column, 'sub') FROM table; -- Oracle/MySQL
SELECT CHARINDEX('sub', column) FROM table; -- SQL Server

SELECT REPLACE(column, 'old', 'new') FROM table;
SELECT TRANSLATE(column, 'abc', 'xyz') FROM table; -- Посимвольная замена
```

### Trim и обрезка
```sql
SELECT TRIM(column) FROM table; -- Удаление пробелов с обоих концов
SELECT LTRIM(column) FROM table; -- Слева
SELECT RTRIM(column) FROM table; -- Справа
SELECT TRIM(BOTH 'x' FROM column) FROM table; -- Удаление конкретных символов
SELECT TRIM(LEADING 'x' FROM column) FROM table;
SELECT TRIM(TRAILING 'x' FROM column) FROM table;
```

---

## 9. Работа с числами

### Округление и усечение
```sql
SELECT ROUND(column, 2) FROM table; -- Округление
SELECT TRUNC(column, 2) FROM table; -- Усечение (PostgreSQL/Oracle)
SELECT FLOOR(column) FROM table; -- Вниз
SELECT CEIL(column) FROM table; -- Вверх (CEILING в SQL Server)
```

### Модуль и степени
```sql
SELECT ABS(column) FROM table; -- Модуль
SELECT POWER(column, 2) FROM table; -- Степень (POW в MySQL)
SELECT SQRT(column) FROM table; -- Квадратный корень
SELECT EXP(column) FROM table; -- Экспонента
SELECT LN(column) FROM table; -- Натуральный логарифм
SELECT LOG10(column) FROM table; -- Логарифм по основанию 10
```

### Остаток от деления
```sql
SELECT MOD(a, b) FROM table; -- PostgreSQL/Oracle/MySQL
SELECT a % b FROM table; -- MySQL/PostgreSQL (оператор)
```

### Генерация случайных чисел
```sql
SELECT RANDOM() FROM table; -- PostgreSQL (0.0 - 1.0)
SELECT RAND() FROM table; -- MySQL/SQL Server
```

---

## 10. Работа с датами и временем

### Текущая дата и время
```sql
SELECT NOW(); -- PostgreSQL/MySQL
SELECT CURRENT_TIMESTAMP; -- Стандарт SQL
SELECT GETDATE(); -- SQL Server
SELECT SYSDATE; -- Oracle
SELECT CURRENT_DATE; -- Только дата
SELECT CURRENT_TIME; -- Только время
```

### Извлечение частей даты
```sql
SELECT EXTRACT(YEAR FROM date_col) FROM table; -- Стандарт SQL
SELECT DATE_PART('year', date_col) FROM table; -- PostgreSQL
SELECT YEAR(date_col) FROM table; -- MySQL/SQL Server
SELECT MONTH(date_col) FROM table;
SELECT DAY(date_col) FROM table;
SELECT HOUR(date_col) FROM table;
SELECT WEEK(date_col) FROM table;
SELECT QUARTER(date_col) FROM table;
SELECT DOW(date_col) FROM table; -- День недели (PostgreSQL)
SELECT DAYOFWEEK(date_col) FROM table; -- MySQL
```

### Форматирование дат
```sql
SELECT TO_CHAR(date_col, 'YYYY-MM-DD HH24:MI:SS') FROM table; -- PostgreSQL/Oracle
SELECT DATE_FORMAT(date_col, '%Y-%m-%d %H:%i:%s') FROM table; -- MySQL
SELECT FORMAT(date_col, 'yyyy-MM-dd HH:mm:ss') FROM table; -- SQL Server
SELECT STRFTIME('%Y-%m-%d', date_col) FROM table; -- SQLite
```

### Арифметика с датами
```sql
SELECT date_col + INTERVAL '1 day' FROM table; -- PostgreSQL
SELECT date_col + INTERVAL 1 DAY FROM table; -- MySQL
SELECT DATEADD(day, 1, date_col) FROM table; -- SQL Server
SELECT date_col + 1 FROM table; -- Oracle (дни)

SELECT age(NOW(), birth_date) FROM table; -- PostgreSQL (разница)
SELECT DATEDIFF(day, start_date, end_date) FROM table; -- SQL Server/MySQL
SELECT MONTHS_BETWEEN(date1, date2) FROM table; -- Oracle
```

### Конструирование дат
```sql
SELECT MAKE_DATE(2023, 12, 25); -- PostgreSQL
SELECT DATE_FROM_PARTS(2023, 12, 25); -- SQL Server
SELECT MAKEDATE(2023, 365); -- MySQL (день года)
SELECT TO_DATE('2023-12-25', 'YYYY-MM-DD'); -- PostgreSQL/Oracle
SELECT STR_TO_DATE('25-12-2023', '%d-%m-%Y'); -- MySQL
```

---

## 11. Работа с NULL

### Проверка на NULL
```sql
SELECT * FROM table WHERE column IS NULL;
SELECT * FROM table WHERE column IS NOT NULL;
```

### Замена NULL
```sql
SELECT COALESCE(column, 'default_value') FROM table; -- Стандарт SQL (возвращает первый не-NULL)
SELECT IFNULL(column, 'default_value') FROM table; -- MySQL
SELECT ISNULL(column, 'default_value') FROM table; -- SQL Server
SELECT NVL(column, 'default_value') FROM table; -- Oracle
SELECT NVL2(column, 'if_not_null', 'if_null') FROM table; -- Oracle
```

### NULL в агрегатах
```sql
-- COUNT(*) считает все строки, COUNT(col) игнорирует NULL
-- SUM, AVG, MIN, MAX игнорируют NULL
-- Если все значения NULL, результат агрегата будет NULL (кроме COUNT)
```

---

## 12. Определение данных (DDL)

### Создание базы данных
```sql
CREATE DATABASE db_name;
CREATE DATABASE db_name WITH ENCODING 'UTF8'; -- PostgreSQL
```

### Удаление базы данных
```sql
DROP DATABASE db_name;
DROP DATABASE IF EXISTS db_name;
```

### Создание таблицы
```sql
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY, -- PostgreSQL (автоинкремент)
    id INT AUTO_INCREMENT PRIMARY KEY, -- MySQL
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    age INT CHECK (age >= 0),
    salary DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);
```

### Изменение таблицы
```sql
ALTER TABLE table_name ADD column_name datatype;
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type;
ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT value;
ALTER TABLE table_name ALTER COLUMN column_name DROP DEFAULT;
ALTER TABLE table_name ADD CONSTRAINT constraint_name UNIQUE (column);
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
ALTER TABLE table_name RENAME TO new_table_name;
```

### Удаление таблицы
```sql
DROP TABLE table_name;
DROP TABLE IF EXISTS table_name;
TRUNCATE TABLE table_name; -- Быстрая очистка
```

### Создание индекса
```sql
CREATE INDEX idx_name ON table_name (column);
CREATE UNIQUE INDEX idx_unique ON table_name (column);
CREATE INDEX idx_multi ON table_name (col1, col2);
CREATE INDEX idx_expr ON table_name (LOWER(name)); -- Функциональный индекс
CREATE INDEX idx_partial ON table_name (column) WHERE condition; -- Частичный индекс (PostgreSQL)
```

### Удаление индекса
```sql
DROP INDEX idx_name;
DROP INDEX IF EXISTS idx_name;
```

### Создание представления (View)
```sql
CREATE VIEW view_name AS
SELECT col1, col2 FROM table WHERE condition;

CREATE OR REPLACE VIEW view_name AS ...; -- PostgreSQL/Oracle
```

### Удаление представления
```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

---

## 13. Ограничения целостности (Constraints)

### PRIMARY KEY – Первичный ключ
```sql
CREATE TABLE t (id INT PRIMARY KEY, name VARCHAR(50));
-- или
CREATE TABLE t (id INT, name VARCHAR(50), CONSTRAINT pk_t PRIMARY KEY (id));
```

### FOREIGN KEY – Внешний ключ
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
-- Варианты ON DELETE: CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION
```

### UNIQUE – Уникальность
```sql
CREATE TABLE t (email VARCHAR(100) UNIQUE);
-- или
CONSTRAINT uniq_email UNIQUE (email)
```

### CHECK – Проверка условия
```sql
CREATE TABLE t (
    age INT CHECK (age >= 0),
    price DECIMAL CHECK (price > 0),
    status VARCHAR(10) CHECK (status IN ('active', 'inactive'))
);
```

### NOT NULL – Обязательное поле
```sql
CREATE TABLE t (name VARCHAR(50) NOT NULL);
```

### DEFAULT – Значение по умолчанию
```sql
CREATE TABLE t (created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
```

---

## 14. Управление транзакциями (TCL)

### Начало и завершение транзакции
```sql
BEGIN; -- или BEGIN TRANSACTION;
COMMIT; -- Фиксация изменений
ROLLBACK; -- Откат изменений
```

### Точки сохранения (Savepoints)
```sql
BEGIN;
INSERT INTO t VALUES (1);
SAVEPOINT sp1;
INSERT INTO t VALUES (2);
ROLLBACK TO sp1; -- Откат до точки сохранения
COMMIT;
```

### Уровень изоляции транзакций
```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

### Автокоммит
```sql
-- Включение/выключение автокоммита зависит от клиента
-- В psql: \autocommit on/off
-- В JDBC: connection.setAutoCommit(false);
```

---

## 15. Управление доступом (DCL)

### Предоставление прав (GRANT)
```sql
GRANT SELECT ON table_name TO user_name;
GRANT INSERT, UPDATE, DELETE ON table_name TO user_name;
GRANT ALL PRIVILEGES ON table_name TO user_name;
GRANT USAGE ON SCHEMA schema_name TO user_name;
GRANT CREATE ON DATABASE db_name TO user_name;
GRANT role_name TO user_name; -- Предоставление роли
```

### Отзыв прав (REVOKE)
```sql
REVOKE SELECT ON table_name FROM user_name;
REVOKE ALL PRIVILEGES ON table_name FROM user_name;
REVOKE role_name FROM user_name;
```

### Просмотр прав
```sql
-- PostgreSQL
\dp table_name -- в psql
SELECT * FROM information_schema.role_table_grants;

-- MySQL
SHOW GRANTS FOR user_name;

-- SQL Server
EXEC sp_helprotect;
```

### Создание пользователя и роли
```sql
CREATE USER user_name WITH PASSWORD 'password'; -- PostgreSQL
CREATE USER 'user_name'@'localhost' IDENTIFIED BY 'password'; -- MySQL
CREATE LOGIN login_name WITH PASSWORD = 'password'; -- SQL Server

CREATE ROLE role_name; -- PostgreSQL
```

### Удаление пользователя
```sql
DROP USER user_name;
DROP USER IF EXISTS user_name;
```

---

## 16. Хранимые процедуры и функции

### Создание функции (PostgreSQL пример)
```sql
CREATE OR REPLACE FUNCTION get_employee_salary(emp_id INT)
RETURNS DECIMAL AS $$
DECLARE
    sal DECIMAL;
BEGIN
    SELECT salary INTO sal FROM employees WHERE id = emp_id;
    RETURN sal;
END;
$$ LANGUAGE plpgsql;

-- Вызов
SELECT get_employee_salary(123);
```

### Создание хранимой процедуры (MySQL пример)
```sql
DELIMITER //
CREATE PROCEDURE get_employee_info(IN emp_id INT)
BEGIN
    SELECT * FROM employees WHERE id = emp_id;
END //
DELIMITER ;

-- Вызов
CALL get_employee_info(123);
```

### Создание функции (T-SQL / SQL Server)
```sql
CREATE FUNCTION dbo.CalculateTax(@salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @tax DECIMAL(10,2);
    SET @tax = @salary * 0.13;
    RETURN @tax;
END;

-- Вызов
SELECT dbo.CalculateTax(100000);
```

### Удаление функций и процедур
```sql
DROP FUNCTION IF EXISTS function_name;
DROP PROCEDURE IF EXISTS procedure_name;
```

---

## 17. Триггеры (Triggers)

### Создание триггера (PostgreSQL)
```sql
CREATE OR REPLACE FUNCTION log_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, old_val, new_val, changed_at)
    VALUES (TG_TABLE_NAME, TG_OP, OLD.id, NEW.id, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_employee_update
AFTER UPDATE ON employees
FOR EACH ROW EXECUTE FUNCTION log_update();
```

### Создание триггера (MySQL)
```sql
DELIMITER //
CREATE TRIGGER before_insert_employee
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    SET NEW.created_at = NOW();
END //
DELIMITER ;
```

### Типы триггеров
-- BEFORE INSERT / UPDATE / DELETE
-- AFTER INSERT / UPDATE / DELETE
-- INSTEAD OF (для представлений в SQL Server)

### Удаление триггера
```sql
DROP TRIGGER IF EXISTS trigger_name;
```

---

## 18. Рекурсивные запросы (CTE)

### Базовый CTE (Common Table Expression)
```sql
WITH dept_summary AS (
    SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_sal
    FROM employees
    GROUP BY department
)
SELECT * FROM dept_summary WHERE emp_count > 5;
```

### Рекурсивный CTE (иерархии)
```sql
WITH RECURSIVE org_chart AS (
    -- Якорный член (корень)
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Рекурсивный член
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

### Несколько CTE
```sql
WITH 
cte1 AS (SELECT ...),
cte2 AS (SELECT ... FROM cte1),
cte3 AS (SELECT ... FROM cte2)
SELECT * FROM cte3;
```

---

## 19. Продвинутые возможности

### PIVOT / UNPIVOT (поворот таблицы)
```sql
-- SQL Server пример PIVOT
SELECT * FROM (
    SELECT product, year, sales FROM sales_data
) AS src
PIVOT (
    SUM(sales) FOR year IN ([2020], [2021], [2022])
) AS pvt;

-- PostgreSQL требует использование FILTER или CASE
SELECT product,
       SUM(CASE WHEN year = 2020 THEN sales ELSE 0 END) AS y2020,
       SUM(CASE WHEN year = 2021 THEN sales ELSE 0 END) AS y2021
FROM sales_data
GROUP BY product;
```

### JSON работа (PostgreSQL)
```sql
-- Доступ к полям JSON
SELECT data->>'name' FROM users; -- Как текст
SELECT data->'address' FROM users; -- Как JSON

-- Проверка наличия ключа
SELECT * FROM users WHERE data ? 'email';

-- Агрегация в JSON
SELECT json_agg(t) FROM (SELECT * FROM employees) t;
SELECT json_object_agg(name, salary) FROM employees;
```

### JSON работа (MySQL)
```sql
SELECT JSON_EXTRACT(data, '$.name') FROM users;
SELECT data->'$.name' FROM users; -- Краткая запись
SELECT JSON_VALID(data) FROM users;
```

### Полнотекстовый поиск (PostgreSQL)
```sql
-- Поиск
SELECT * FROM documents 
WHERE to_tsvector('russian', content) @@ to_tsquery('russian', 'ключ & слово');

-- Ранжирование
SELECT title, ts_rank(to_tsvector(content), query) AS rank
FROM documents, to_tsquery('ключ') query
WHERE to_tsvector(content) @@ query
ORDER BY rank DESC;
```

### Материализованные представления
```sql
-- Создание
CREATE MATERIALIZED VIEW mv_sales AS
SELECT region, SUM(amount) as total FROM sales GROUP BY region;

-- Обновление
REFRESH MATERIALIZED VIEW mv_sales;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales; -- Без блокировки чтения (PostgreSQL)
```

---

## 20. Оптимизация и анализ запросов

### EXPLAIN – План выполнения
```sql
EXPLAIN SELECT * FROM table WHERE condition;
EXPLAIN ANALYZE SELECT * FROM table WHERE condition; -- С выполнением (PostgreSQL)
EXPLAIN PLAN FOR SELECT * FROM table; -- Oracle
```

### Индексация стратегий
-- B-Tree: для равенства, диапазонов, сортировки (по умолчанию)
-- Hash: только для равенства
-- GiST/GIN: для полнотекстового поиска, массивов, JSON (PostgreSQL)
-- BRIN: для больших таблиц с естественным порядком

### Статистика
```sql
ANALYZE table_name; -- Сбор статистики (PostgreSQL/MySQL)
UPDATE STATISTICS table_name; -- SQL Server
```

### Советы по оптимизации
-- Использовать конкретные колонны вместо SELECT *
-- Избегать функций в WHERE (ломает использование индексов)
-- Использовать EXISTS вместо IN для больших подзапросов
-- Избегать SELECT DISTINCT если возможно
-- Использовать UNION ALL вместо UNION если дубликаты не важны
-- Правильно выбирать типы данных
-- Регулярно делать VACUUM (PostgreSQL) или OPTIMIZE TABLE (MySQL)

---

## Заключение

Эта шпаргалка охватывает основные и продвинутые команды SQL, используемые в повседневной работе разработчиков и администраторов баз данных. Для печати рекомендуется формат A4.

**Версия:** 1.0.4  
**Дата обновления:** 2024  
**Форматирование:** Arial, заголовки 12pt, подзаголовки 11pt, текст 10pt
