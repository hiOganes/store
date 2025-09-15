# StoreAPI

#### Decisions taken:

- *Приложения*: Создано четыре приложения. Одно из них `common` там лежат общие 
инструменты: пагинация, права доступа и тестовые данные. Общая модель `BaseModel` 
не реализована, так как модели не имеют общих полей. Для соблюдения принципа `DRY` 
в будущем можно добавить `BaseModel` с полями `created_at`, `updated_at` и другими, 
если у других моделей будут общие поля.

  
- *Пользователи*: Переопределена модель `User`, На мой взгляд, это был наиболее 
подходящий вариант, так как она уже содержит все необходимое, включая ссылку на 
переменную `AUTH_USER_MODEL`. 
Поле `email` сделано уникальным и используется для аутентификации. 
Регистрация выдает `JWT-токены`, для уменьшения количества обращений к базе данных.

  
- *Заказы*: Представления, тесты и маршруты разделены на пользовательские и 
административные для уменьшения объема кода в отдельных файлах при росте 
админ-эндпоинтов. 
Метод `create` в сериализаторе использует контекстный менеджер `Atomic` для 
атомарности процесса.


- *Документация*: Для документации эндпоинтов используется `drf_spectacular`, 
данные вынесены в отдельные файлы `schema_examples.py` в каждом приложении, чтобы
не занимать много места в файлах с представлениями.

  
- *Настройки*: В папке `core/settings` находятся файлы настроек: для разработки 
`dev.py`, продакшена `prod.py` и `Celery`: `celery.py`. 
Настройки `Celery` созданы с учетом будущего расширения, например, для 
добавления расписаний.


- *Celery*: Сгенерированные `PDF-файлы` хранятся в папке `orders/orders_reports`.
Если папки нет, она будет создана автоматически. 
Для мониторинга задач подключены `Flower` и `result_backend`: `django-db`, с 
просмотром результатов в админ-панели.

  
- *Базы данных*: В разработке используется `SQLite`, в продакшене через `Docker` — `PostgreSQL`. 
Настройки для разработки хранятся в `.env`, настройки для продакшена хранятся в `.docker.env`. 
Выбор базы данных зависит от окружения:
Если ничего не меняя запустить проект локально, тогда будут применены настройки 
для разработки и база данных `SQLite`.
Если запуск проекта будет сделан в контейнерах по инструкции которая указана 
ниже, тогда будут применены настроки для продакшена и база данных `PostgreSQL`


- *Дополнительно*: Файлы `.env` и `.docker.env` не добавлены в `.gitignore`,
некоторые данные также не были скрыты, для упрощения запуска. 
Папка `screenshots` включена для демонстрации работы 
сервисов в `README.md`.


## Table of Contents

- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Screenshots](#screenshots)

## Technologies

- Python 3.12.3
- Django 5.2.5
- PostgreSQL 17.0
- Redis 8.2
- Memcached 1.6.24

## Installation and start project

1. Clone the repository
    ```
    git clone git@github.com:hiOganes/store.git
    ```

2. In the terminal, at the docker-compose.yaml file level, run the command:
    ```
    docker compose up
    ```

3. Next, you need to connect to the project terminal using the command:
    ```
    docker compose exec web bash
    ```
### inside the container / bash

1. Apply migrations:
    ```
    python manage.py migrate
    ```

2. Create a superuser:
    ```
    python manage.py createsuperuser
    ```

## Endpoints

1. Open your browser and go to [OpenAPI](http://127.0.0.1:8001/api/schema/swagger-ui/)
2. Open your browser and go to [ReDoc](http://127.0.0.1:8001/api/schema/redoc/)

## Testing

 ```
 python manage.py test .
 ```

### Screenshots 
### Celery
#### Flower
![celery_flower](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_flower.png)
![celery_flower_tasks](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_flower_tasks.png)
#### Terminal
![celery_terminal_gen_pdf](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminal_gen_pdf.png)
![celery_terminal_sending_email](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminal_sending_email.png)
![celery_terminsl_api_simulation](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminsl_api_simulation.png)
#### Admin
![celery_admin](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_admin.png)

### Memcached

<p align="center">
 <img width="1000px" src="https://raw.githubusercontent.com/hiOganes/store/main/screenshots/memcache.png" alt="qr"/>
</p>