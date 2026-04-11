# Шпаргалка по MySQL

Полный справочник команд и особенностей MySQL для быстрого поиска.

## Типы данных MySQL

### Числовые типы

| Тип | Размер | Диапазон | Описание |
|-----|--------|----------|----------|
| `TINYINT` | 1 байт | -128 to 127 | Малое целое |
| `SMALLINT` | 2 байта | -32,768 to 32,767 | Малое целое |
| `MEDIUMINT` | 3 байта | -8,388,608 to 8,388,607 | Среднее целое |
| `INT` | 4 байта | -2,147,483,648 to 2,147,483,647 | Целое |
| `BIGINT` | 8 байтов | Очень большой диапазон | Большое целое |
| `FLOAT` | 4 байта | ~7 знаков | Число с плавающей точкой |
| `DOUBLE` | 8 байтов | ~15 знаков | Число с плавающей точкой |
| `DECIMAL(M,D)` | Зависит | Точное значение | Точное число |

### Строковые типы

| Тип | Описание | Макс размер |
|-----|----------|-------------|
| `CHAR(N)` | Фиксированная длина | 255 символов |
| `VARCHAR(N)` | Переменная длина | 65,535 байт |
| `TINYTEXT` | Короткий текст | 255 байт |
| `TEXT` | Текст | 65,535 байт |
| `MEDIUMTEXT` | Средний текст | 16,777,215 байт |
| `LONGTEXT` | Длинный текст | 4,294,967,295 байт |
| `ENUM` | Перечисление | 65,535 значений |
| `SET` | Множество | 64 значения |

### Типы даты и времени

| Тип | Формат | Диапазон |
|-----|--------|----------|
| `DATE` | YYYY-MM-DD | 1000-01-01 to 9999-12-31 |
| `DATETIME` | YYYY-MM-DD HH:MM:SS | 1000-01-01 00:00:00 to 9999-12-31 23:59:59 |
| `TIMESTAMP` | YYYY-MM-DD HH:MM:SS | 1970-01-01 to 2038-01-19 |
| `TIME` | HH:MM:SS | -838:59:59 to 838:59:59 |
| `YEAR` | YYYY | 1901 to 2155 |

### JSON тип

```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    attributes JSON
);

-- Вставка JSON
INSERT INTO products VALUES (1, '{"color": "red", "size": "L"}');

--查询JSON
SELECT attributes->'$.color' FROM products WHERE id = 1;
```

## Специфичные команды MySQL

### Управление базами данных

```sql
-- Создание БД с кодировкой
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Просмотр создания БД
SHOW CREATE DATABASE mydb;

-- Выбор БД
USE mydb;
```

### Управление таблицами

```sql
-- Создание таблицы с опциями движка
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Изменение движка
ALTER TABLE users ENGINE=MyISAM;

-- Оптимизация таблицы
OPTIMIZE TABLE users;

-- Анализ таблицы
ANALYZE TABLE users;

-- Проверка таблицы
CHECK TABLE users;

-- Восстановление таблицы
REPAIR TABLE users;
```

### Работа с пользователями и привилегиями

```sql
-- Создание пользователя с хостом
CREATE USER 'app'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'app'@'%' IDENTIFIED BY 'password';  -- Любой хост

-- Предоставление прав
GRANT SELECT, INSERT, UPDATE ON db.* TO 'app'@'localhost';
GRANT ALL PRIVILEGES ON db.* TO 'admin'@'localhost' WITH GRANT OPTION;

-- Отзыв прав
REVOKE DELETE ON db.* FROM 'app'@'localhost';

-- Просмотр прав
SHOW GRANTS FOR 'app'@'localhost';

-- Переименование пользователя
RENAME USER 'olduser'@'localhost' TO 'newuser'@'localhost';

-- Удаление пользователя
DROP USER 'app'@'localhost';

-- Применение изменений
FLUSH PRIVILEGES;
```

### Репликация

```sql
-- Настройка мастера
CHANGE MASTER TO
    MASTER_HOST='master_host',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='repl_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=107;

-- Запуск репликации
START SLAVE;
STOP SLAVE;

-- Проверка статуса
SHOW SLAVE STATUS\G

-- Сброс репликации
RESET SLAVE ALL;
```

## Функции MySQL

