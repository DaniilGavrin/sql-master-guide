# INSERT: Добавление данных

## Синтаксис

```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
```

## Примеры

### Вставка одной строки
```sql
INSERT INTO users (name, email)
VALUES ('Иван', 'ivan@example.com');
```

### Вставка нескольких строк
```sql
INSERT INTO users (name, email)
VALUES 
    ('Петр', 'petr@example.com'),
    ('Анна', 'anna@example.com');
```

## Частые ошибки
- Не соответствие количества колонок и значений
- Нарушение ограничений (NOT NULL, UNIQUE)

[← Назад к ORDER BY](order-by.md) | [Далее: UPDATE →](update.md)
