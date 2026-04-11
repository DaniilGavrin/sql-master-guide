# JOIN — Объединение таблиц

Оператор `JOIN` позволяет объединять строки из двух или более таблиц на основе связанного столбца между ними. Это одна из самых мощных возможностей SQL.

## 📋 Типы JOIN

### 1. INNER JOIN (Внутреннее соединение)

Возвращает только те строки, для которых есть совпадение в обеих таблицах.

```sql
SELECT employees.name, departments.dept_name
FROM employees
INNER JOIN departments ON employees.dept_id = departments.id;
```

**Пример данных:**

| employees | | departments | |
|-----------|-|-------------|-|
| id | name | dept_id | id | dept_name |
| 1 | Иван | 10 | 10 | Бухгалтерия |
| 2 | Мария | 20 | 20 | IT |
| 3 | Петр | 30 | 30 | Продажи |

**Результат:**

| name | dept_name |
|------|-----------|
| Иван | Бухгалтерия |
| Мария | IT |
| Петр | Продажи |

### 2. LEFT JOIN (Левое соединение)

Возвращает все строки из левой таблицы и совпадающие строки из правой. Если совпадений нет, возвращаются NULL.

```sql
SELECT employees.name, departments.dept_name
FROM employees
LEFT JOIN departments ON employees.dept_id = departments.id;
```

**Результат (если у сотрудника нет департамента):**

| name | dept_name |
|------|-----------|
| Иван | Бухгалтерия |
| Мария | IT |
| Петр | Продажи |
| Анна | NULL |

### 3. RIGHT JOIN (Правое соединение)

Возвращает все строки из правой таблицы и совпадающие строки из левой.

```sql
SELECT employees.name, departments.dept_name
FROM employees
RIGHT JOIN departments ON employees.dept_id = departments.id;
```

### 4. FULL OUTER JOIN (Полное внешнее соединение)

Возвращает все строки из обеих таблиц. Поддерживается не всеми СУБД (PostgreSQL поддерживает, MySQL — нет).

```sql
SELECT employees.name, departments.dept_name
FROM employees
FULL OUTER JOIN departments ON employees.dept_id = departments.id;
```

### 5. CROSS JOIN (Декартово произведение)

Возвращает декартово произведение всех строк обеих таблиц.

```sql
SELECT * FROM table1 CROSS JOIN table2;
-- Или
SELECT * FROM table1, table2;
```

## 🔗 Условия соединения

### Соединение по нескольким условиям

```sql
SELECT e.name, d.dept_name, l.city
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id AND e.active = 1
INNER JOIN locations l ON d.location_id = l.id;
```

### Самосоединение (Self Join)

Используется для соединения таблицы с самой собой.

```sql
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

## ⚠️ Частые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| Забытое условие ON | Возвращается декартово произведение | Всегда указывайте условие JOIN |
| Неправильный тип JOIN | Потеря данных | Выбирайте тип соединения осознанно |
| Дубликаты в результатах | Несколько совпадений | Проверьте уникальность ключей |
| Путаница с NULL | LEFT JOIN может вернуть NULL | Используйте COALESCE для обработки |

## 💡 Практические примеры

### Пример 1: Отчёт по продажам

```sql
SELECT 
    c.customer_name,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.price
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
ORDER BY o.order_date DESC;
```

### Пример 2: Поиск сотрудников без департамента

```sql
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
WHERE d.id IS NULL;
```

### Пример 3: Подсчёт заказов по клиентам

```sql
SELECT 
    c.customer_name,
    COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.customer_name
ORDER BY order_count DESC;
```

## 🎯 Ключевые моменты

- **INNER JOIN** — только совпадающие записи
- **LEFT JOIN** — все записи слева + совпадения справа
- **RIGHT JOIN** — все записи справа + совпадения слева
- **FULL OUTER JOIN** — все записи из обеих таблиц
- Всегда указывайте условие `ON` для соединения
- Используйте алиасы таблиц для читаемости

## ➡️ Что дальше?

Изучите [агрегатные функции](./aggregates.md) для анализа объединённых данных!
