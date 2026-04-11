# UPDATE: Обновление данных

## Синтаксис

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

## Примеры

### Обновление одной записи
```sql
UPDATE users
SET email = 'new@example.com'
WHERE id = 1;
```

### Обновление нескольких полей
```sql
UPDATE products
SET price = 100, stock = 50
WHERE category = 'Electronics';
```

### Обновление всех записей (осторожно!)
```sql
UPDATE users
SET status = 'active';
```

## Частые ошибки
- **Забывчивость с WHERE**: обновление всех строк вместо нужных
- **Неправильные условия**: обновление не тех записей

[← Назад к INSERT](insert.md) | [Далее: DELETE →](delete.md)
