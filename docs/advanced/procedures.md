# Хранимые процедуры и функции

Хранимые процедуры и функции позволяют сохранять SQL-код на сервере базы данных для повторного использования, автоматизации и инкапсуляции логики.

## 📋 Различия

| Характеристика | Функция | Процедура |
|---------------|---------|-----------|
| Возврат значения | ✅ Обязательно | ❌ Необязательно |
| Использование в запросах | ✅ Да | ❌ Нет |
| Транзакции | ⚠️ Ограничения | ✅ Полная поддержка |
| Вызов | `SELECT func()` | `CALL proc()` |

## 🔧 Создание функций

### Простая функция

```sql
CREATE OR REPLACE FUNCTION get_employee_name(emp_id INTEGER)
RETURNS VARCHAR(255) AS $$
DECLARE
    emp_name VARCHAR(255);
BEGIN
    SELECT name INTO emp_name
    FROM employees
    WHERE id = emp_id;
    
    RETURN emp_name;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT get_employee_name(123);
```

### Функция с параметрами

```sql
CREATE OR REPLACE FUNCTION calculate_bonus(
    base_salary NUMERIC,
    performance_rating INTEGER,
    years_of_service INTEGER
)
RETURNS NUMERIC AS $$
DECLARE
    bonus NUMERIC;
BEGIN
    bonus := base_salary * 0.1; -- Базовый бонус 10%
    
    -- Надбавка за рейтинг
    IF performance_rating >= 5 THEN
        bonus := bonus * 2;
    ELSIF performance_rating >= 4 THEN
        bonus := bonus * 1.5;
    END IF;
    
    -- Надбавка за стаж
    IF years_of_service > 10 THEN
        bonus := bonus + base_salary * 0.05;
    END IF;
    
    RETURN bonus;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT 
    name,
    salary,
    calculate_bonus(salary, rating, EXTRACT(YEAR FROM AGE(NOW(), hire_date))) AS bonus
FROM employees;
```

### Функция возвращающая таблицу

```sql
CREATE OR REPLACE FUNCTION get_department_stats(dept_id_param INTEGER)
RETURNS TABLE (
    employee_name VARCHAR(255),
    employee_salary NUMERIC,
    dept_avg_salary NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.name,
        e.salary,
        AVG(e.salary) OVER () AS avg_salary
    FROM employees e
    WHERE e.dept_id = dept_id_param;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT * FROM get_department_stats(10);
```

## 🔧 Создание процедур

### Простая процедура

```sql
CREATE OR REPLACE PROCEDURE update_salary(
    emp_id INTEGER,
    increase_percent NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE employees
    SET salary = salary * (1 + increase_percent / 100)
    WHERE id = emp_id;
    
    COMMIT;
END;
$$;

-- Вызов
CALL update_salary(123, 10); -- Увеличить зарплату на 10%
```

### Процедура с транзакцией

```sql
CREATE OR REPLACE PROCEDURE transfer_money(
    from_account INTEGER,
    to_account INTEGER,
    amount NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    current_balance NUMERIC;
BEGIN
    -- Проверка баланса
    SELECT balance INTO current_balance
    FROM accounts
    WHERE id = from_account
    FOR UPDATE;
    
    IF current_balance < amount THEN
        RAISE EXCEPTION 'Недостаточно средств';
    END IF;
    
    -- Списание
    UPDATE accounts
    SET balance = balance - amount
    WHERE id = from_account;
    
    -- Зачисление
    UPDATE accounts
    SET balance = balance + amount
    WHERE id = to_account;
    
    -- Логирование
    INSERT INTO transaction_log (from_id, to_id, amount, created_at)
    VALUES (from_account, to_account, amount, NOW());
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
$$;

-- Вызов
CALL transfer_money(1, 2, 1000);
```

## 📊 Типы языков

### SQL функции

Простые функции на чистом SQL.

```sql
CREATE OR REPLACE FUNCTION get_total_sales()
RETURNS NUMERIC AS $$
    SELECT SUM(total_amount) FROM orders;
$$ LANGUAGE SQL;
```

### PL/pgSQL

Процедурный язык PostgreSQL (как PL/SQL в Oracle).

```sql
CREATE OR REPLACE FUNCTION factorial(n INTEGER)
RETURNS INTEGER AS $$
DECLARE
    result INTEGER := 1;
    i INTEGER;
BEGIN
    FOR i IN 1..n LOOP
        result := result * i;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### Другие языки

PostgreSQL поддерживает Python, Perl, Tcl, C и другие.

```sql
-- Требуется расширение plpython3u
CREATE EXTENSION IF NOT EXISTS plpython3u;

CREATE OR REPLACE FUNCTION max_value(a INTEGER, b INTEGER)
RETURNS INTEGER AS $$
    return max(a, b)
