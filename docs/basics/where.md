# Фильтрация данных (WHERE)

## Основы фильтрации

Оператор `WHERE` позволяет фильтровать строки, возвращаемые запросом, на основе указанного условия.

## Синтаксис

```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

## Операторы сравнения

| Оператор | Описание | Пример |
|----------|----------|--------|
| `=` | Равно | `age = 25` |
| `<>` или `!=` | Не равно | `status != 'inactive'` |
| `>` | Больше | `price > 100` |
| `<` | Меньше | `age < 18` |
| `>=` | Больше или равно | `salary >= 50000` |
| `<=` | Меньше или равно | `quantity <= 10` |

## Логические операторы

### AND — логическое И

```sql
SELECT * FROM users
WHERE city = 'Москва' AND status = 'active';
```

### OR — логическое ИЛИ

```sql
SELECT * FROM users
WHERE city = 'Москва' OR city = 'Санкт-Петербург';
```

### NOT — логическое НЕ

```sql
SELECT * FROM users
WHERE NOT status = 'inactive';
```

## Специальные операторы

### BETWEEN — диапазон значений

```sql
SELECT * FROM products
WHERE price BETWEEN 100 AND 500;
```

### IN — список значений

```sql
SELECT * FROM users
WHERE city IN ('Москва', 'Санкт-Петербург', 'Казань');
```

### LIKE — поиск по шаблону

| Шаблон | Описание | Пример |
|--------|----------|--------|
| `%` | Любое количество символов | `'Иван%'` |
| `_` | Один любой символ | `'А_ексей'` |

```sql
-- Имена, начинающиеся на "Иван"
SELECT * FROM users WHERE first_name LIKE 'Иван%';

-- Имена, заканчивающиеся на "ов"
SELECT * FROM users WHERE last_name LIKE '%ов';
```

### IS NULL / IS NOT NULL

```sql
-- Пользователи без email
SELECT * FROM users WHERE email IS NULL;

-- Пользователи с заполненным email
SELECT * FROM users WHERE email IS NOT NULL;
```

!!! warning "Внимание"
    Для проверки на NULL используйте `IS NULL` или `IS NOT NULL`, а не `= NULL`.

## Практические примеры

### Фильтрация заказов

```sql
SELECT * FROM orders
WHERE 
    order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND total_amount > 1000
    AND status = 'completed';
```

## Частые ошибки

❌ **Неправильно:**
```sql
WHERE email = NULL;
```

✅ **Правильно:**
```sql
WHERE email IS NULL;
```

## Что дальше?

- [Сортировка](order-by.md) — упорядочивание результатов
- [JOIN операции](../advanced/joins.md) — соединение таблиц

---

**Совет:** Используйте скобки для группировки сложных условий — это улучшает читаемость и предотвращает ошибки.
