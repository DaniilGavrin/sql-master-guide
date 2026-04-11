# PostgreSQL: Установка и настройка

PostgreSQL — мощная объектно-реляционная СУБД с открытым исходным кодом, известная своей надёжностью, расширенными возможностями и соответствием стандартам SQL.

## Установка PostgreSQL

### Ubuntu/Debian

```bash
# Добавление репозитория
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Запуск службы
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Проверка статуса
sudo systemctl status postgresql
```

### CentOS/RHEL

```bash
# Добавление репозитория
sudo yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y

# Установка
sudo yum install postgresql13-server postgresql13-contrib -y

# Инициализация базы данных
sudo /usr/pgsql-13/bin/postgresql-13-setup initdb

# Запуск
sudo systemctl start postgresql-13
sudo systemctl enable postgresql-13
```

### macOS (Homebrew)

```bash
# Установка
brew install postgresql@13

# Запуск
brew services start postgresql@13

# Или ручной запуск
pg_ctl -D /usr/local/var/postgres start
```

### Windows

1. Скачайте установщик с [официального сайта](https://www.postgresql.org/download/windows/)
2. Запустите установщик (рекомендуется Stack Builder)
3. Выберите версию PostgreSQL
4. Укажите порт (по умолчанию 5432)
5. Задайте пароль для суперпользователя `postgres`
6. Установите pgAdmin (опционально)

## Первоначальная настройка

### Доступ к пользователю postgres

```bash
# Переключение на пользователя postgres
sudo -i -u postgres

# Подключение к psql
psql

# Выход
\q
exit
```

### Создание первого пользователя и базы данных

```bash
# Вход в psql от имени postgres
sudo -u postgres psql

-- Создание пользователя
CREATE USER myuser WITH PASSWORD 'mypassword';

-- Создание базы данных
CREATE DATABASE mydb OWNER myuser;

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

-- Выход
\q
```

## Подключение к PostgreSQL

### Через командную строку

```bash
# Локальное подключение
psql -U username -d database_name

# Подключение к удалённому серверу
psql -h hostname -U username -d database_name

# Подключение с портом
psql -h localhost -p 5432 -U username -d database_name

# Подключение по URI
psql postgresql://username:password@hostname:5432/database_name
```

### Основные команды psql

| Команда | Описание |
|---------|----------|
| `\h` | Справка по SQL командам |
| `\?` | Справка по командам psql |
| `\l` | Список баз данных |
| `\c dbname` | Подключиться к базе |
| `\dt` | Список таблиц |
| `\d table` | Описание таблицы |
| `\du` | Список пользователей |
| `\df` | Список функций |
| `\dn` | Список схем |
| `\dx` | Список расширений |
| `\s` | История команд |
| `\o file` | Вывод в файл |
| `\i file` | Выполнить файл |
| `\timing` | Включить тайминг |
| `\q` | Выйти из psql |

## Конфигурационные файлы

Основные файлы конфигурации находятся в `/etc/postgresql/<version>/main/` (Debian/Ubuntu) или `/var/lib/pgsql/<version>/data/` (RHEL/CentOS):

### postgresql.conf

Основные параметры:

```conf
# Порт
port = 5432

# Максимум подключений
max_connections = 100

# Размер буфера
shared_buffers = 256MB

# Рабочая память
work_mem = 4MB

# Кэш для JOIN и сортировок
effective_cache_size = 1GB

# Логирование
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'all'  # none, ddl, mod, all
log_min_duration_statement = 1000  # мс

# Автовакуум
autovacuum = on
autovacuum_max_workers = 3

# Репликация
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64
```

### pg_hba.conf (Host-Based Authentication)

Пример настройки доступа:

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Локальные подключения через socket
local   all             all                                     peer

# IPv4 локальные подключения
host    all             all             127.0.0.1/32            scram-sha-256

# IPv4 удалённые подключения
host    all             all             192.168.1.0/24          scram-sha-256

# IPv6 локальные подключения
host    all             all             ::1/128                 scram-sha-256
```

**Методы аутентификации:**
- `peer` — проверка имени ОС пользователя
- `trust` — без пароля (не рекомендуется для production)
- `scram-sha-256` — хэшированный пароль (рекомендуется)
- `md5` — устаревший метод хэширования
- `password` — пароль в открытом виде (не рекомендуется)

После изменений перезагрузите PostgreSQL:

```bash
sudo systemctl restart postgresql
# или
sudo systemctl reload postgresql  # без остановки
```

## Управление пользователями и правами

```sql
-- Создание роли (пользователя)
CREATE ROLE username WITH LOGIN PASSWORD 'password';
CREATE USER username WITH LOGIN PASSWORD 'password';  -- алиас

-- Создание роли с правами суперпользователя
CREATE ROLE admin WITH SUPERUSER LOGIN PASSWORD 'password';

-- Создание роли только для чтения
CREATE ROLE reader WITH LOGIN PASSWORD 'password';

-- Предоставление прав на БД
GRANT CONNECT ON DATABASE mydb TO reader;
GRANT ALL PRIVILEGES ON DATABASE mydb TO username;

-- Переключение на базу
\c mydb

-- Права на схемы
GRANT USAGE ON SCHEMA public TO reader;
GRANT ALL ON SCHEMA public TO username;

-- Права на таблицы
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;

-- Права на последовательности
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO username;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO username;

-- Права на функции
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO reader;

-- Применение прав к будущим объектам
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO username;

-- Изменение пароля
ALTER USER username WITH PASSWORD 'newpassword';

-- Блокировка пользователя
ALTER USER username WITH NOLOGIN;

-- Удаление пользователя
DROP USER username;

-- Просмотр ролей
\du

-- Просмотр прав
\dp
```

## Резервное копирование и восстановление

### Создание бэкапа

```bash
# Бэкап всей кластерной системы
pg_dumpall -U postgres > backup.sql

# Бэкап конкретной базы
pg_dump -U username -d database_name > db_backup.sql

# Бэкап в формате custom (для выборочного восстановления)
pg_dump -U username -d database_name -F c -f db_backup.dump

# Бэкап только схемы
pg_dump -U username -d database_name --schema-only > schema.sql

# Бэкап только данных
pg_dump -U username -d database_name --data-only > data.sql

# Бэкап с сжатием
pg_dump -U username -d database_name | gzip > db_backup.sql.gz
```

### Восстановление из бэкапа

```bash
# Восстановление из SQL файла
psql -U username -d database_name < db_backup.sql

# Восстановление из custom формата
pg_restore -U username -d database_name db_backup.dump

# Восстановление только схемы
pg_restore -U username -d database_name --schema-only db_backup.dump

# Восстановление только данных
pg_restore -U username -d database_name --data-only db_backup.dump

# Восстановление из сжатого файла
gunzip < db_backup.sql.gz | psql -U username -d database_name
```

### Point-in-Time Recovery (PITR)

Настройка непрерывного архивирования:

```conf
# postgresql.conf
archive_mode = on
archive_command = 'cp %p /path/to/archive/%f'
```

## Особенности PostgreSQL

### Расширения (Extensions)

```sql
-- Просмотр доступных расширений
SELECT * FROM pg_available_extensions;

-- Просмотр установленных расширений
\dx

-- Установка расширения
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS postgis;  -- для геоданных

-- Удаление расширения
DROP EXTENSION IF EXISTS extension_name;
```

**Популярные расширения:**
- `pg_stat_statements` — статистика запросов
- `uuid-ossp` — генерация UUID
- `hstore` — хранение пар ключ-значение
- `postgis` — геопространственные данные
- `pg_trgm` — триграммы для поиска
- `citext` — регистронезависимый текст

### Типы таблиц

```sql
-- Обычная таблица
CREATE TABLE users (id INT, name TEXT);

-- Временная таблица (существует в рамках сессии)
CREATE TEMP TABLE temp_data (id INT, value TEXT);

-- Нежурналируемая таблица (быстрее, но нет WAL)
CREATE UNLOGGED TABLE cache_data (id INT, data JSONB);

-- Таблица-наследник
CREATE TABLE logs_2024 INHERITS (logs);
```

### Генерация идентификаторов

```sql
-- SERIAL (автоинкремент)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- BIGSERIAL для больших таблиц
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_data TEXT
);

