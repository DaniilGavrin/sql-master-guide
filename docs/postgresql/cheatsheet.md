# Шпаргалка по PostgreSQL

Полный справочник команд и особенностей PostgreSQL для быстрого поиска.

## Типы данных PostgreSQL

### Числовые типы

| Тип | Размер | Диапазон | Описание |
|-----|--------|----------|----------|
| `SMALLINT` / `INT2` | 2 байта | -32,768 to 32,767 | Малое целое |
| `INTEGER` / `INT` / `INT4` | 4 байта | -2,147,483,648 to 2,147,483,647 | Целое |
| `BIGINT` / `INT8` | 8 байтов | Очень большой диапазон | Большое целое |
| `SERIAL` | 4 байта | Автоинкремент | Последовательность |
| `BIGSERIAL` | 8 байтов | Автоинкремент | Большая последовательность |
| `REAL` / `FLOAT4` | 4 байта | ~6 знаков | Число с плавающей точкой |
| `DOUBLE PRECISION` / `FLOAT8` | 8 байтов | ~15 знаков | Число с плавающей точкой |
| `NUMERIC(M,D)` / `DECIMAL` | Переменный | Точное значение | Точное число |

### Строковые типы

| Тип | Описание | Макс размер |
|-----|----------|-------------|
| `CHAR(N)` | Фиксированная длина | 1 GB |
| `VARCHAR(N)` | Переменная длина с лимитом | 1 GB |
| `TEXT` | Переменная длина без лимита | 1 GB |
| `"char"` | Один символ | 1 байт |
| `NAME` | Для имен объектов | 64 байта |

### Типы даты и времени

| Тип | Размер | Диапазон | Точность |
|-----|--------|----------|----------|
| `TIMESTAMP` | 8 байтов | 4713 BC to 5874897 AD | 1 микросекунда |
| `TIMESTAMPTZ` | 8 байтов | С часовым поясом | 1 микросекунда |
| `DATE` | 4 байта | 4713 BC to 5874897 AD | 1 день |
| `TIME` | 8 байтов | 00:00:00 to 24:00:00 | 1 микросекунда |
| `TIMETZ` | 12 байтов | С часовым поясом | 1 микросекунда |
| `INTERVAL` | 16 байтов | -178,000,000 to 178,000,000 лет | 1 микросекунда |

### Булевы и битовые типы

```sql
-- BOOLEAN
CREATE TABLE flags (
    is_active BOOLEAN,  -- TRUE, FALSE, NULL
    is_deleted BOOL     -- алиас
);

-- BIT
CREATE TABLE bitfields (
    flags BIT(8),           -- фиксированная длина
    varflags BIT VARYING(8) -- переменная длина
);
```

### JSON типы

```sql
CREATE TABLE data (
    id INT,
    raw_json JSON,      -- текст JSON (быстрее вставка)
    parsed_json JSONB   -- бинарный JSON (быстрее запросы, поддерживает индексы)
);

-- Вставка
INSERT INTO data VALUES (1, '{"key": "value"}'::jsonb);

-- Query JSONB
SELECT parsed_json->>'key' FROM data WHERE id = 1;
SELECT * FROM data WHERE parsed_json @> '{"key": "value"}';
```

### Массивы

```sql
-- Одномерный массив
CREATE TABLE tags (
    id INT,
    tags TEXT[]
);

-- Многомерный массив
CREATE TABLE matrix (
    id INT,
    grid INT[][]
);

-- Вставка
INSERT INTO tags VALUES (1, ARRAY['tag1', 'tag2']);
INSERT INTO tags VALUES (2, '{"tag3", "tag4"}');

-- Query
SELECT * FROM tags WHERE 'tag1' = ANY(tags);
SELECT * FROM tags WHERE tags @> ARRAY['tag1'];
```

### Специальные типы

