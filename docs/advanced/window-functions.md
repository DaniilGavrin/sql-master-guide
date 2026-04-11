# Оконные функции (Window Functions)

Оконные функции выполняют вычисления над набором строк, связанных с текущей строкой, но в отличие от агрегатных функций, они не группируют строки в один результат.

## 📊 Синтаксис оконных функций

```sql
функция_окна(аргументы) OVER (
    [PARTITION BY столбец]
    [ORDER BY столбец]
    [ROWS/RANGE между_строки]
)
```

- **PARTITION BY** — разбивает результат на группы (как GROUP BY, но без агрегации)
- **ORDER BY** — сортирует строки внутри окна
- **ROWS/RANGE** — определяет диапазон строк для вычисления

## 🔢 Нумерация и ранжирование

### ROW_NUMBER()

Присваивает уникальный порядковый номер каждой строке.

```sql
SELECT 
    name,
    salary,
    dept_id,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;
```

**Результат:**

| name | salary | dept_id | rank |
|------|--------|---------|------|
| Директор | 150000 | 10 | 1 |
| Менеджер | 120000 | 20 | 2 |
| Аналитик | 90000 | 20 | 3 |

### RANK() и DENSE_RANK()

- **RANK()** — присваивает одинаковый ранг равным значениям, следующий ранг пропускается
- **DENSE_RANK()** — присваивает одинаковый ранг равным значениям, следующий ранг не пропускается

```sql
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;
```

**Пример с одинаковыми зарплатами:**

| name | salary | rank | dense_rank |
|------|--------|------|------------|
| A | 100000 | 1 | 1 |
| B | 100000 | 1 | 1 |
| C | 90000 | 3 | 2 |
| D | 80000 | 4 | 3 |

### NTILE(n)

Разбивает строки на n групп примерно одинакового размера.

```sql
-- Разделить сотрудников на 4 квартеля по зарплате
SELECT 
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;
```

## 📈 Агрегатные оконные функции

Агрегатные функции можно использовать как оконные.

### Накопительный итог (Running Total)

```sql
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders;
```

### Скользящее среднее

```sql
SELECT 
    order_date,
    amount,
    AVG(amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7days
FROM orders;
```

### Агрегаты с PARTITION BY

```sql
SELECT 
    name,
    salary,
    dept_id,
    AVG(salary) OVER (PARTITION BY dept_id) AS avg_dept_salary,
    salary - AVG(salary) OVER (PARTITION BY dept_id) AS diff_from_avg
FROM employees;
```

## 🔀 Функции смещения

### LAG() и LEAD()

Доступ к предыдущим и следующим строкам.

```sql
-- Сравнение с предыдущим месяцем
SELECT 
    month,
    sales,
    LAG(sales, 1) OVER (ORDER BY month) AS prev_month_sales,
    sales - LAG(sales, 1) OVER (ORDER BY month) AS change
FROM monthly_sales;

-- Прогноз на следующий период
SELECT 
    month,
    sales,
    LEAD(sales, 1) OVER (ORDER BY month) AS next_month_forecast
FROM monthly_sales;
```

### FIRST_VALUE() и LAST_VALUE()

Получение первого и последнего значения в окне.

```sql
SELECT 
    name,
    hire_date,
    dept_id,
    FIRST_VALUE(name) OVER (
        PARTITION BY dept_id 
        ORDER BY hire_date
    ) AS first_hire_in_dept,
    LAST_VALUE(name) OVER (
        PARTITION BY dept_id 
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_hire_in_dept
FROM employees;
```

## 💡 Практические примеры

### Пример 1: Топ-3 сотрудника в каждом департаменте

```sql
SELECT name, dept_id, salary, rank_in_dept
FROM (
    SELECT 
        name,
        dept_id,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY dept_id 
            ORDER BY salary DESC
        ) AS rank_in_dept
    FROM employees
) AS ranked
WHERE rank_in_dept <= 3;
```

### Пример 2: Анализ изменений зарплаты

```sql
SELECT 
    name,
    year,
    salary,
    LAG(salary) OVER (PARTITION BY name ORDER BY year) AS prev_salary,
    salary - LAG(salary) OVER (PARTITION BY name ORDER BY year) AS change,
    ROUND(
        100.0 * (salary - LAG(salary) OVER (PARTITION BY name ORDER BY year)) 
        / LAG(salary) OVER (PARTITION BY name ORDER BY year), 
        2
    ) AS change_percent
FROM employee_salaries
ORDER BY name, year;
```

### Пример 3: Накопительные продажи по месяцам

```sql
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    SUM(total_amount) AS monthly_sales,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS running_total,
    AVG(SUM(total_amount)) OVER (
        ORDER BY DATE_TRUNC('month', order_date)
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS three_month_avg
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### Пример 4: Выявление аномалий

```sql
-- Найти заказы, превышающие средний более чем на 2 стандартных отклонения
SELECT order_id, customer_id, total_amount, avg_amount, std_dev, z_score
FROM (
    SELECT 
        order_id,
        customer_id,
        total_amount,
        AVG(total_amount) OVER () AS avg_amount,
        STDDEV(total_amount) OVER () AS std_dev,
        (total_amount - AVG(total_amount) OVER ()) 
        / NULLIF(STDDEV(total_amount) OVER (), 0) AS z_score
    FROM orders
) AS stats
WHERE ABS(z_score) > 2;
```

### Пример 5: Сравнение с лучшим показателем

```sql
SELECT 
    salesperson,
    region,
    sales,
    MAX(sales) OVER (PARTITION BY region) AS best_in_region,
    ROUND(
        100.0 * sales / MAX(sales) OVER (PARTITION BY region), 
        1
    ) AS percent_of_best
FROM sales_data;
```

## ⚠️ Частые ошибки

| Ошибка | Проблема | Решение |
|--------|----------|---------|
| Забытый ORDER BY в LAST_VALUE | Возвращает только до текущей строки | Добавьте `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` |
| Неправильное понимание RANGE vs ROWS | Разные результаты | Используйте ROWS для подсчёта строк, RANGE для значений |
| Производительность на больших данных | Медленное выполнение | Индексируйте столбцы в PARTITION BY и ORDER BY |
| Путаница с NULL | Неожиданные результаты | Используйте COALESCE для обработки NULL |

## 🎯 Окно по умолчанию

Если не указано иначе, окно включает:
- Все строки партиции (без PARTITION BY — все строки результата)
- От первой строки до текущей (при ORDER BY)
- Или все строки (без ORDER BY)

```sql
-- Эквивалентны:
SUM(salary) OVER ()
SUM(salary) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

## 📊 Сравнение функций ранжирования

| Функция | Одинаковые значения | Следующий ранг | Пример |
|---------|-------------------|----------------|--------|
| ROW_NUMBER | Уникальные номера | +1 | 1, 2, 3, 4 |
| RANK | Одинаковый ранг | Пропуск | 1, 1, 3, 4 |
| DENSE_RANK | Одинаковый ранг | Без пропуска | 1, 1, 2, 3 |
| NTILE(n) | Распределение по группам | - | 1, 1, 2, 2 (для n=2) |

## ➡️ Что дальше?

Изучите [CTE](./cte.md) для создания читаемых сложных запросов!
