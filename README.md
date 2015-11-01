# progressive
Web service for smart news aggregation


**Библиотеки:**

`pip3 install -r requirements.txt`

`cd web && npm install`

### База данных:

#### Требования

#### Установка MySQL
Прежде чем приступить к созданию БД, MySQL не ниже **5.6** должен быть установлен.

Рекомендуется установить версию **5.6.25**, так как эта версия установлена на сервере на данный момент.

#### Конфигурация MySQL
Нужно изменить стандартную кодировку MySQL на utf8mb4. Для этого необходимо в файле конфигурации для MySQL `my.cnf`, который находится:
`/etc/mysql/my.cnf` или `/etc/my.cnf`

Внести следующие изменения:
* в секцию `[client]` (если ее не существует, то следует ее создать):
```
[client]
default-character-set = utf8mb4
```
* в секцию `[mysqld]` (если ее не существует, то следует ее создать):
```
init_connect='SET collation_connection = utf8mb4_unicode_ci'
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

Затем нужно рестартовать mysql любым способом, например:

`sudo service mysql restart`

Чтобы проверить, что кодировка установлено верно необходимо присоединитьсяк mysql процессу:

`mysql -u username -p`
(параметр `-p` нужен только в том случае, если при установке MySQL вы установили пароль для вашего `username`)

Результат команды `show variables like "%character_set%";` должен быть следующим:

```
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8mb4                    |
| character_set_connection | utf8mb4                    |
| character_set_database   | utf8mb4                    |
| character_set_filesystem | binary                     |
| character_set_results    | utf8mb4                    |
| character_set_server     | utf8mb4                    |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```

Если результат совпадает с вышеприведенным, то MySQL сконфигурирован корректно и можно переходить к следующему пункту
#### Установка логина и пароля для соединения к БД
* Устанавливаем переменную окружения $GRESSPRO, которая указывает на папку progressive (лучше всего это сделать в ~/.profile) - путь не должен заканчиваться на `/`:

```
admin@linux-495i:~> echo $GRESSPRO
/home/admin/progressive
```

* В папку на уровень выше нужно положить файл `.db_secrets`, в котором надо указать `username:password` для соединения к MySQL (если вы не указали пароль для юзера, то `:passwords` нужно не писать):

#### Создание базы данных

`python3 news/database/create_db.py`

#### Поиск групп для сбора информации
`python3 news/base/json_groups.py && python3 news/base/find_groups.py`

**Сборка веб-файлов**

`cd web`
`grunt less autoprefixer` или `grunt watch`

**Запуск:**

`python3 news/main.py & python3 web/main.py &`