| Тип | Описание |
|-----|----------|
| `UUID` | Универсальный уникальный идентификатор |
| `XML` | XML данные |
| `INET` | IPv4/IPv6 адреса |
| `CIDR` | IPv4/IPv6 сети |
| `MACADDR` | MAC адреса |
| `TSVECTOR` | Для полнотекстового поиска |
| `TSQUERY` | Запрос полнотекстового поиска |
| `POINT`, `LINE`, `LSEG`, `BOX`, `PATH`, `POLYGON`, `CIRCLE` | Геометрические типы |
| `PG_LSN` | Log Sequence Number для репликации |

## Специфичные команды PostgreSQL

### Управление схемами

```sql
-- Создание схемы
CREATE SCHEMA myschema;

-- Установка пути поиска
SET search_path TO myschema, public;

-- Просмотр схем
\dn

-- Удаление схемы
DROP SCHEMA IF EXISTS myschema CASCADE;
```

### Управление таблицами

```sql
-- Создание таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Изменение таблицы
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users RENAME TO accounts;

-- Удаление таблицы
DROP TABLE IF EXISTS users CASCADE;

-- Усечение таблицы (быстрое удаление всех данных)
TRUNCATE TABLE users RESTART IDENTITY;
```

### Ограничения (Constraints)

```sql
-- PRIMARY KEY
CREATE TABLE pk_example (
    id INT PRIMARY KEY
);

-- FOREIGN KEY
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE
);

-- UNIQUE
CREATE TABLE unique_example (
    id INT,
    email TEXT UNIQUE
);

-- CHECK
CREATE TABLE check_example (
    id INT,
    age INT CHECK (age >= 18),
    status TEXT CHECK (status IN ('active', 'inactive'))
);

-- NOT NULL
CREATE TABLE notnull_example (
    id INT NOT NULL
);

-- EXCLUSION (PostgreSQL специфика)
CREATE TABLE ranges (
    id INT,
    period TSRANGE,
    EXCLUDE USING GIST (period WITH &&)
);
```

### Работа с последовательностями

```sql
-- Создание последовательности
CREATE SEQUENCE myseq START WITH 1 INCREMENT BY 1;

-- Использование
SELECT nextval('myseq');
SELECT currval('myseq');
SELECT setval('myseq', 100);

-- Сброс последовательности
ALTER SEQUENCE myseq RESTART WITH 1;

-- Удаление
DROP SEQUENCE IF EXISTS myseq;
```

## Функции PostgreSQL

### Строковые функции

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `CONCAT(a,b,...)` | Конкатенация | `CONCAT('Hello', ' ', 'World')` | `'Hello World'` |
| `SUBSTRING(str, start, len)` | Подстрока | `SUBSTRING('PostgreSQL', 1, 4)` | `'Post'` |
| `LENGTH(str)` | Длина | `LENGTH('привет')` | `12` |
| `CHAR_LENGTH(str)` | Длина в символах | `CHAR_LENGTH('привет')` | `6` |
| `UPPER(str)` | Верхний регистр | `UPPER('postgresql')` | `'POSTGRESQL'` |
| `LOWER(str)` | Нижний регистр | `LOWER('POSTGRESQL')` | `'postgresql'` |
| `TRIM(str)` | Удаление пробелов | `TRIM('  test  ')` | `'test'` |
| `REPLACE(str, from, to)` | Замена | `REPLACE('aabb', 'a', 'x')` | `'xxbb'` |
| `POSITION(sub IN str)` | Позиция | `POSITION('ll' IN 'hello')` | `3` |
| `LPAD(str, len, pad)` | Левое дополнение | `LPAD('5', 3, '0')` | `'005'` |
| `RPAD(str, len, pad)` | Правое дополнение | `RPAD('5', 3, '0')` | `'500'` |
| `SPLIT_PART(str, delim, n)` | Разделение | `SPLIT_PART('a,b,c', ',', 2)` | `'b'` |
| `REGEXP_MATCHES(str, pattern)` | RegExp | `REGEXP_MATCHES('abc123', '\d+')` | `{123}` |
| `STRING_AGG(expr, delim)` | Агрегация строк | `STRING_AGG(name, ', ')` | `'A, B, C'` |

