# Полная шпаргалка по SQL

## 1. ОСНОВНЫЕ ОПЕРАТОРЫ (DML)

### SELECT – Выборка данных
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name;
SELECT DISTINCT column FROM table_name;
SELECT column AS alias FROM table_name;

### WHERE – Фильтрация
SELECT * FROM table WHERE column = value;
SELECT * FROM table WHERE column > 100;
SELECT * FROM table WHERE column BETWEEN 10 AND 20;
SELECT * FROM table WHERE column IN (val1, val2);
SELECT * FROM table WHERE column LIKE 'pattern%';
SELECT * FROM table WHERE column IS NULL;
SELECT * FROM table WHERE column IS NOT NULL;

### INSERT – Вставка данных
INSERT INTO table (col1, col2) VALUES (val1, val2);
INSERT INTO table SELECT * FROM other_table;

### UPDATE – Обновление данных
UPDATE table SET col1 = val1 WHERE condition;
UPDATE table SET col1 = val1, col2 = val2 WHERE condition;

### DELETE – Удаление данных
DELETE FROM table WHERE condition;
DELETE FROM table; -- Удаляет все строки

---

## 2. СОРТИРОВКА И ОГРАНИЧЕНИЕ

### ORDER BY – Сортировка
SELECT * FROM table ORDER BY column ASC;
SELECT * FROM table ORDER BY column DESC;
SELECT * FROM table ORDER BY col1 ASC, col2 DESC;

### LIMIT / OFFSET – Ограничение выборки
SELECT * FROM table LIMIT 10;
SELECT * FROM table LIMIT 10 OFFSET 5;
SELECT * FROM table FETCH FIRST 10 ROWS ONLY; -- Стандарт SQL

### TOP (T-SQL)
SELECT TOP 10 * FROM table;

---

## 3. АГРЕГАТНЫЕ ФУНКЦИИ

### Основные функции
COUNT(column) – Количество строк
SUM(column) – Сумма значений
AVG(column) – Среднее значение
MIN(column) – Минимальное значение
MAX(column) – Максимальное значение

### Примеры использования
SELECT COUNT(*) FROM table;
SELECT SUM(salary) FROM employees;
SELECT AVG(price), MIN(price), MAX(price) FROM products;

### GROUP BY – Группировка
SELECT department, COUNT(*) FROM employees GROUP BY department;
SELECT department, AVG(salary) FROM employees GROUP BY department;

### HAVING – Фильтрация групп
SELECT department, COUNT(*) FROM employees 
GROUP BY department 
HAVING COUNT(*) > 5;

---

## 4. СОЕДИНЕНИЕ ТАБЛИЦ (JOINS)

### INNER JOIN – Внутреннее соединение
SELECT a.col, b.col 
FROM table_a a 
INNER JOIN table_b b ON a.id = b.a_id;

### LEFT JOIN – Левое соединение
SELECT a.col, b.col 
FROM table_a a 
LEFT JOIN table_b b ON a.id = b.a_id;

### RIGHT JOIN – Правое соединение
SELECT a.col, b.col 
FROM table_a a 
RIGHT JOIN table_b b ON a.id = b.a_id;

### FULL OUTER JOIN – Полное соединение
SELECT a.col, b.col 
FROM table_a a 
FULL OUTER JOIN table_b b ON a.id = b.a_id;

### CROSS JOIN – Декартово произведение
SELECT * FROM table_a CROSS JOIN table_b;

### SELF JOIN – Соединение с самим собой
SELECT a.name, b.name 
FROM employees a, employees b 
WHERE a.manager_id = b.id;

---

## 5. ПОДЗАПРОСЫ (SUBQUERIES)

### Подзапрос в WHERE
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products);

### Подзапрос в FROM
SELECT dept, avg_sal 
FROM (SELECT department AS dept, AVG(salary) AS avg_sal FROM employees GROUP BY department) AS sub;

### Подзапрос в SELECT
SELECT name, (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count 
FROM users;

### EXISTS / NOT EXISTS
SELECT * FROM departments d 
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);

---

## 6. ОПЕРАЦИИ МНОЖЕСТВ

### UNION – Объединение (без дубликатов)
SELECT col FROM table1 
UNION 
SELECT col FROM table2;

### UNION ALL – Объединение (с дубликатами)
SELECT col FROM table1 
UNION ALL 
SELECT col FROM table2;

### INTERSECT – Пересечение
SELECT col FROM table1 
INTERSECT 
SELECT col FROM table2;

### EXCEPT / MINUS – Разность
SELECT col FROM table1 
EXCEPT 
SELECT col FROM table2;

---

## 7. ОПРЕДЕЛЕНИЕ ДАННЫХ (DDL)

