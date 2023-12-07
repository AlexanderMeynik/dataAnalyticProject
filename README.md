# dataAnalyticProject
Базовый вариант сервера для запросов данных

Перед запуском клиент-серверного приложения потребуется загрузить дамп в бд.
Запустите только бд: docker compose run -d --publish 5501:5432 --name database_container  db  можно убрать параметр -d чтобы видеть,когда бд будет готова
Далее следует выполнить следующий код для загрузки данных из дампа : cat <path_to_dump> | docker exec -i database_container psql -U postgres
Можно завершить работу бд из ui докера(удалив его) или из терминала:

docker stop database_container

docker rm database_container

docker network remove project_default (проверить что удаляем ту сеть docker network ls)


Flask server упакован в докере вместе с бд. Имеются два профиля работы 
1. Dev запускается командой: docker compose --profile dev --profile db up -d. Суть состоит в том, что можно менять код и исполнять его без билда образа для сервера.
2. Prod запускается командой: docker compose --profile dev --profile db up -d. Файлы для сервера имеются ещё до запуска(удобнее будет потом деплоить).

Теперь из докера можно запустить и клиент: docker compose --profile client up -d

Повторно данный процесс выполнять не надо, поскольку всё сохраниться в data volume.

Как и ранее саму бд можно запустить командой docker compose run -d --publish 5501:5432 --name database_container  db
Сам flask сервер стоит запускать командой python3 flaskApi.py local в директории ServerCode.