### Числовые функции

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `ABS(x)` | Модуль | `ABS(-5)` | `5` |
| `CEIL(x)` / `CEILING(x)` | Округление вверх | `CEIL(4.2)` | `5` |
| `FLOOR(x)` | Округление вниз | `FLOOR(4.8)` | `4` |
| `ROUND(x, d)` | Округление | `ROUND(4.567, 2)` | `4.57` |
| `TRUNC(x, d)` | Отсечение | `TRUNC(4.567, 2)` | `4.56` |
| `MOD(a, b)` | Остаток | `MOD(10, 3)` | `1` |
| `RANDOM()` | Случайное число | `RANDOM()` | `0.xxxxx` |
| `POWER(x, y)` | Степень | `POWER(2, 3)` | `8` |
| `SQRT(x)` | Квадратный корень | `SQRT(16)` | `4` |
| `CBRT(x)` | Кубический корень | `CBRT(27)` | `3` |
| `FACTORIAL(n)` | Факториал | `FACTORIAL(5)` | `120` |
| `GCD(a, b)` | НОД | `GCD(12, 8)` | `4` |
| `LCM(a, b)` | НОК | `LCM(12, 8)` | `24` |

### Функции даты и времени

| Функция | Описание | Пример | Результат |
|---------|----------|--------|-----------|
| `NOW()` | Текущие дата и время | `NOW()` | `timestamp with time zone` |
| `CURRENT_TIMESTAMP` | Текущая метка времени | `CURRENT_TIMESTAMP` | `timestamptz` |
| `CURRENT_DATE` | Текущая дата | `CURRENT_DATE` | `date` |
| `CURRENT_TIME` | Текущее время | `CURRENT_TIME` | `time with time zone` |
| `AGE(timestamp)` | Разница от сейчас | `AGE('2020-01-01')` | `interval` |
| `AGE(t1, t2)` | Разница между датами | `AGE('2024-01-20', '2024-01-15')` | `5 days` |
| `DATE_TRUNC(part, ts)` | Усечение даты | `DATE_TRUNC('month', NOW())` | `начало месяца` |
| `DATE_PART(part, ts)` | Извлечение части | `DATE_PART('year', NOW())` | `2024` |
| `EXTRACT(part FROM ts)` | Извлечение | `EXTRACT(MONTH FROM NOW())` | `1` |
| `TO_CHAR(ts, fmt)` | Форматирование | `TO_CHAR(NOW(), 'DD.MM.YYYY')` | `'15.01.2024'` |
| `TO_DATE(str, fmt)` | Парсинг даты | `TO_DATE('15.01.2024', 'DD.MM.YYYY')` | `date` |
| `TO_TIMESTAMP(str, fmt)` | Парсинг timestamp | `TO_TIMESTAMP(...)` | `timestamp` |
| `MAKE_DATE(y, m, d)` | Создание даты | `MAKE_DATE(2024, 1, 15)` | `date` |
| `MAKE_TIMESTAMP(...)` | Создание timestamp | `MAKE_TIMESTAMP(2024, 1, 15, 10, 30, 0)` | `timestamp` |
| `GENERATE_SERIES(start, end, step)` | Генерация серии | `GENERATE_SERIES(1, 5, 1)` | `1,2,3,4,5` |

**Форматы даты:**
- `YYYY` — год (4 цифры)
- `YY` — год (2 цифры)
- `MM` — месяц (01-12)
- `DD` — день (01-31)
- `HH24` — часы (00-23)
- `HH12` — часы (01-12)
- `MI` — минуты (00-59)
- `SS` — секунды (00-59)
- `MS` — миллисекунды (000-999)
- `US` — микросекунды (000000-999999)
- `Day` — день недели (полный)
- `Mon` — месяц (сокращённый)

### Агрегатные функции

