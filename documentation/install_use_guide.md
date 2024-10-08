[На страницу с документацией](README.md)
# Инструкция по работе и установке
На основной странице репозитория имеются 2 релиза данного ПО: fat и lite версии. Fat релиз содержит полный dump с готовой информацией, в то время как lite релиз содержит только необходимые скрипты и конфигурационные файлы.
## Установка вручную
### Предварительная инициализация
Для выполнения инициализации потребуется установить файл с дампом бд из fat([см. последний release](https://github.com/AlexanderMeynik/dataAnalyticProject/releases/tag/fat)). Его можно получить из дистрибутива на диске.
- Клонируйте репозиторий git clone https://github.com/AlexanderMeynik/dataAnalyticProject
- Перейдите в рабочую директорию dataAnalyticProject
- Можно собрать образы заранее docker compose -p data_analytic_project --profile prod --profile db --profile client_prod build(см. [Профили](#профили))
- Запустите сервис бд: docker compose  -p data_analytic_project run -d --publish 5501:5432 --name database_container  db
- Когда бд будет готова к подключениям(docker logs database_container), выполните загрузку дампа следующей командой: 
  - cat <path_to_dump> | docker exec -i database_container psql -U postgres
- Завершите работу сервиса docker stop database_container&&docker rm database_container

### Инструкция по запуску
- Для запуска сервисов бд и Rest можно выполнить команду:
  - docker compose -p data_analytic_project --profile prod --profile db up -d
- После небольшой паузы можно запустить и клиент:
  - docker compose -p data_analytic_project --profile client_prod up -d 
  - UI из сервиса клиента можно получить перейдя по URL http://localhost:8050/
  - Rest api доступен по адресу http://localhost:5000/
- Завершить работу всех сервисов можно используя команду
  - docker compose -p data_analytic_project --profile prod --profile db --profile client_prod down (см. [Профили](#профили))
  docker network remove project_default (проверить что удаляем ту сеть docker network ls)


# Профили
Для удобной разработки были введены несколько профилей для работы с сервером и бд и клиентом.
1. Профили клиента
    - client_prod - используется для развёртывания клиента. При выполнении данного профиля будет собран полноценный образ с кодом клиента.
    - client_dev - отличие от предыдущего профиля состоит в том, что в конченом образе не содержится кода клиента. Данный код будет присоединяться из директории ClientCode, что позволяет обновлять клиент без повторной сборки образа, однако требуется перезапускать контейнер.
2. Профили сервера(запускать всегда требуется в паре с базой данных --profile db)
   - prod - аналогичен prod профилю клиента. Используется для развёртывания сервера REST API.
   - dev - При выборе данного профиля потребуется заменить в файле clientCode/dataRequestService.py хост s server:5000 на server_dev:5000

При использовании dev профилей также рекомендуется использовать [Flask Development server](https://flask.palletsprojects.com/en/2.3.x/server/)(вместо waitress).
Таким образом при появлении изменений в коде данных сервисов они автоматически перезагрузятся, что убирает необходимость выполнять docker compose restart на нужных контейнерах.

При запуске элементов с определёнными профилями завершать их работу из консоли следует с теми же профилями, с которыми они и были запущены.

Пример:
- Связку бд и REST API запущенную данной командой:
    - docker compose -p data_analytic_project --profile dev --profile db up -d
- Можно закрыть следующей командой:
  - docker compose -p data_analytic_project --profile dev --profile db down

Для удобства можно пользоваться GUI докера, чтобы закрывать весь проект разом.
Имеется возможность запуска элементов(REST API, клиент) локально вне докера.
Однако так делать не стоит, поскольку это обернётся большим числом неудобств связанных с настройкой конфигурации ip и сетей.
