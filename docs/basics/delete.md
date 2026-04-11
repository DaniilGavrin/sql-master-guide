# DELETE: Удаление данных

## Синтаксис

```sql
DELETE FROM table_name
WHERE condition;
```

## Примеры

### Удаление одной записи
```sql
DELETE FROM users
WHERE id = 1;
```

### Удаление по условию
```sql
DELETE FROM orders
WHERE status = 'cancelled';
```

### Удаление всех записей (осторожно!)
```sql
DELETE FROM users;
```

## TRUNCATE vs DELETE

| Операция | Скорость | WHERE | Возврат места |
|----------|----------|-------|---------------|
| DELETE   | Медленнее| Да    | Постепенно    |
| TRUNCATE | Быстрее  | Нет   | Сразу         |

## Частые ошибки
- **Забывчивость с WHERE**: удаление всех строк
- **Нарушение внешних ключей**: невозможность удаления связанных записей

[← Назад к UPDATE](update.md) | [Далее: Продвинутые темы →](../advanced/coming-soon.md)