| Функция | Описание |
|---------|----------|
| `COUNT(*)` | Количество строк |
| `COUNT(column)` | Количество непустых значений |
| `SUM(column)` | Сумма |
| `AVG(column)` | Среднее |
| `MIN(column)` | Минимум |
| `MAX(column)` | Максимум |
| `STRING_AGG(expr, delim)` | Конкатенация строк |
| `ARRAY_AGG(expr)` | Агрегация в массив |
| `JSON_AGG(expr)` | Агрегация в JSON |
| `JSONB_AGG(expr)` | Агрегация в JSONB |
| `JSON_OBJECT_AGG(key, value)` | Агрегация в JSON объект |
| `BOOL_AND(expr)` | Логическое И |
| `BOOL_OR(expr)` | Логическое ИЛИ |
| `EVERY(expr)` | Алиас для BOOL_AND |
| `STDDEV(column)` | Стандартное отклонение |
| `VARIANCE(column)` | Дисперсия |
| `CORR(x, y)` | Корреляция |
| `COVAR_POP(x, y)` | Ковариация |

### Оконные функции

```sql
-- ROW_NUMBER
SELECT name, score, ROW_NUMBER() OVER (ORDER BY score DESC) as rank
FROM students;

-- RANK и DENSE_RANK
SELECT name, score, 
       RANK() OVER (ORDER BY score DESC) as rank,
       DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;

-- NTILE
SELECT name, score, NTILE(4) OVER (ORDER BY score DESC) as quartile
FROM students;

-- LAG и LEAD
SELECT date, value,
       LAG(value, 1) OVER (ORDER BY date) as prev_value,
       LEAD(value, 1) OVER (ORDER BY date) as next_value
FROM metrics;

-- FIRST_VALUE и LAST_VALUE
SELECT date, value,
       FIRST_VALUE(value) OVER (ORDER BY date) as first,
       LAST_VALUE(value) OVER (ORDER BY date 
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last
FROM metrics;

-- NTH_VALUE
SELECT name, score, NTH_VALUE(score, 2) OVER (ORDER BY score DESC) as second_score
FROM students;

-- Накопительная сумма
SELECT date, sales,
       SUM(sales) OVER (ORDER BY date) as running_total
FROM daily_sales;

-- Скользящее среднее
SELECT date, sales,
       AVG(sales) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
FROM daily_sales;

-- Partition By
SELECT department, employee, salary,
       AVG(salary) OVER (PARTITION BY department) as dept_avg,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- Frame clauses
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
```

## Управление транзакциями

```sql
-- Начало транзакции
BEGIN;
START TRANSACTION;

-- Точки сохранения
SAVEPOINT sp1;

-- Откат до точки сохранения
ROLLBACK TO sp1;

-- Полный откат
ROLLBACK;

-- Фиксация
COMMIT;
COMMIT WORK;

-- Установка уровня изоляции
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- ReadOnly транзакция
SET TRANSACTION READ ONLY;
```

**Уровни изоляции PostgreSQL:**
- `READ UNCOMMITTED` (синоним READ COMMITTED)
- `READ COMMITTED` (по умолчанию)
- `REPEATABLE READ`
- `SERIALIZABLE`

## Конфликты и блокировки

```sql
-- Просмотр блокировок
SELECT * FROM pg_locks;

-- Просмотр ожидающих запросов
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Убийство блокирующего процесса
SELECT pg_terminate_backend(pid);

-- Advisory locks (советующие блокировки)
SELECT pg_advisory_lock(123);
SELECT pg_advisory_unlock(123);
SELECT pg_try_advisory_lock(123);
```

## Переменные и параметры

```sql
-- Пользовательские переменные через SET
SET myapp.user_id = 123;
SELECT current_setting('myapp.user_id');

-- Системные параметры
SHOW ALL;
SHOW max_connections;
SET work_mem = '64MB';
SET SESSION statement_timeout = '30s';

-- Конфигурация на уровне сессии
SET LOCAL work_mem = '128MB';  -- только в рамках транзакции
```

## EXPLAIN и оптимизация

```sql
-- Анализ плана выполнения
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Расширенный анализ с выполнением
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- С буферами
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';

-- С cost settings
EXPLAIN (ANALYZE, COSTS, VERBOSE, SETTINGS, BUFFERS, WAL, TIMING) 
SELECT * FROM users WHERE email = 'test@example.com';

-- JSON формат
EXPLAIN (FORMAT JSON) SELECT * FROM users WHERE email = 'test@example.com';

-- YAML формат
EXPLAIN (FORMAT YAML) SELECT * FROM users WHERE email = 'test@example.com';
```