-- IDENTITY (стандарт SQL, рекомендуется)
CREATE TABLE products (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT
);

-- UUID
CREATE TABLE sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INT
);
```

### Работа с датами и временем

```sql
-- Текущая дата и время
SELECT NOW();
SELECT CURRENT_TIMESTAMP;
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;

-- Интервалы
SELECT NOW() + INTERVAL '1 day';
SELECT NOW() - INTERVAL '2 hours';
SELECT AGE(NOW(), '2020-01-01');

-- Извлечение частей даты
SELECT EXTRACT(YEAR FROM NOW());
SELECT DATE_PART('month', NOW());

-- Форматирование
SELECT TO_CHAR(NOW(), 'DD.MM.YYYY HH24:MI:SS');
SELECT TO_DATE('15.01.2024', 'DD.MM.YYYY');

-- Часовые пояса
SELECT NOW() AT TIME ZONE 'UTC';
SELECT NOW() AT TIME ZONE 'Europe/Moscow';
SET TIME ZONE 'Europe/Moscow';
```

## Мониторинг и отладка

### Просмотр активных запросов

```sql
-- Активные процессы
SELECT pid, usename, state, query, query_start
FROM pg_stat_activity
WHERE state != 'idle';

-- Убийство процесса
SELECT pg_terminate_backend(pid);