$$ LANGUAGE plpython3u;
```

## 💡 Практические примеры

### Пример 1: Валидация данных

```sql
CREATE OR REPLACE FUNCTION validate_email(email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
END;
$$ LANGUAGE plpgsql;

-- Использование в CHECK ограничении
ALTER TABLE users 
ADD CONSTRAINT check_email_format 
CHECK (validate_email(email));
```

### Пример 2: Автоматическое ведение истории

```sql
-- Таблица истории
CREATE TABLE employee_history (
    employee_id INTEGER,
    old_salary NUMERIC,
    new_salary NUMERIC,
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by VARCHAR(255)
);

-- Триггерная функция
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salary IS DISTINCT FROM NEW.salary THEN
        INSERT INTO employee_history (
            employee_id,
            old_salary,
            new_salary,
            changed_by
        ) VALUES (
            NEW.id,
            OLD.salary,
            NEW.salary,
            current_setting('app.current_user', TRUE)
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер
CREATE TRIGGER trg_salary_change
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION log_salary_change();
```

### Пример 3: Генерация отчёта

```sql
CREATE OR REPLACE FUNCTION generate_monthly_report(
    report_year INTEGER,
    report_month INTEGER
)
RETURNS TABLE (
    department VARCHAR(255),
    total_sales NUMERIC,
    order_count BIGINT,
    avg_order_value NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.dept_name,
        COALESCE(SUM(o.total_amount), 0),
        COUNT(o.id),
        COALESCE(AVG(o.total_amount), 0)
    FROM departments d
    LEFT JOIN orders o ON d.id = o.dept_id
        AND EXTRACT(YEAR FROM o.order_date) = report_year
        AND EXTRACT(MONTH FROM o.order_date) = report_month
    GROUP BY d.id, d.dept_name
    ORDER BY total_sales DESC;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT * FROM generate_monthly_report(2024, 1);
```

### Пример 4: Массовое обновление

```sql
CREATE OR REPLACE PROCEDURE apply_annual_raise(
    min_performance INTEGER DEFAULT 3
)
LANGUAGE plpgsql
AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE employees
    SET salary = CASE
        WHEN performance_rating >= 5 THEN salary * 1.15
        WHEN performance_rating >= 4 THEN salary * 1.10
        WHEN performance_rating >= 3 THEN salary * 1.05
        ELSE salary
    END
    WHERE performance_rating >= min_performance
      AND status = 'active';
    
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    
    RAISE NOTICE 'Обновлено зарплат: %', updated_count;
    
    COMMIT;
END;
$$;

-- Вызов
CALL apply_annual_raise(4); -- Только для сотрудников с рейтингом 4+
```

## ⚠️ Обработка ошибок

```sql
CREATE OR REPLACE FUNCTION safe_divide(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    IF b = 0 THEN
        RAISE WARNING 'Деление на ноль';
        RETURN NULL;
    END IF;
    
    RETURN a / b;
EXCEPTION
    WHEN DIVISION_BY_ZERO THEN
        RAISE NOTICE 'Поймано деление на ноль';
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE NOTICE 'Произошла ошибка: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

### Коды ошибок

```sql
BEGIN
    -- какой-то код
EXCEPTION
    WHEN UNIQUE_VIOLATION THEN
        -- Нарушение уникальности (23505)
    WHEN FOREIGN_KEY_VIOLATION THEN
        -- Нарушение внешнего ключа (23503)
    WHEN NOT_NULL_VIOLATION THEN
        -- Нарушение NOT NULL (23502)
    WHEN DEADLOCK_DETECTED THEN
        -- Взаимная блокировка (40P01)
    WHEN OTHERS THEN
        -- Любая другая ошибка
END;
```

## 🎯 Оптимизация

### Используйте правильный тип функции

```sql
-- Для простых вычислений — SQL
CREATE OR REPLACE FUNCTION add_tax(price NUMERIC)
RETURNS NUMERIC AS $$
    SELECT price * 1.20;
$$ LANGUAGE SQL;

-- Для сложной логики — PL/pgSQL
CREATE OR REPLACE FUNCTION calculate_complex_discount(...)
RETURNS NUMERIC AS $$
    -- сложная логика
$$ LANGUAGE plpgsql;
```

### Избегайте лишних запросов

```sql
-- Плохо: несколько запросов
CREATE OR REPLACE FUNCTION get_employee_info(emp_id INTEGER)
RETURNS VARCHAR AS $$
DECLARE
    emp_name VARCHAR;
    dept_name VARCHAR;
BEGIN
    SELECT name INTO emp_name FROM employees WHERE id = emp_id;
    SELECT d.name INTO dept_name 
    FROM departments d 
    INNER JOIN employees e ON d.id = e.dept_id 
    WHERE e.id = emp_id;
    RETURN emp_name || ' - ' || dept_name;
END;
$$ LANGUAGE plpgsql;

-- Хорошо: один запрос
CREATE OR REPLACE FUNCTION get_employee_info(emp_id INTEGER)
RETURNS VARCHAR AS $$
DECLARE
    result VARCHAR;
BEGIN
    SELECT e.name || ' - ' || d.name INTO result
    FROM employees e
    INNER JOIN departments d ON e.dept_id = d.id
    WHERE e.id = emp_id;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

## 📈 Мониторинг

### PostgreSQL

```sql
-- Список всех функций
SELECT 
    routine_name,
    routine_type,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'public';

-- Статистика вызовов (требуется pg_stat_statements)
SELECT 
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
WHERE query LIKE '%FUNCTION%'
ORDER BY total_time DESC;
```

## 🎯 Лучшие практики

1. ✅ Документируйте функции и процедуры
2. ✅ Используйте понятные имена
3. ✅ Обрабатывайте ошибки явно
4. ✅ Минимизируйте количество запросов
5. ✅ Используйте транзакции в процедурах
6. ✅ Тестируйте на граничных случаях
7. ✅ Избегайте бизнес-логики в функциях (переносите в приложение)
8. ✅ Версионируйте изменения функций

## ➡️ Что дальше?

Переходите к разделу [Справочник](../reference/index.md) для полного списка команд SQL!