**Типы сканирования:**
- `Seq Scan` — полное сканирование таблицы
- `Index Scan` — сканирование по индексу с доступом к таблице
- `Index Only Scan` — только индекс (без доступа к таблице)
- `Bitmap Index Scan` + `Bitmap Heap Scan` — битовая карта индексов

**Типы JOIN:**
- `Nested Loop` — вложенные циклы (хорошо для маленьких таблиц)
- `Hash Join` — хэш соединение (хорошо для больших таблиц)
- `Merge Join` — сортировка + слияние (для отсортированных данных)

## Системные каталоги и представления

```sql
-- Информация о базах данных
SELECT * FROM pg_database;

-- Информация о таблицах
SELECT * FROM pg_tables WHERE schemaname = 'public';

-- Информация о колонках
SELECT * FROM information_schema.columns WHERE table_name = 'users';

-- Индексы
SELECT * FROM pg_indexes WHERE tablename = 'users';

-- Внешние ключи
SELECT * FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY';

-- Зависимости
SELECT * FROM pg_depend;

-- Статистика
SELECT * FROM pg_stat_user_tables;
SELECT * FROM pg_stat_user_indexes;

-- Размер объектов
SELECT pg_size_pretty(pg_total_relation_size('users'));
SELECT pg_size_pretty(pg_database_size(current_database()));
```

## Хранимые процедуры и функции

```sql
-- Создание функции (PL/pgSQL)
CREATE OR REPLACE FUNCTION get_user(user_id INT)
RETURNS TABLE(id INT, username TEXT, email TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.username, u.email
    FROM users u
    WHERE u.id = user_id;
END;
$$ LANGUAGE plpgsql;

-- Вызов функции
SELECT * FROM get_user(1);

-- Функция с OUT параметрами
CREATE OR REPLACE FUNCTION get_stats(
    IN user_id INT,
    OUT total_orders INT,
    OUT total_amount NUMERIC
) AS $$
BEGIN
    SELECT COUNT(*), SUM(amount)
    INTO total_orders, total_amount
    FROM orders
    WHERE user_id = $1;
END;
$$ LANGUAGE plpgsql;

-- Процедура (PostgreSQL 11+)
CREATE OR REPLACE PROCEDURE transfer_funds(
    from_account INT,
    to_account INT,
    amount NUMERIC
) AS $$
BEGIN
    UPDATE accounts SET balance = balance - amount WHERE id = from_account;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account;
END;
$$ LANGUAGE plpgsql;

CALL transfer_funds(1, 2, 100);

-- Триггерная функция
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER update_users_modtime
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Удаление
DROP FUNCTION IF EXISTS get_user(INT);
DROP PROCEDURE IF EXISTS transfer_funds(INT, INT, NUMERIC);
DROP TRIGGER IF EXISTS update_users_modtime ON users;
```

## Полнотекстовый поиск

```sql
-- Базовый поиск
SELECT * FROM articles
WHERE to_tsvector('russian', title || ' ' || body) @@ to_tsquery('russian', 'база & данных');

-- С использованием столбца tsvector
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;
UPDATE articles SET search_vector = to_tsvector('russian', title || ' ' || body);
CREATE INDEX idx_search ON articles USING GIN(search_vector);

-- Поиск
SELECT * FROM articles WHERE search_vector @@ to_tsquery('russian', 'база & данных');

-- Ранжирование
SELECT title, ts_rank(search_vector, query) as rank
FROM articles, to_tsquery('russian', 'база & данных') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Подсветка результатов
SELECT ts_headline('russian', body, to_tsquery('russian', 'база'), 'StartSel=<b>, StopSel=</b>')
FROM articles WHERE search_vector @@ to_tsquery('russian', 'база');

-- Синонимы и словари
SELECT to_tsvector('russian', 'бежит') @@ to_tsquery('russian', 'бежать');
```

## Работа с JSONB

