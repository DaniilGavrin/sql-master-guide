# Транзакции

Транзакция — это последовательность операций с базой данных, которая выполняется как единое целое. Либо все операции выполняются успешно, либо ни одна не выполняется.

## 🔑 ACID свойства

Надёжные транзакции гарантируют четыре свойства (ACID):

### 1. Atomicity (Атомарность)

Все операции транзакции выполняются или не выполняются вообще.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Если вторая операция не выполнится, первая будет отменена
```

### 2. Consistency (Согласованность)

Транзакция переводит базу из одного согласованного состояния в другое.

```sql
-- Ограничение целостности
ALTER TABLE accounts ADD CONSTRAINT check_balance CHECK (balance >= 0);

-- Транзакция не нарушит это ограничение
BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE id = 1; -- Ошибка, если balance < 200
COMMIT;
```

### 3. Isolation (Изоляция)

Параллельные транзакции не влияют друг на друга.

```sql
-- Транзакция 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- 1000

-- Транзакция 2 (параллельно)
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- Транзакция 1 (в зависимости от уровня изоляции)
SELECT balance FROM accounts WHERE id = 1; -- 1000 или 900
COMMIT;
```

### 4. Durability (Долговечность)

После COMMIT изменения сохраняются навсегда, даже при сбое.

```sql
BEGIN;
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;
-- После этого изменения сохранены даже при отключении питания
```

## 🎮 Управление транзакциями

### Основные команды

```sql
-- Начало транзакции
BEGIN;
-- или
START TRANSACTION;

-- Выполнение операций
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
INSERT INTO transactions (from_id, to_id, amount) VALUES (1, 2, 100);

-- Подтверждение изменений
COMMIT;

-- Отмена всех изменений
ROLLBACK;

-- Точка сохранения (можно откатиться до неё)
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = 0 WHERE id = 3;
ROLLBACK TO my_savepoint; -- Отменяет только последнее изменение
```

### Пример с точкой сохранения

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT after_first_update;

UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Что-то пошло не так...
ROLLBACK TO after_first_update;

-- Исправленная операция
UPDATE accounts SET balance = balance + 100 WHERE id = 3;

COMMIT;
```

## 🔒 Уровни изоляции

Уровни изоляции определяют, насколько транзакции видят изменения друг друга.

### 1. Read Uncommitted (Чтение незафиксированных данных)

Самый низкий уровень. Возможны "грязные" чтения.

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Транзакция 1
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
-- Ещё не COMMIT

-- Транзакция 2
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- Видит 900 (грязное чтение!)
COMMIT;
```

**Проблемы:** Грязное чтение (Dirty Read)

### 2. Read Committed (Чтение зафиксированных данных)

Уровень по умолчанию в PostgreSQL и Oracle.

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Только зафиксированные данные видны
```

**Проблемы:** Неповторяющееся чтение (Non-repeatable Read)

### 3. Repeatable Read (Повторяемое чтение)

Гарантирует, что повторный запрос вернёт те же данные.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Транзакция 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- 1000

-- Транзакция 2
BEGIN;
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- Транзакция 1
SELECT balance FROM accounts WHERE id = 1; -- Всё ещё 1000!
COMMIT;
```

**Проблемы:** Фантомное чтение (Phantom Read) — в некоторых СУБД

### 4. Serializable (Сериализуемый)

Самый строгий уровень. Полная изоляция.

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Транзакции выполняются последовательно
```

**Проблемы:** Нет, но возможна ошибка сериализации

## 📊 Сравнение уровней изоляции

| Уровень | Грязное чтение | Неповторяющееся чтение | Фантомное чтение | Производительность |
|---------|---------------|----------------------|-----------------|-------------------|
| Read Uncommitted | ✅ Возможно | ✅ Возможно | ✅ Возможно | ⚡⚡⚡⚡ |
| Read Committed | ❌ Нет | ✅ Возможно | ✅ Возможно | ⚡⚡⚡ |
| Repeatable Read | ❌ Нет | ❌ Нет | ✅ Возможно* | ⚡⚡ |
| Serializable | ❌ Нет | ❌ Нет | ❌ Нет | ⚡ |

*В PostgreSQL Repeatable Read предотвращает и фантомное чтение

## 💡 Практические примеры

### Пример 1: Перевод денег

```sql
BEGIN;

-- Проверка баланса
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- Списание
UPDATE accounts 
SET balance = balance - 1000 
WHERE id = 1 AND balance >= 1000;

-- Если ничего не обновилось, откат
-- (проверяем количество затронутых строк)

-- Зачисление
UPDATE accounts 
SET balance = balance + 1000 
WHERE id = 2;

-- Запись в историю
INSERT INTO transaction_log (from_id, to_id, amount, created_at)
VALUES (1, 2, 1000, NOW());

COMMIT;
```