-- Долгие запросы
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;
```

### Статистика производительности

```sql
-- Статистика по таблицам
SELECT * FROM pg_stat_user_tables;

-- Статистика по индексам
SELECT * FROM pg_stat_user_indexes;

-- Статистика по функциям
SELECT * FROM pg_stat_user_functions;

-- Размер таблиц
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Размер базы данных
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### EXPLAIN и анализ запросов

```sql
-- План выполнения
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- План с выполнением
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- План с буферами
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';

-- JSON формат
EXPLAIN (FORMAT JSON) SELECT * FROM users WHERE email = 'test@example.com';
```

## Оптимизация производительности

### VACUUM и ANALYZE

```sql
-- Очистка мёртвых кортежей
VACUUM;

-- Подробный вакуум с блокировками
VACUUM VERBOSE;

-- Полное переписывание таблицы
VACUUM FULL;

-- Обновление статистики
ANALYZE;

-- Вакуум и анализ конкретной таблицы
VACUUM ANALYZE users;
```

### Индексы

```sql
-- B-дерево (по умолчанию)
CREATE INDEX idx_email ON users(email);

-- Hash индекс
CREATE INDEX idx_hash ON users USING HASH(email);

-- GiST для полнотекстового поиска и геоданных
CREATE INDEX idx_gist ON articles USING GIST(search_vector);

-- GIN для JSONB и массивов
CREATE INDEX idx_gin ON products USING GIN(attributes);

-- Составной индекс
CREATE INDEX idx_name_email ON users(last_name, email);

-- Частичный индекс
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Выражение в индексе
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- Уникальный индекс
CREATE UNIQUE INDEX idx_unique_email ON users(email);

-- Удаление индекса
DROP INDEX idx_email;
```

## Безопасность

- Используйте `scram-sha-256` для аутентификации
- Настройте `pg_hba.conf` для ограничения доступа по IP
- Не используйте суперпользователя `postgres` для приложений
- Шифруйте соединения (SSL/TLS)
- Регулярно обновляйте PostgreSQL
- Делайте регулярные бэкапы
- Используйте роли с минимальными необходимыми правами
- Включите логирование важных событий

## Полезные утилиты

- **psql** — интерактивный терминал
- **pg_dump** — экспорт базы
- **pg_dumpall** — экспорт всех баз
- **pg_restore** — восстановление из бэкапа
- **pg_basebackup** — физический бэкап
- **pgbench** — бенчмарк производительности
- **vacuumlo** — удаление orphaned large objects
- **pg_isready** — проверка готовности сервера

## Ресурсы

- [Официальная документация](https://www.postgresql.org/docs/)
- [pgAdmin](https://www.pgadmin.org/) — GUI инструмент
- [PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Main_Page)
- [Explain Visualizer](https://explain.depesz.com/) — визуализация EXPLAIN

---

**Далее:** [Шпаргалка по PostgreSQL](./cheatsheet.md)
