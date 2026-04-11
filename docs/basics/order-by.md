# Сортировка данных (ORDER BY)

## Основы сортировки

Оператор `ORDER BY` используется для сортировки результатов запроса по одному или нескольким столбцам.

## Синтаксис

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
```

## Направления сортировки

- **ASC** — по возрастанию (по умолчанию)
- **DESC** — по убыванию

## Примеры использования

### Сортировка по одному столбцу

```sql
-- Сортировка по имени (A-Z)
SELECT * FROM users ORDER BY first_name ASC;

-- Сортировка по убыванию
SELECT * FROM products ORDER BY price DESC;
```

### Сортировка по датам

```sql
-- Последние заказы сначала
SELECT * FROM orders ORDER BY order_date DESC;
```

## Множественная сортировка

```sql
-- Сначала по городу, затем по зарплате внутри города
SELECT * FROM employees
ORDER BY city ASC, salary DESC;
```

## Сортировка с LIMIT

```sql
-- Top 5 самых дорогих продуктов
SELECT * FROM products
ORDER BY price DESC
LIMIT 5;
```

## Практические примеры

### Топ товаров по продажам

```sql
SELECT 
    product_name,
    SUM(quantity) AS total_sold
FROM order_items
GROUP BY product_name
ORDER BY total_sold DESC
LIMIT 10;
```

## Частые ошибки

❌ **Неправильно:**
```sql
ORDER BY;  -- Отсутствует столбец
```

✅ **Правильно:**
```sql
ORDER BY created_at;
```

## Что дальше?

- [JOIN операции](../advanced/joins.md) — соединение таблиц
- [Агрегатные функции](../advanced/aggregates.md) — анализ данных

---

**Совет:** Всегда используйте `ORDER BY` вместе с `LIMIT` для пагинации — без сортировки порядок строк не гарантирован!
