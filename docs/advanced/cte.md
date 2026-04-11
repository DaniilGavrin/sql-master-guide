# CTE (Common Table Expressions)

Общие табличные выражения (CTE) позволяют создавать временные именованные наборы результатов, которые можно использовать в запросе. Они улучшают читаемость и поддерживают рекурсию.

## 📋 Базовый синтаксис

```sql
WITH cte_name AS (
    SELECT столбцы
    FROM таблицы
    WHERE условия
)
SELECT * FROM cte_name;
```

## 🔁 Обычные CTE

### Простой пример

```sql
WITH high_earners AS (
    SELECT id, name, salary, dept_id
    FROM employees
    WHERE salary > 100000
)
SELECT * FROM high_earners
ORDER BY salary DESC;
```

### Несколько CTE в одном запросе

```sql
WITH 
dept_stats AS (
    SELECT 
        dept_id,
        COUNT(*) AS emp_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
),
location_stats AS (
    SELECT 
        location,
        COUNT(*) AS dept_count
    FROM departments
    GROUP BY location
)
SELECT 
    d.dept_id,
    d.dept_name,
    ds.emp_count,
    ds.avg_salary,
    ls.location,
    ls.dept_count
FROM departments d
INNER JOIN dept_stats ds ON d.id = ds.dept_id
INNER JOIN location_stats ls ON d.location = ls.location
ORDER BY ds.avg_salary DESC;
```

### CTE вместо подзапроса

**С подзапросом:**
```sql
SELECT name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary) 
    FROM (
        SELECT AVG(salary) AS avg_sal
        FROM employees
        GROUP BY dept_id
    ) AS dept_avgs
);
```

**С CTE (читаемее):**
```sql
WITH dept_avgs AS (
    SELECT AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
),
overall_avg AS (
    SELECT AVG(avg_sal) AS avg_salary
    FROM dept_avgs
)
SELECT e.name, e.salary
FROM employees e, overall_avg o
WHERE e.salary > o.avg_salary;
```

## 🔄 Рекурсивные CTE

Рекурсивные CTE позволяют выполнять итеративные запросы, например, для обхода иерархий.

### Синтаксис

```sql
WITH RECURSIVE cte_name AS (
    -- Базовый случай (якорь)
    SELECT начальные_данные
    
    UNION ALL
    
    -- Рекурсивный случай
    SELECT рекурсивные_данные
    FROM cte_name
    WHERE условие_остановки
)
SELECT * FROM cte_name;
```

### Пример 1: Иерархия сотрудников

```sql
WITH RECURSIVE employee_hierarchy AS (
    -- Якорь: генеральный директор (без начальника)
    SELECT 
        id,
        name,
        manager_id,
        1 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Рекурсия: подчинённые
    SELECT 
        e.id,
        e.name,
        e.manager_id,
        eh.level + 1,
        eh.path || ' -> ' || e.name
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;
```

**Результат:**

| id | name | manager_id | level | path |
|----|------|------------|-------|------|
| 1 | Гендиректор | NULL | 1 | Гендиректор |
| 2 | Технический директор | 1 | 2 | Гендиректор -> Технический директор |
| 3 | Финансовый директор | 1 | 2 | Гендиректор -> Финансовый директор |
| 4 | Разработчик | 2 | 3 | Гендиректор -> Технический директор -> Разработчик |

### Пример 2: Генерация последовательности

```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    
    UNION ALL
    
    SELECT n + 1
    FROM numbers
    WHERE n < 100
)
SELECT * FROM numbers;
```

### Пример 3: Обход дерева категорий

```sql
WITH RECURSIVE category_tree AS (
    -- Корневые категории
    SELECT 
        id,
        name,
        parent_id,
        0 AS depth,
        CAST(name AS VARCHAR(1000)) AS full_path
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Дочерние категории
    SELECT 
        c.id,
        c.name,
        c.parent_id,
        ct.depth + 1,
        ct.full_path || ' / ' || c.name
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree
ORDER BY full_path;
```

