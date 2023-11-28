# dataAnalyticProject
Базовый вариант сервера для запросов данных
Упакован в доке вместе с бд для запуска также требуется прописать docker compose up -d
При запущенной бд можно её шардировать(установлен плагин citus data) при помощи данного кода

  docker exec -it database_container psql -U postgres

  SELECT create_distributed_table('public.articles', 'article_id');

  SELECT create_distributed_table('public.journals', 'id');

  \q
  
На данный момент клиент не упакован в докер т.к. его базовая реализация ещё не сделана. По даннйо причине пока запросы к к flask серверу надо начинать с url "'http://127.0.0.1:5500", при тестах с браузера или postman.
