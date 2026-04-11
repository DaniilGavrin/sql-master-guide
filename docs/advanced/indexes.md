# Индексы и оптимизация запросов

Индексы — это структуры данных, которые ускоряют поиск и сортировку данных в таблицах. Правильное использование индексов критически важно для производительности базы данных.

## 📊 Что такое индекс?

Индекс работает как оглавление в книге — позволяет быстро найти нужные данные без просмотра всей таблицы.

```sql
-- Без индекса: полный скан таблицы (медленно)
SELECT * FROM employees WHERE last_name = 'Иванов';

-- С индексом: быстрый поиск по индексу
CREATE INDEX idx_last_name ON employees(last_name);
SELECT * FROM employees WHERE last_name = 'Иванов';
```

## 🔧 Типы индексов

### 1. B-Tree (по умолчанию)

Подходит для большинства случаев: равенство, диапазоны, сортировка.

```sql
CREATE INDEX idx_salary ON employees(salary);
CREATE INDEX idx_name ON employees(last_name, first_name);
```

**Эффективен для:**
- `=`, `<`, `>`, `<=`, `>=`
- `BETWEEN`
- `ORDER BY`
- `GROUP BY`

### 2. Hash Index

Только для точного совпадения (=). Быстрее B-Tree для равенства.

```sql
-- PostgreSQL
CREATE INDEX idx_email_hash ON employees USING HASH(email);
```

**Эффективен только для:**
- `=`
- `IN`

### 3. GiST и GIN

Для полнотекстового поиска, JSON, массивов, геометрических данных.

```sql
-- Полнотекстовый поиск
CREATE INDEX idx_search ON documents USING GIN(to_tsvector('russian', content));

-- JSONB индекс
CREATE INDEX idx_data ON products USING GIN(data);

-- Массивы
CREATE INDEX idx_tags ON articles USING GIN(tags);
```

### 4. BRIN

Для больших таблиц с естественным порядком данных (временные ряды).

```sql
CREATE INDEX idx_date_brin ON logs USING BRIN(created_at);
```

## 📈 Составные индексы

Индекс по нескольким столбцам. Порядок столбцов важен!

```sql
-- Индекс для запросов по dept_id и salary
CREATE INDEX idx_dept_salary ON employees(dept_id, salary);
```

### Правило левого префикса

Индекс `(A, B, C)` работает для:
- ✅ `WHERE A = ?`
- ✅ `WHERE A = ? AND B = ?`
- ✅ `WHERE A = ? AND B = ? AND C = ?`
- ❌ `WHERE B = ?` (нет A)
- ❌ `WHERE C = ?` (нет A и B)

```sql
-- Эффективно использует индекс
SELECT * FROM employees WHERE dept_id = 10 AND salary > 50000;

-- Не использует индекс полностью
SELECT * FROM employees WHERE salary > 50000;
```

## 🎯 Уникальные индексы

Гарантируют уникальность значений.

```sql
CREATE UNIQUE INDEX idx_unique_email ON users(email);
-- Или при создании таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE
);
```

## ⚡ Оптимизация запросов

### EXPLAIN — Анализ плана выполнения

```sql
-- Показать план выполнения
EXPLAIN SELECT * FROM employees WHERE last_name = 'Иванов';

-- Подробный анализ с фактическим выполнением
EXPLAIN ANALYZE SELECT * FROM employees WHERE last_name = 'Иванов';
```

**Ключевые метрики:**
- **Seq Scan** — полный скан таблицы (плохо для больших таблиц)
- **Index Scan** — сканирование индекса (хорошо)
- **Index Only Scan** — только индекс (отлично)
- **Bitmap Heap Scan** — комбинация индексов (хорошо)

### Пример анализа

```sql
EXPLAIN ANALYZE
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
WHERE e.salary > 80000
ORDER BY e.salary DESC
LIMIT 10;
```

**Что искать:**
- Высокая стоимость (cost)
- Большой объём строк (rows)
- Фактическое время (actual time)

## 🔍 Практики оптимизации