### Строковые функции

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `CONCAT(a,b)` | Конкатенация | `CONCAT('Hello', ' ', 'World')` | `'Hello World'` |
| `SUBSTRING(str, pos, len)` | Подстрока | `SUBSTRING('MySQL', 1, 3)` | `'MyS'` |
| `LENGTH(str)` | Длина в байтах | `LENGTH('привет')` | `12` |
| `CHAR_LENGTH(str)` | Длина в символах | `CHAR_LENGTH('привет')` | `6` |
| `UPPER(str)` | Верхний регистр | `UPPER('mysql')` | `'MYSQL'` |
| `LOWER(str)` | Нижний регистр | `LOWER('MYSQL')` | `'mysql'` |
| `TRIM(str)` | Удаление пробелов | `TRIM('  test  ')` | `'test'` |
| `REPLACE(str, from, to)` | Замена | `REPLACE('aabb', 'a', 'x')` | `'xxbb'` |
| `INSTR(str, substr)` | Позиция подстроки | `INSTR('hello', 'll')` | `3` |
| `LPAD(str, len, pad)` | Левое дополнение | `LPAD('5', 3, '0')` | `'005'` |
| `RPAD(str, len, pad)` | Правое дополнение | `RPAD('5', 3, '0')` | `'500'` |
| `GROUP_CONCAT()` | Групповая конкатенация | `GROUP_CONCAT(name SEPARATOR ', ')` | `'A, B, C'` |

### Числовые функции

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `ABS(x)` | Модуль | `ABS(-5)` | `5` |
| `CEIL(x)` | Округление вверх | `CEIL(4.2)` | `5` |
| `FLOOR(x)` | Округление вниз | `FLOOR(4.8)` | `4` |
| `ROUND(x, d)` | Округление | `ROUND(4.567, 2)` | `4.57` |
| `TRUNCATE(x, d)` | Отсечение | `TRUNCATE(4.567, 2)` | `4.56` |
| `MOD(a, b)` | Остаток | `MOD(10, 3)` | `1` |
| `RAND()` | Случайное число | `RAND()` | `0.xxxxx` |
| `POW(x, y)` | Степень | `POW(2, 3)` | `8` |
| `SQRT(x)` | Квадратный корень | `SQRT(16)` | `4` |

### Функции даты и времени

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `NOW()` | Текущие дата и время | `NOW()` | `'2024-01-15 10:30:00'` |
| `CURDATE()` | Текущая дата | `CURDATE()` | `'2024-01-15'` |
| `CURTIME()` | Текущее время | `CURTIME()` | `'10:30:00'` |
| `DATE_ADD(date, INTERVAL)` | Добавление | `DATE_ADD(NOW(), INTERVAL 1 DAY)` | `+1 день` |
| `DATE_SUB(date, INTERVAL)` | Вычитание | `DATE_SUB(NOW(), INTERVAL 1 MONTH)` | `-1 месяц` |
| `DATEDIFF(d1, d2)` | Разница в днях | `DATEDIFF('2024-01-20', '2024-01-15')` | `5` |
| `TIMEDIFF(t1, t2)` | Разница во времени | `TIMEDIFF('10:30', '09:00')` | `'01:30:00'` |
| `DATE_FORMAT(date, fmt)` | Форматирование | `DATE_FORMAT(NOW(), '%d/%m/%Y')` | `'15/01/2024'` |
| `STR_TO_DATE(str, fmt)` | Парсинг даты | `STR_TO_DATE('15/01/2024', '%d/%m/%Y')` | `DATE` |
| `YEAR(date)` | Год | `YEAR(NOW())` | `2024` |
| `MONTH(date)` | Месяц | `MONTH(NOW())` | `1` |
| `DAY(date)` | День | `DAY(NOW())` | `15` |
| `WEEKDAY(date)` | День недели (0-6) | `WEEKDAY(NOW())` | `0-6` |
| `LAST_DAY(date)` | Последний день месяца | `LAST_DAY('2024-02-01')` | `'2024-02-29'` |

**Форматы даты:**
- `%Y` — год (4 цифры)
- `%y` — год (2 цифры)
- `%m` — месяц (01-12)
- `%d` — день (01-31)
- `%H` — часы (00-23)
- `%i` — минуты (00-59)
- `%s` — секунды (00-59)
- `%W` — день недели (полный)
- `%a` — день недели (сокращённый)

### Агрегатные функции

