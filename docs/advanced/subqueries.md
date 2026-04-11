# Подзапросы (Subqueries)

Подзапрос — это запрос, вложенный в другой запрос. Он позволяет использовать результаты одного запроса внутри другого для создания сложных логических конструкций.

## 📋 Типы подзапросов

### 1. Подзапрос в WHERE

Используется для фильтрации данных на основе результатов другого запроса.

```sql
-- Найти сотрудников с зарплатой выше средней
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Найти продукты, которые заказывали
SELECT product_name
FROM products
WHERE id IN (SELECT DISTINCT product_id FROM order_items);
```

### 2. Подзапрос в SELECT

Возвращает значение для каждого результата основного запроса.

```sql
-- Показать зарплату сотрудника и среднюю по компании
SELECT 
    name,
    salary,
    (SELECT AVG(salary) FROM employees) AS avg_salary,
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

### 3. Подзапрос в FROM

Используется как виртуальная таблица.

```sql
-- Найти департаменты со средней зарплатой выше общей средней
SELECT dept_id, avg_salary
FROM (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) AS dept_stats
WHERE avg_salary > (SELECT AVG(salary) FROM employees);
```

## 🔍 Операторы с подзапросами

### IN / NOT IN

Проверяет, находится ли значение в списке результатов подзапроса.

```sql
-- Сотрудники из определённых департаментов
SELECT name, dept_id
FROM employees
WHERE dept_id IN (10, 20, 30);

-- Динамический список
SELECT name
FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE location = 'Moscow');

-- Исключение
SELECT name
FROM employees
WHERE dept_id NOT IN (SELECT dept_id FROM employees WHERE salary > 100000);
```

### EXISTS / NOT EXISTS

Проверяет существование строк, возвращаемых подзапросом.

```sql
-- Клиенты, у которых есть заказы
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Клиенты без заказов
SELECT customer_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### ANY / ALL

Сравнение с любым или всеми значениями из подзапроса.

```sql
-- Зарплата больше минимальной в любом департаменте
SELECT name, salary
FROM employees
WHERE salary > ANY (
    SELECT MIN(salary) FROM employees GROUP BY dept_id
);

-- Зарплата больше максимальной во всех департаментах
SELECT name, salary
FROM employees
WHERE salary > ALL (
    SELECT MAX(salary) FROM employees GROUP BY dept_id
);
```

## 💡 Практические примеры

### Пример 1: Топ продуктов по продажам

```sql
SELECT 
    p.product_name,
    p.category,
    (SELECT SUM(oi.quantity) FROM order_items oi WHERE oi.product_id = p.id) AS total_sold
FROM products p
ORDER BY total_sold DESC
LIMIT 10;
```

### Пример 2: Сотрудники с максимальной зарплатой в каждом департаменте

```sql
SELECT e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (
    SELECT MAX(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e.dept_id
);
```

### Пример 3: Клиенты с общим объёмом заказов выше среднего

```sql
SELECT 
    c.customer_name,
    total_spent
FROM customers c
INNER JOIN (
    SELECT 
        customer_id,
        SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
) AS customer_totals ON c.id = customer_totals.customer_id
WHERE total_spent > (
    SELECT AVG(total_spent) FROM (
        SELECT SUM(total_amount) AS total_spent
        FROM orders
        GROUP BY customer_id
    ) AS all_totals
);
```

### Пример 4: Обновление данных на основе подзапроса

```sql
-- Увеличить зарплату сотрудникам с зарплатой ниже средней
UPDATE employees
SET salary = salary * 1.1
WHERE salary < (SELECT AVG(salary) FROM employees);
```

### Пример 5: Удаление дубликатов

```sql
DELETE FROM orders o1
WHERE EXISTS (
    SELECT 1 FROM orders o2
    WHERE o2.customer_id = o1.customer_id
      AND o2.order_date = o1.order_date
      AND o2.id < o1.id
);
```

## ⚠️ Частые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| Подзапрос возвращает несколько строк для одиночного сравнения | Ошибка SQL | Используйте IN, EXISTS или ограничьте результат |
| NULL в NOT IN | Пустой результат | Обрабатывайте NULL явно или используйте NOT EXISTS |
| Непроизводительные коррелированные подзапросы | Медленное выполнение | Используйте JOIN или CTE |
| Глубокая вложенность | Сложность чтения | Разбейте на CTE |

## 🎯 Коррелированные vs Некоррелированные подзапросы

### Некоррелированный подзапрос

Выполняется один раз независимо от внешнего запроса.

```sql
-- Выполняется один раз
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### Коррелированный подзапрос

Выполняется для каждой строки внешнего запроса (может быть медленным).

```sql
-- Выполняется для каждой строки
SELECT name, salary, dept_id
FROM employees e
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees 
    WHERE dept_id = e.dept_id
);
```

**Оптимизация через JOIN:**

```sql
-- Более эффективная версия
SELECT e.name, e.salary, e.dept_id
FROM employees e
INNER JOIN (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) AS dept_avg ON e.dept_id = dept_avg.dept_id
WHERE e.salary > dept_avg.avg_salary;
```

## 📊 Сравнение подходов

| Задача | Подзапрос | JOIN | CTE |
|--------|-----------|------|-----|
| Простая фильтрация | ✅ Отлично | ⚠️ Избыточно | ⚠️ Избыточно |
| Проверка существования | ✅ EXISTS | ⚠️ DISTINCT | ✅ CTE |
| Агрегация для сравнения | ✅ Хорошо | ✅ Отлично | ✅ Отлично |
| Множественные использования | ❌ Плохо | ⚠️ Повторение | ✅ Отлично |
| Читаемость | ⚠️ Средняя | ✅ Хорошая | ✅ Отличная |

## ➡️ Что дальше?

Изучите [оконные функции](./window-functions.md) для ещё более мощной аналитики!