### CREATE TABLE – Создание таблицы
CREATE TABLE table_name (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### ALTER TABLE – Изменение таблицы
ALTER TABLE table ADD column datatype;
ALTER TABLE table DROP COLUMN column;
ALTER TABLE table MODIFY COLUMN column datatype;
ALTER TABLE table RENAME COLUMN old TO new;
ALTER TABLE table ADD CONSTRAINT pk PRIMARY KEY (id);

### DROP TABLE – Удаление таблицы
DROP TABLE table_name;
DROP TABLE IF EXISTS table_name;

### TRUNCATE TABLE – Очистка таблицы
TRUNCATE TABLE table_name;

### CREATE INDEX – Создание индекса
CREATE INDEX idx_name ON table(column);
CREATE UNIQUE INDEX idx_unique ON table(column);

### DROP INDEX – Удаление индекса
DROP INDEX idx_name ON table;

---

## 8. ОГРАНИЧЕНИЯ (CONSTRAINTS)

### PRIMARY KEY – Первичный ключ
CREATE TABLE t (id INT PRIMARY KEY);

### FOREIGN KEY – Внешний ключ
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

### UNIQUE – Уникальность
CREATE TABLE t (email VARCHAR(100) UNIQUE);

### NOT NULL – Не пустое значение
CREATE TABLE t (name VARCHAR(100) NOT NULL);

### CHECK – Проверка условия
CREATE TABLE t (age INT CHECK (age >= 18));

### DEFAULT – Значение по умолчанию
CREATE TABLE t (status VARCHAR(20) DEFAULT 'active');

---

## 9. РАБОТА СО СТРОКАМИ И ЧИСЛАМИ

### Строковые функции
UPPER(str), LOWER(str) – Регистр
LENGTH(str), CHAR_LENGTH(str) – Длина
SUBSTRING(str, start, len) – Подстрока
TRIM(str), LTRIM(str), RTRIM(str) – Удаление пробелов
CONCAT(str1, str2) – Конкатенация
REPLACE(str, from, to) – Замена
INSTR(str, substr) – Позиция подстроки

### Числовые функции
ROUND(num, decimals) – Округление
CEIL(num), FLOOR(num) – Округление вверх/вниз
ABS(num) – Модуль
POWER(num, exp) – Степень
SQRT(num) – Квадратный корень
MOD(a, b) – Остаток от деления

### Дата и время
NOW(), CURRENT_DATE, CURRENT_TIME
DATE_ADD(date, INTERVAL val unit)
DATE_SUB(date, INTERVAL val unit)
DATEDIFF(date1, date2)
EXTRACT(YEAR FROM date)
DATE_FORMAT(date, format)

---

## 10. ПРОЦЕДУРНЫЙ SQL (T-SQL / PLSQL)

### Переменные
DECLARE @var INT = 10;
SET @var = 20;

### Условия IF
IF condition BEGIN
    -- действия
END ELSE BEGIN
    -- действия
END

### Циклы WHILE
WHILE condition BEGIN
    -- действия
END

### Хранимые процедуры
CREATE PROCEDURE proc_name @param INT AS BEGIN
    SELECT * FROM table WHERE id = @param;
END;

EXEC proc_name 123;

### Функции
CREATE FUNCTION func_name(@param INT) RETURNS INT AS BEGIN
    RETURN @param * 2;
END;

### Триггеры
CREATE TRIGGER trg_name AFTER INSERT ON table FOR EACH ROW BEGIN
    -- действия
END;

---

## 11. ОКНА И АНАЛИТИЧЕСКИЕ ФУНКЦИИ

### ROW_NUMBER() – Нумерация строк
SELECT name, ROW_NUMBER() OVER (ORDER BY salary) AS rn FROM employees;

### RANK() / DENSE_RANK() – Ранжирование
SELECT name, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees;
SELECT name, DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk FROM employees;

### NTILE() – Распределение по группам
SELECT name, NTILE(4) OVER (ORDER BY salary) AS quartile FROM employees;

### LAG() / LEAD() – Доступ к соседним строкам
SELECT name, salary, LAG(salary) OVER (ORDER BY salary) AS prev_sal FROM employees;
SELECT name, salary, LEAD(salary) OVER (ORDER BY salary) AS next_sal FROM employees;

### SUM() / AVG() OVER – Скользящие агрегаты
SELECT date, sales, SUM(sales) OVER (ORDER BY date) AS running_total FROM sales;

### PARTITION BY – Разбиение на группы
SELECT dept, name, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn FROM employees;

---

## 12. ТРАНЗАКЦИИ И БЛОКИРОВКИ

### Управление транзакциями
BEGIN TRANSACTION;
COMMIT;
ROLLBACK;
SAVEPOINT sp_name;
ROLLBACK TO sp_name;

### Уровни изоляции
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

---

## 13. ПРЕДСТАВЛЕНИЯ (VIEWS)

### Создание представления
CREATE VIEW view_name AS SELECT col1, col2 FROM table WHERE condition;

### Использование
SELECT * FROM view_name;

### Обновляемое представление
CREATE OR REPLACE VIEW view_name AS SELECT ...;

### Удаление
DROP VIEW view_name;

---

## 14. ИНДЕКСЫ И ОПТИМИЗАЦИЯ

### Типы индексов
- B-Tree (стандартный)
- Hash (для точных совпадений)
- Full-Text (для полнотекстового поиска)
- Composite (составной индекс)
- Covering (покрывающий индекс)

### Анализ запросов
EXPLAIN SELECT * FROM table WHERE ...;
EXPLAIN ANALYZE SELECT * FROM table WHERE ...;

### Оптимизация
- Избегать SELECT *
- Использовать индексы для WHERE и JOIN
- Избегать функций в WHERE (теряется индекс)
- Использовать EXISTS вместо IN для больших наборов
- Избегать LIKE '%pattern'

---

## 15. БЕЗОПАСНОСТЬ И ДОСТУП

### Пользователи и роли
CREATE USER username WITH PASSWORD 'password';
GRANT SELECT, INSERT ON table TO username;
REVOKE INSERT ON table FROM username;
DROP USER username;

### Роли
CREATE ROLE role_name;
GRANT role_name TO username;

### Привилегии
GRANT ALL PRIVILEGES ON DATABASE db TO user;
GRANT EXECUTE ON PROCEDURE proc TO user;

---

## 16. РАЗЛИЧИЯ СУБД (СИНТАКСИС)

### LIMIT vs TOP vs FETCH
MySQL/PostgreSQL: LIMIT 10
SQL Server: TOP 10
Oracle/Standard: FETCH FIRST 10 ROWS ONLY

### Автоинкремент
MySQL: AUTO_INCREMENT
PostgreSQL: SERIAL / GENERATED ALWAYS AS IDENTITY
SQL Server: IDENTITY(1,1)
Oracle: SEQUENCE

### Кавычки
MySQL: `table` (обратные), "string"
PostgreSQL: "table" (двойные), 'string'
SQL Server: [table] (квадратные), 'string'
Oracle: "table", 'string'

### Конкатенация
Standard: CONCAT(a, b) или a || b
MySQL: CONCAT(a, b)
SQL Server: a + b
Oracle: a || b

---

## 17. РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ (REGEXP)

### PostgreSQL / MySQL
SELECT * FROM table WHERE column ~ 'pattern';
SELECT * FROM table WHERE column REGEXP '^[0-9]+$';

### Паттерны
^ – Начало строки
$ – Конец строки
. – Любой символ
* – 0 или более повторений
+ – 1 или более повторений
? – 0 или 1 повторение
[abc] – Один из символов
[^abc] – Любой кроме
\d – Цифра
\w – Слово
\s – Пробел

---

## 18. JSON В SQL

### PostgreSQL
SELECT data->>'key' FROM table;
SELECT * FROM table WHERE data @> '{"key": "value"}';

### MySQL
SELECT JSON_EXTRACT(data, '$.key') FROM table;
SELECT data->'$.key' FROM table;

### SQL Server
SELECT data.value('$.key', 'VARCHAR(100)') FROM table;

### Oracle
SELECT json_value(data, '$.key') FROM table;

---

## 19. РЕКУРСИВНЫЕ ЗАПРОСЫ (CTE)

### WITH Clause
WITH RECURSIVE cte AS (
    SELECT id, parent_id, 1 AS level FROM tree WHERE parent_id IS NULL
    UNION ALL
    SELECT t.id, t.parent_id, c.level + 1 
    FROM tree t JOIN cte c ON t.parent_id = c.id
)
SELECT * FROM cte;

---

## 20. ПИВОТ И УНПИВОТ

### PIVOT (SQL Server)
SELECT * FROM (
    SELECT year, product, amount FROM sales
) AS src
PIVOT (SUM(amount) FOR product IN ([A], [B], [C])) AS pvt;

### UNPIVOT
SELECT * FROM table
UNPIVOT (value FOR product IN (colA, colB, colC)) AS unpvt;

### CASE для Pivot (универсальный)
SELECT year,
    SUM(CASE WHEN product = 'A' THEN amount END) AS A,
    SUM(CASE WHEN product = 'B' THEN amount END) AS B
FROM sales GROUP BY year;