| Функция | Описание |
|---------|----------|
| `COUNT(*)` | Количество строк |
| `COUNT(column)` | Количество непустых значений |
| `SUM(column)` | Сумма |
| `AVG(column)` | Среднее |
| `MIN(column)` | Минимум |
| `MAX(column)` | Максимум |
| `GROUP_CONCAT(column)` | Конкатенация значений группы |

### Оконные функции (MySQL 8.0+)

```sql
-- ROW_NUMBER
SELECT name, score, ROW_NUMBER() OVER (ORDER BY score DESC) as rank
FROM students;

-- RANK и DENSE_RANK
SELECT name, score, 
       RANK() OVER (ORDER BY score DESC) as rank,
       DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;

-- LAG и LEAD
SELECT date, value,
       LAG(value, 1) OVER (ORDER BY date) as prev_value,
       LEAD(value, 1) OVER (ORDER BY date) as next_value
FROM metrics;

-- Накопительная сумма
SELECT date, sales,
       SUM(sales) OVER (ORDER BY date) as running_total
FROM daily_sales;

-- Partition By
SELECT department, employee, salary,
       AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

## Управление транзакциями

```sql
-- Начало транзакции
START TRANSACTION;
BEGIN;

-- Точки сохранения
SAVEPOINT sp1;

-- Откат до точки сохранения
ROLLBACK TO sp1;

-- Полный откат
ROLLBACK;

-- Фиксация
COMMIT;

-- Установка уровня изоляции
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Переменные

```sql
-- Пользовательские переменные
SET @var = 10;
SELECT @var;

-- Использование в запросе
SELECT @counter := @counter + 1 as row_num, name
FROM users, (SELECT @counter := 0) as init;

-- Системные переменные
SHOW VARIABLES LIKE 'max_connections';
SET GLOBAL max_connections = 200;
SET SESSION sql_mode = 'STRICT_TRANS_TABLES';
```

## EXPLAIN и оптимизация

```sql
-- Анализ плана выполнения
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Расширенный анализ
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Ключевые поля EXPLAIN:
-- id: идентификатор шага
-- select_type: тип SELECT
-- table: таблица
-- type: тип соединения (ALL, index, range, ref, eq_ref, const, system)
-- possible_keys: возможные индексы
-- key: используемый индекс
-- rows: оценочное количество строк
-- Extra: дополнительная информация
```

**Типы соединений (от худшего к лучшему):**
- `ALL` — полное сканирование таблицы
- `index` — сканирование индекса
- `range` — диапазон по индексу
- `ref` — поиск по не уникальному индексу
- `eq_ref` — поиск по уникальному индексу
- `const` — константное значение
- `system` — системная таблица

## Полезные системные таблицы

```sql
-- Информация о процессах
SHOW PROCESSLIST;
SELECT * FROM information_schema.PROCESSLIST;

-- Статус сервера
SHOW STATUS;
SHOW STATUS LIKE 'Threads_connected';

-- Переменные сервера
SHOW VARIABLES;
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Информация о базах данных
SELECT * FROM information_schema.SCHEMATA;

-- Информация о таблицах
SELECT * FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'mydb';

-- Информация о колонках
SELECT * FROM information_schema.COLUMNS 
WHERE TABLE_NAME = 'users';

-- Индексы
SHOW INDEX FROM users;
SELECT * FROM information_schema.STATISTICS 
WHERE TABLE_NAME = 'users';

-- Внешние ключи
SELECT * FROM information_schema.KEY_COLUMN_USAGE 
WHERE REFERENCED_TABLE_NAME IS NOT NULL;
```

## Хранимые процедуры и функции

```sql
-- Создание процедуры
DELIMITER $$
CREATE PROCEDURE get_user(IN user_id INT)
BEGIN
    SELECT * FROM users WHERE id = user_id;
END$$
DELIMITER ;

-- Вызов процедуры
CALL get_user(1);

-- Процедура с OUT параметром
DELIMITER $$
CREATE PROCEDURE get_user_count(OUT count INT)
BEGIN
    SELECT COUNT(*) INTO count FROM users;
END$$
DELIMITER ;

CALL get_user_count(@cnt);
SELECT @cnt;

-- Создание функции
DELIMITER $$
CREATE FUNCTION get_full_name(first VARCHAR(50), last VARCHAR(50))
RETURNS VARCHAR(101)
DETERMINISTIC
BEGIN
    RETURN CONCAT(first, ' ', last);
END$$
DELIMITER ;

SELECT get_full_name('John', 'Doe');

-- Удаление
DROP PROCEDURE IF EXISTS get_user;
DROP FUNCTION IF EXISTS get_full_name;
```

