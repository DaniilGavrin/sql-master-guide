# MySQL: Установка и настройка

MySQL — одна из самых популярных реляционных СУБД с открытым исходным кодом. В этом разделе мы рассмотрим установку, базовую настройку и особенности работы с MySQL.

## Установка MySQL

### Ubuntu/Debian

```bash
# Обновление пакетов
sudo apt update

# Установка MySQL Server
sudo apt install mysql-server -y

# Запуск службы
sudo systemctl start mysql
sudo systemctl enable mysql

# Проверка статуса
sudo systemctl status mysql
```

### CentOS/RHEL

```bash
# Добавление репозитория
sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm -y

# Установка
sudo yum install mysql-community-server -y

# Запуск
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### macOS (Homebrew)

```bash
# Установка
brew install mysql

# Запуск
brew services start mysql
```

### Windows

1. Скачайте установщик с [официального сайта](https://dev.mysql.com/downloads/mysql/)
2. Запустите установщик и следуйте инструкциям
3. Выберите тип установки (Developer Default рекомендуется)
4. Запомните пароль root, установленный в процессе

## Первоначальная настройка безопасности

После установки выполните скрипт безопасности:

```bash
sudo mysql_secure_installation
```

Вас попросят:
- Установить пароль для root (если не был установлен)
- Удалить анонимных пользователей
- Запретить удалённый вход для root
- Удалить тестовую базу данных
- Перезагрузить таблицы привилегий

## Подключение к MySQL

### Через командную строку

```bash
# Локальное подключение
mysql -u root -p

# Подключение к удалённому серверу
mysql -h hostname -u username -p

# Подключение к конкретной базе данных
mysql -u username -p database_name
```

### Основные команды CLI

| Команда | Описание |
|---------|----------|
| `\h` или `help` | Показать справку |
| `\u database` | Переключиться на базу данных |
| `\s` | Показать статус соединения |
| `\q` | Выйти из MySQL |
| `SHOW DATABASES;` | Показать все базы данных |
| `SHOW TABLES;` | Показать таблицы в текущей БД |
| `DESCRIBE table_name;` | Показать структуру таблицы |

## Конфигурационный файл

Основной конфиг: `/etc/mysql/my.cnf` или `/etc/my.cnf`

Пример базовой настройки:

```ini
[mysqld]
# Порт
port = 3306

# Путь к данным
datadir = /var/lib/mysql

# Лимит подключений
max_connections = 150

# Размер буфера
innodb_buffer_pool_size = 256M

# Логирование медленных запросов
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# Кодировка
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

После изменений перезапустите сервер:

```bash
sudo systemctl restart mysql
```

## Управление пользователями

```sql
-- Создание пользователя
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';

-- Предоставление прав
GRANT ALL PRIVILEGES ON database_name.* TO 'newuser'@'localhost';

-- Применение изменений
FLUSH PRIVILEGES;

-- Просмотр прав
SHOW GRANTS FOR 'newuser'@'localhost';

-- Отзыв прав
REVOKE ALL PRIVILEGES ON database_name.* FROM 'newuser'@'localhost';

-- Удаление пользователя
DROP USER 'newuser'@'localhost';
```

## Резервное копирование и восстановление

### Создание бэкапа

```bash
# Полная резервная копия
mysqldump -u root -p --all-databases > backup.sql

# Бэкап конкретной базы
mysqldump -u root -p database_name > db_backup.sql

# Бэкап с сжатием
mysqldump -u root -p database_name | gzip > db_backup.sql.gz
```

### Восстановление из бэкапа

```bash
# Восстановление базы
mysql -u root -p database_name < db_backup.sql

# Восстановление из сжатого файла
gunzip < db_backup.sql.gz | mysql -u root -p database_name
```

## Особенности MySQL

### Движки хранения

- **InnoDB** (по умолчанию) — транзакционный движок с поддержкой внешних ключей
- **MyISAM** — быстрый для чтения, но без транзакций
- **Memory** — хранение данных в оперативной памяти

Проверка движка таблицы:

```sql
SHOW TABLE STATUS WHERE Name = 'table_name';
```

Смена движка:

```sql
ALTER TABLE table_name ENGINE = InnoDB;
```

### Автоматическое увеличение (AUTO_INCREMENT)

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- Сброс счётчика
ALTER TABLE users AUTO_INCREMENT = 1;
```

### Работа с датами

MySQL имеет свои особенности работы с датами:

```sql
-- Текущая дата и время
SELECT NOW();
SELECT CURDATE();
SELECT CURTIME();

-- Форматирование даты
SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');

-- Добавление интервала
SELECT DATE_ADD(NOW(), INTERVAL 1 DAY);
```

## Полезные утилиты

- **mysqladmin** — администрирование сервера
- **mysqlimport** — импорт данных
- **mysqlshow** — просмотр структуры БД
- **mytop** — мониторинг запросов в реальном времени

## Отладка и логирование

Включение общего лога (для отладки):

```ini
[mysqld]
general_log = 1
general_log_file = /var/log/mysql/general.log
```

Просмотр активных процессов:

```sql
SHOW PROCESSLIST;
```

Убийство зависшего процесса:

```sql
KILL process_id;
```

## Оптимизация производительности

### Анализ запросов

```sql
-- Включение EXPLAIN
EXPLAIN SELECT * FROM users WHERE id = 1;

-- Анализ медленных запросов
SELECT * FROM mysql.slow_log;
```

### Индексы

```sql
-- Создание индекса
CREATE INDEX idx_username ON users(username);

-- Составной индекс
CREATE INDEX idx_name_email ON users(last_name, email);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_email ON users(email);

-- Удаление индекса
DROP INDEX idx_username ON users;
```

## Безопасность

- Регулярно обновляйте MySQL до последней версии
- Используйте сложные пароли
- Ограничьте доступ по IP
- Не используйте root для приложений
- Шифруйте соединения (SSL)
- Регулярно делайте бэкапы

## Ресурсы

- [Официальная документация](https://dev.mysql.com/doc/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/) — GUI инструмент
- [Percona Toolkit](https://www.percona.com/software/percona-toolkit) — набор утилит

---

**Далее:** [Шпаргалка по MySQL](./cheatsheet.md)