### Пример 2: Бронирование мест

```sql
BEGIN;

-- Проверка доступности с блокировкой
SELECT seat_number, is_booked 
FROM seats 
WHERE flight_id = 123 AND seat_number = '15A'
FOR UPDATE;

-- Бронирование
UPDATE seats 
SET is_booked = TRUE, booked_by = 456 
WHERE flight_id = 123 AND seat_number = '15A' AND is_booked = FALSE;

-- Если строка не обновилась, место уже занято
ROLLBACK; -- или COMMIT без изменений
```

### Пример 3: Инвентаризация

```sql
BEGIN;

-- Резервирование товара
UPDATE inventory 
SET quantity = quantity - 5 
WHERE product_id = 789 AND quantity >= 5;

-- Проверка успешности
-- Если quantity < 5, товар недоступен

-- Создание заказа
INSERT INTO orders (product_id, quantity, status)
VALUES (789, 5, 'pending');

COMMIT;
```

## ⚠️ Распространённые проблемы

### 1. Взаимная блокировка (Deadlock)

Две транзакции ждут друг друга.

```sql
-- Транзакция 1
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 1;
UPDATE accounts SET balance = 200 WHERE id = 2; -- Ждёт транзакцию 2
COMMIT;

-- Транзакция 2
BEGIN;
UPDATE accounts SET balance = 300 WHERE id = 2;
UPDATE accounts SET balance = 400 WHERE id = 1; -- Ждёт транзакцию 1
COMMIT;

-- DEADLOCK! Одна из транзакций будет отменена
```

**Решение:** Всегда обновляйте таблицы в одинаковом порядке

### 2. Длительные транзакции

```sql
-- Плохо: транзакция открыта слишком долго
BEGIN;
SELECT * FROM large_table; -- Долгий запрос
-- ... обработка в приложении ...
UPDATE accounts SET balance = 100;
COMMIT;

-- Хорошо: минимизируйте время транзакции
SELECT * FROM large_table; -- Вне транзакции
-- ... обработка ...
BEGIN;
UPDATE accounts SET balance = 100;
COMMIT;
```

### 3. Забытый COMMIT/ROLLBACK

```python
# Плохо: нет явного завершения
conn.begin()
cursor.execute("UPDATE accounts SET balance = 100")
# Забыли conn.commit() или conn.rollback()

# Хорошо: используйте контекстный менеджер
with conn.begin():
    cursor.execute("UPDATE accounts SET balance = 100")
# Автоматический commit или rollback при ошибке
```

## 🎯 Блокировки

### FOR UPDATE

Блокирует строки для обновления.

```sql
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- Другие транзакции не могут изменить эту строку до COMMIT
```

### FOR SHARE

Блокирует строки только от изменения, но разрешает чтение.

```sql
SELECT * FROM accounts WHERE id = 1 FOR SHARE;
```

### SKIP LOCKED

Пропускает заблокированные строки.

```sql
SELECT * FROM tasks 
WHERE status = 'pending' 
FOR UPDATE SKIP LOCKED 
LIMIT 1;
-- Получит первую незаблокированную задачу
```

### NOWAIT

Не ждёт блокировку, сразу возвращает ошибку.

```sql
SELECT * FROM accounts 
WHERE id = 1 
FOR UPDATE NOWAIT;
-- Ошибка, если строка заблокирована
```

## 📈 Мониторинг транзакций

### PostgreSQL

```sql
-- Активные транзакции
SELECT 
    pid,
    usename,
    state,
    query,
    age(clock_timestamp(), xact_start) AS duration
FROM pg_stat_activity
WHERE state != 'idle';

-- Блокировки
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocking_locks.pid AS blocking_pid,
    blocked_activity.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;
```

## 🎯 Лучшие практики

1. ✅ Держите транзакции короткими
2. ✅ Всегда завершайте транзакции (COMMIT/ROLLBACK)
3. ✅ Обрабатывайте ошибки и делайте ROLLBACK
4. ✅ Используйте один порядок обновления таблиц
5. ✅ Выбирайте подходящий уровень изоляции
6. ✅ Избегайте пользовательского ввода внутри транзакций
7. ✅ Используйте точки сохранения для частичного отката
8. ✅ Мониторьте длительные транзакции и блокировки

## ➡️ Что дальше?

Изучите [хранимые процедуры и функции](./procedures.md) для автоматизации логики!
