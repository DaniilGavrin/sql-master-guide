# Агрегатные функции и GROUP BY

Агрегатные функции выполняют вычисления над набором значений и возвращают одно значение. Они незаменимы для аналитики и отчётности.

## 📊 Основные агрегатные функции

### COUNT — Подсчёт строк

```sql
-- Подсчёт всех строк
SELECT COUNT(*) FROM employees;

-- Подсчёт не-NULL значений
SELECT COUNT(dept_id) FROM employees;

-- Подсчёт уникальных значений
SELECT COUNT(DISTINCT dept_id) FROM employees;
```

### SUM — Суммирование

```sql
SELECT SUM(salary) AS total_salary FROM employees;
SELECT SUM(quantity * price) AS total_amount FROM order_items;
```

### AVG — Среднее значение

```sql
SELECT AVG(salary) AS avg_salary FROM employees;
SELECT AVG(price) AS avg_price FROM products;
```

### MIN / MAX — Минимум и максимум

```sql
SELECT MIN(salary) AS min_salary, MAX(salary) AS max_salary FROM employees;
SELECT MIN(order_date), MAX(order_date) FROM orders;
```

## 🔢 GROUP BY — Группировка данных

Оператор `GROUP BY` группирует строки с одинаковыми значениями в указанные столбцы.

```sql
SELECT dept_id, COUNT(*) AS emp_count, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id;
```

**Пример результата:**

| dept_id | emp_count | avg_salary |
|---------|-----------|------------|
| 10 | 5 | 75000 |
| 20 | 8 | 85000 |
| 30 | 3 | 65000 |

### Группировка по нескольким столбцам

```sql
SELECT 
    dept_id, 
    position, 
    COUNT(*) AS count,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id, position;
```

## 🎯 HAVING — Фильтрация групп

`HAVING` фильтрует результаты после группировки (в отличие от `WHERE`, который фильтрует до группировки).

```sql
-- Найти департаменты с более чем 5 сотрудниками
SELECT dept_id, COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 5;

-- Найти департаменты со средней зарплатой выше 80000
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 80000;
```

### WHERE vs HAVING

| Критерий | WHERE | HAVING |
|----------|-------|--------|
| Когда применяется | До группировки | После группировки |
| Что фильтрует | Отдельные строки | Группы строк |
| Можно использовать агрегаты | ❌ Нет | ✅ Да |
| Пример | `WHERE salary > 50000` | `HAVING COUNT(*) > 5` |

```sql
-- Правильное использование обоих
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
WHERE active = 1  -- Фильтр до группировки
GROUP BY dept_id
HAVING AVG(salary) > 60000;  -- Фильтр после группировки
```

## 💡 Практические примеры

### Пример 1: Отчёт по продажам по месяцам

```sql
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_sales,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### Пример 2: Топ клиентов по сумме заказов

```sql
SELECT 
    c.customer_name,
    COUNT(o.id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.customer_name
HAVING SUM(o.total_amount) > 10000
ORDER BY total_spent DESC
LIMIT 10;
```

### Пример 3: Статистика по продуктам

```sql
SELECT 
    p.category,
    COUNT(*) AS product_count,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price,
    AVG(p.price) AS avg_price,
    SUM(p.stock_quantity) AS total_stock
FROM products p
GROUP BY p.category
ORDER BY product_count DESC;
```

### Пример 4: Анализ активности сотрудников

```sql
SELECT 
    e.dept_id,
    d.dept_name,
    COUNT(e.id) AS emp_count,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    MIN(e.hire_date) AS earliest_hire,
    MAX(e.hire_date) AS latest_hire
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
GROUP BY e.dept_id, d.dept_name
HAVING COUNT(e.id) >= 3
ORDER BY avg_salary DESC;
```

## ⚠️ Частые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| SELECT столбца без GROUP BY | Ошибка SQL | Добавьте столбец в GROUP BY или используйте агрегат |
| Использование WHERE вместо HAVING | Невозможно фильтровать по агрегатам | Используйте HAVING для агрегатов |
| Забытый DISTINCT в COUNT | Дубликаты в подсчёте | Используйте `COUNT(DISTINCT column)` |
| Неправильный порядок | WHERE после GROUP BY | Сначала WHERE, потом GROUP BY, потом HAVING |

## 🎯 Порядок выполнения запроса

1. **FROM** — выбор таблиц
2. **JOIN** — объединение таблиц
3. **WHERE** — фильтрация строк
4. **GROUP BY** — группировка
5. **HAVING** — фильтрация групп
6. **SELECT** — выбор столбцов
7. **ORDER BY** — сортировка
8. **LIMIT** — ограничение результатов

## 📈 Комбинирование с другими функциями

```sql
-- Округление среднего значения
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id;

-- Конкатенация с агрегацией
SELECT 
    dept_id,
    STRING_AGG(name, ', ') AS employee_names,
    COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id;

-- CASE внутри агрегата
SELECT 
    COUNT(CASE WHEN salary > 80000 THEN 1 END) AS high_earners,
    COUNT(CASE WHEN salary <= 80000 THEN 1 END) AS low_earners
FROM employees;
```

## ➡️ Что дальше?

Изучите [подзапросы](./subqueries.md) для создания ещё более сложных запросов!
