# Simple Calendar App

Это простой аналог Google Календаря, созданный с использованием Django и Django REST Framework.

## Инструкция по запуску

1. Клонируйте репозиторий.
2. Запустите контейнеры с помощью команды 
    ```bash
    docker compose -f "docker-compose.yml" up -d --build 
    ```
3. API доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API запросы

- **POST /add/** — Добавить событие.
- **POST /remove/{id}/{year}/{month}/{day}/** — Удалить конкретное событие.
- **POST /remove-next/{id}/{year}/{month}/{day}/** — Удалить конкретное событие и все последующие.
- **POST /update/{id}/{year}/{month}/{day}/** — Изменить название конкретного события.
- **GET /events/{year}/{month}/{day}/** — Получить список событий на указанный день.