### Пример 4: Поиск пути в графе

```sql
WITH RECURSIVE paths AS (
    -- Начальная точка
    SELECT 
        start_node,
        end_node,
        1 AS distance,
        ARRAY[start_node, end_node] AS path
    FROM edges
    WHERE start_node = 'A'
    
    UNION ALL
    
    -- Продолжение пути
    SELECT 
        p.start_node,
        e.end_node,
        p.distance + 1,
        p.path || e.end_node
    FROM paths p
    INNER JOIN edges e ON p.end_node = e.start_node
    WHERE e.end_node != ALL(p.path)  -- Избегаем циклов
      AND p.distance < 10  -- Ограничение глубины
)
SELECT * FROM paths
WHERE end_node = 'Z'
ORDER BY distance
LIMIT 1;  -- Кратчайший путь
```

## 💡 Практические примеры

### Пример 1: Отчёт с промежуточными вычислениями

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(total_amount) AS total_sales,
        COUNT(*) AS order_count
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', order_date)
),
sales_with_growth AS (
    SELECT 
        month,
        total_sales,
        order_count,
        LAG(total_sales) OVER (ORDER BY month) AS prev_month_sales,
        ROUND(
            100.0 * (total_sales - LAG(total_sales) OVER (ORDER BY month)) 
            / NULLIF(LAG(total_sales) OVER (ORDER BY month), 0),
            2
        ) AS growth_percent
    FROM monthly_sales
)
SELECT * FROM sales_with_growth
ORDER BY month;
```

### Пример 2: Удаление дубликатов

```sql
WITH duplicates AS (
    SELECT 
        id,
        ROW_NUMBER() OVER (
            PARTITION BY email 
            ORDER BY created_at
        ) AS rn
    FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);
```

### Пример 3: Обновление с использованием CTE

```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
UPDATE employees e
SET salary = salary * 1.1
WHERE e.salary < (
    SELECT da.avg_salary
    FROM dept_avg da
    WHERE da.dept_id = e.dept_id
);
```

## ⚠️ Частые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| Бесконечная рекурсия | Зависание запроса | Всегда добавляйте условие остановки |
| Отсутствие ограничения глубины | Переполнение стека | Используйте `MAXRECURSION` или аналог |
| Неправильное использование UNION | Дубликаты или потеря данных | Выбирайте UNION или UNION ALL осознанно |
| Сложные рекурсивные запросы | Плохая производительность | Индексируйте ключевые столбцы |

## 🎯 UNION vs UNION ALL в рекурсии

- **UNION** — удаляет дубликаты (медленнее, но безопаснее)
- **UNION ALL** — сохраняет все строки (быстрее, но может зациклиться)

```sql
-- Безопаснее для рекурсии
WITH RECURSIVE ... AS (
    SELECT ...
    UNION
    SELECT ...
)

-- Быстрее, но требует контроля циклов
WITH RECURSIVE ... AS (
    SELECT ...
    UNION ALL
    SELECT ... WHERE ... -- явное условие остановки
)
```

## 📊 CTE vs Подзапросы vs Временные таблицы

| Критерий | CTE | Подзапросы | Временные таблицы |
|----------|-----|------------|-------------------|
| Читаемость | ✅ Отличная | ⚠️ Средняя | ✅ Хорошая |
| Переиспользование | ✅ В одном запросе | ❌ Нет | ✅ В сессии |
| Рекурсия | ✅ Да | ❌ Нет | ⚠️ Через цикл |
| Производительность | ✅ Оптимизируется | ⚠️ Может дублироваться | ✅ Индексы |
| Область видимости | Один запрос | Один запрос | Сессия/транзакция |

## ➡️ Что дальше?

Изучите [индексы и оптимизацию](./indexes.md) для ускорения запросов!
