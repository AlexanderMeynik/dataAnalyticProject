# dataAnalyticProject
Базовый вариант сервера для запросов данных
Упакован в докер вместе с бд. Имеются два профиля работы 
1. Dev запускается командой: docker compose --profile dev up -d. Суть состоит в том, что можно менять код и исполнять его без билда образа для сервера.
2. Prod запускается командой: docker compose --profile prod up -d. Файлы для сервера имеются ещё до запуска(удобнее будет потом деплоить).

При запущенной бд можно её шардировать(установлен плагин citus data) при помощи данного кода.

SELECT create_distributed_table('public.articles', 'article_id');

SELECT create_distributed_table('public.journals', 'id');

SELECT truncate_local_data_after_distributing_table($$public.articles$$);

SELECT truncate_local_data_after_distributing_table($$public.journals$$);

\q
Повторно данный процесс выполнять не надо, поскольку всё сохраниться в data volume.

Также для тестов можно запустить бд отдельно. Для этого выполняем команду: docker compose run --publish 5501:5432 --name database_container  db -d.

Сам flask сервер стоит запускать командой python3 flaskApi.py local в директории ServerCode.

На данный момент клиент не упакован в докер т.к. его базовая реализация ещё не сделана. По даннйо причине пока запросы к к flask серверу надо начинать с url "http://127.0.0.1:5000", при тестах с браузера или postman.
