# dataAnalyticProject
Базовый вариант сервера для запросов данных

Перед запуском клиент-серверного приложения потребуется загрузить дамп в бд.
Запустите только бд: docker compose run -d --publish 5501:5432 --name database_container  db
можно убрать параметр -d чтобы видеть,когда бд будет готова
Далее следует выполнить следующий код для загрузки данных из дампа : cat <path_to_dump> | docker exec -i database_container psql -U postgres
Можно завершить работу бд из ui докера(удалив его) или из терминала:

docker stop database_container

docker rm database_container

docker network remove project_default (проверить что удаляем ту сеть docker network ls)


Упакован в докер вместе с бд. Имеются два профиля работы 
1. Dev запускается командой: docker compose --profile dev up -d. Суть состоит в том, что можно менять код и исполнять его без билда образа для сервера.
2. Prod запускается командой: docker compose --profile prod up -d. Файлы для сервера имеются ещё до запуска(удобнее будет потом деплоить).

Повторно данный процесс выполнять не надо, поскольку всё сохраниться в data volume.


Сам flask сервер стоит запускать командой python3 flaskApi.py local в директории ServerCode.

На данный момент клиент не упакован в докер т.к. его базовая реализация ещё не сделана. По даннйо причине пока запросы к к flask серверу надо начинать с url "http://127.0.0.1:5000", при тестах с браузера или postman.