### 1. Избегайте SELECT *

```sql
-- Плохо: выбирает все столбцы
SELECT * FROM employees;

-- Хорошо: только нужные столбцы
SELECT id, name, salary FROM employees;
```

### 2. Используйте LIMIT

```sql
-- Получить только первые 10 результатов
SELECT * FROM products ORDER BY created_at DESC LIMIT 10;
```

### 3. Оптимизируйте WHERE

```sql
-- Плохо: функция на столбце ломает индекс
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-15';

-- Хорошо: диапазон
SELECT * FROM orders 
WHERE order_date >= '2024-01-15' 
  AND order_date < '2024-01-16';
```

### 4. Избегайте LIKE с ведущим %

```sql
-- Плохо: не использует индекс
SELECT * FROM products WHERE name LIKE '%phone%';

-- Хорошо: использует индекс
SELECT * FROM products WHERE name LIKE 'phone%';

-- Альтернатива: полнотекстовый поиск
SELECT * FROM products 
WHERE to_tsvector('russian', name) @@ to_tsquery('russian', 'phone');
```

### 5. Оптимизируйте JOIN

```sql
-- Убедитесь, что ключи соединения индексированы
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_customers_id ON customers(id);

-- Теперь JOIN будет быстрым
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

### 6. Используйте EXISTS вместо IN для подзапросов

```sql
-- Медленнее для больших наборов
SELECT * FROM customers c
WHERE c.id IN (SELECT customer_id FROM orders);

-- Быстрее
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

## 📊 Мониторинг индексов

### PostgreSQL

```sql
-- Статистика использования индексов
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Найти неиспользуемые индексы
SELECT indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey';

-- Размер индексов
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

### MySQL

```sql
-- Статистика индексов
SHOW INDEX FROM employees;

-- Анализ таблицы
ANALYZE TABLE employees;

-- Проверка медленных запросов
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';
```

## 💡 Стратегии индексирования

### Когда создавать индекс

✅ Частые запросы с WHERE, JOIN, ORDER BY
✅ Столбцы с высокой селективностью (много уникальных значений)
✅ Внешние ключи для JOIN
✅ Столбцы, используемые в GROUP BY

### Когда НЕ создавать индекс

❌ Таблицы с частыми INSERT/UPDATE/DELETE (индексы замедляют запись)
❌ Столбцы с низкой селективностью (пол, статус)
❌ Маленькие таблицы (< 1000 строк)
❌ Столбцы, которые редко используются в запросах

### Покрывающий индекс

Индекс, содержащий все столбцы запроса.

```sql
-- Запрос
SELECT id, name, salary FROM employees WHERE dept_id = 10;

-- Покрывающий индекс
CREATE INDEX idx_dept_covering ON employees(dept_id, id, name, salary);

-- Теперь используется Index Only Scan
```

## ⚠️ Распространённые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| Слишком много индексов | Замедление записи | Удаляйте неиспользуемые |
| Неправильный порядок столбцов | Индекс не используется | Ставьте более селективные первыми |
| Индексы на маленьких таблицах | Накладные расходы | Индексируйте только большие таблицы |
| Отсутствие ANALYZE | Устаревшая статистика | Регулярно обновляйте статистику |
| Игнорирование EXPLAIN | Неизвестна причина медленной работы | Всегда анализируйте план |

## 🎯 Чек-лист оптимизации

1. ✅ Проанализируйте медленные запросы через `EXPLAIN ANALYZE`
2. ✅ Добавьте индексы на столбцы в WHERE и JOIN
3. ✅ Убедитесь, что внешние ключи индексированы
4. ✅ Удалите неиспользуемые индексы
5. ✅ Обновите статистику (`ANALYZE`)
6. ✅ Рассмотрите покрывающие индексы для частых запросов
7. ✅ Избегайте функций на столбцах в WHERE
8. ✅ Используйте LIMIT для ограничения результатов

## ➡️ Что дальше?

Изучите [транзакции](./transactions.md) для обеспечения целостности данных!