```sql
-- Создание
SELECT '{"name": "John", "age": 30}'::jsonb;
SELECT jsonb_build_object('name', 'John', 'age', 30);
SELECT jsonb_build_array(1, 2, 3);

-- Извлечение
SELECT data->'name' FROM table;        -- JSONB
SELECT data->>'name' FROM table;       -- TEXT
SELECT data#>'{address,city}' FROM table;  -- вложенный
SELECT data#>>'{address,city}' FROM table;

-- Проверка существования
SELECT * FROM table WHERE data ? 'name';
SELECT * FROM table WHERE data ?| ARRAY['name', 'age'];
SELECT * FROM table WHERE data ?& ARRAY['name', 'age'];

-- Поиск по значению
SELECT * FROM table WHERE data @> '{"age": 30}';
SELECT * FROM table WHERE data->>'name' = 'John';

-- Обновление
UPDATE table SET data = jsonb_set(data, '{age}', '31');
UPDATE table SET data = data || '{"city": "Moscow"}'::jsonb;
UPDATE table SET data = data - 'temp_field';

-- Агрегация
SELECT jsonb_agg(name) FROM users;
SELECT jsonb_object_agg(id, name) FROM users;
```

## Репликация

```sql
-- Настройка standby
-- postgresql.conf на master:
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64

-- pg_hba.conf на master:
host    replication     replicator      192.168.1.0/24        scram-sha-256

-- Создание пользователя репликации
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'password';

-- Бэкап для standby
pg_basebackup -h master -D /var/lib/postgresql/data -U replicator -P -X stream

-- Проверка статуса репликации
SELECT * FROM pg_stat_replication;

-- Переключение на standby
SELECT pg_promote();

-- Создание слота репликации
SELECT pg_create_physical_replication_slot('standby_slot');
```

## Секционирование таблиц

```sql
-- Декларативное секционирование (PostgreSQL 10+)
CREATE TABLE logs (
    id INT,
    log_date DATE NOT NULL,
    message TEXT
) PARTITION BY RANGE (log_date);

-- Создание партиций
CREATE TABLE logs_2024_q1 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE logs_2024_q2 PARTITION OF logs
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Секционирование по списку
CREATE TABLE users_by_country (
    id INT,
    country TEXT NOT NULL
) PARTITION BY LIST (country);

CREATE TABLE users_ru PARTITION OF users_by_country
    FOR VALUES IN ('RU');

CREATE TABLE users_us PARTITION OF users_by_country
    FOR VALUES IN ('US');

-- Просмотр партиций
SELECT * FROM pg_partitioned_table;
```

## Полезные расширения

```sql
-- pg_stat_statements (статистика запросов)
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- uuid-ossp (генерация UUID)
CREATE EXTENSION uuid-ossp;
SELECT uuid_generate_v4();

-- hstore (ключ-значение)
CREATE EXTENSION hstore;
SELECT 'name => John, age => 30'::hstore;

-- pg_trgm (триграммы для нечёткого поиска)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_name_trgm ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name % 'Jon';  -- похоже на 'Jon'
SELECT similarity('John', 'Jon');  -- 0.75

-- citext (регистронезависимый текст)
CREATE EXTENSION citext;
CREATE TABLE users (email CITEXT UNIQUE);

-- btree_gin (B-tree операторы в GIN)
CREATE EXTENSION btree_gin;

-- postgis (геоданные)
CREATE EXTENSION postgis;
```

## Утилиты командной строки

| Утилита | Описание |
|---------|----------|
| `psql` | Интерактивный терминал |
| `pg_dump` | Экспорт базы |
| `pg_dumpall` | Экспорт всех баз |
| `pg_restore` | Восстановление из бэкапа |
| `pg_basebackup` | Физический бэкап |
| `pgbench` | Бенчмарк производительности |
| `createdb` | Создание базы |
| `createuser` | Создание пользователя |
| `dropdb` | Удаление базы |
| `dropuser` | Удаление пользователя |
| `pg_isready` | Проверка готовности сервера |
| `pg_ctl` | Управление сервером |
| `initdb` | Инициализация кластера |
| `vacuumlo` | Удаление orphaned large objects |
| `pg_rewind` | Синхронизация после failover |

---

**Назад:** [Установка и настройка PostgreSQL](./installation.md)  
**Далее:** [Справочник SQL команд](../reference/commands.md)
