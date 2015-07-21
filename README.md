# progressive
Web service for smart news aggregation

Инструкция для запуска:

1) pip install vk_api sqlalchemy

2) rm vk.db

3) python3.4 database/create_db.py

4) Для запуска надо запустить web.py и main.py одновременно

main.py скаладывает в БД новые посты
web.py запускает веб сервер