## Триггеры

```sql
-- Создание триггера
DELIMITER $$
CREATE TRIGGER before_user_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.created_at = NOW();
    SET NEW.username = LOWER(NEW.username);
END$$
DELIMITER ;

-- Типы триггеров: BEFORE/AFTER INSERT/UPDATE/DELETE

-- Просмотр триггеров
SHOW TRIGGERS;
SELECT * FROM information_schema.TRIGGERS;

-- Удаление триггера
DROP TRIGGER IF EXISTS before_user_insert;
```

## События (Events)

```sql
-- Включение планировщика
SET GLOBAL event_scheduler = ON;

-- Создание события
CREATE EVENT cleanup_old_logs
ON SCHEDULE EVERY 1 DAY
DO
    DELETE FROM logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Однократное событие
CREATE EVENT one_time_task
ON SCHEDULE AT '2024-12-31 23:59:59'
DO
    UPDATE stats SET year_end = TRUE;

-- Просмотр событий
SHOW EVENTS;

-- Удаление события
DROP EVENT IF EXISTS cleanup_old_logs;
```

## Полнотекстовый поиск

```sql
-- Создание таблицы с FULLTEXT индексом
CREATE TABLE articles (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    body TEXT,
    FULLTEXT(title, body)
) ENGINE=MyISAM;

-- Поиск
SELECT * FROM articles
WHERE MATCH(title, body) AGAINST('database optimization');

-- Булев режим
SELECT * FROM articles
WHERE MATCH(title, body) AGAINST('+MySQL -Oracle' IN BOOLEAN MODE);

-- Режим с расширением
SELECT * FROM articles
WHERE MATCH(title, body) AGAINST('database*' WITH QUERY EXPANSION);
```

## Компрессия и шифрование

```sql
-- Сжатие данных
SELECT COMPRESS('text to compress');
SELECT UNCOMPRESS(compressed_data);

-- Хэширование
SELECT MD5('password');
SELECT SHA1('password');
SELECT SHA2('password', 256);

-- Шифрование
SELECT AES_ENCRYPT('secret', 'key');
SELECT AES_DECRYPT(encrypted_data, 'key');
```

## Работа с JSON (MySQL 5.7+)

```sql
-- Создание JSON
SELECT JSON_OBJECT('name', 'John', 'age', 30);

-- Парсинг JSON
SELECT JSON_EXTRACT('{"name": "John"}', '$.name');
SELECT '{"name": "John"}'->>'$.name';

-- Обновление JSON
SELECT JSON_SET('{"name": "John"}', '$.age', 31);
SELECT JSON_INSERT('{"name": "John"}', '$.city', 'Moscow');
SELECT JSON_REPLACE('{"name": "John"}', '$.name', 'Jane');
SELECT JSON_REMOVE('{"name": "John", "age": 30}', '$.age');

-- Проверка существования
SELECT JSON_CONTAINS_PATH('{"name": "John"}', 'one', '$.name');

-- Слияние JSON
SELECT JSON_MERGE('{"a": 1}', '{"b": 2}');
```

## Производительность и мониторинг

```sql
-- Медленные запросы
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';

-- Буферный пул InnoDB
SHOW ENGINE INNODB STATUS;

-- Блокировки
SELECT * FROM information_schema.INNODB_LOCKS;
SELECT * FROM information_schema.INNODB_TRX;
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- Статистика по таблицам
ANALYZE TABLE users;
SHOW TABLE STATUS LIKE 'users';
```

## Утилиты командной строки

| Утилита | Описание |
|---------|----------|
| `mysql` | Клиент командной строки |
| `mysqldump` | Экспорт баз данных |
| `mysqlimport` | Импорт данных |
| `mysqladmin` | Администрирование |
| `mysqlshow` | Просмотр структуры |
| `myisamchk` | Проверка MyISAM таблиц |
| `innochecksum` | Проверка InnoDB файлов |
| `mysqlbinlog` | Чтение бинарных логов |
| `pt-query-digest` | Анализ запросов (Percona) |
| `mytop` | Мониторинг в реальном времени |

---

**Назад:** [Установка и настройка MySQL](./installation.md)  
**Далее:** [PostgreSQL: Установка и настройка](../postgresql/installation.md)
