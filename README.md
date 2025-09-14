# StoreAPI

#### Принятые решения:

- Было создано четыре приложения, одно из которых предназначено для реализации 
общих инструментов разработки, таких как пагинация, права доступа и данные 
для тестов. Общая базовая модель не была реализована, так как в ней пока нет 
необходимости, поскольку у моделей отсутствуют общие поля. В дальнейшем, 
чтобы следовать принципам `DRY`, можно создать общую модель `BaseModel` и 
реализовать в ней общие поля, такие как `created_at`, `updated_at` и другие, 
по необходимости. На данный момент это не сделано, так как в техническом 
задании нет пересекающихся полей у моделей.
- Была переопределена модель `User`. На мой взгляд, это был наиболее подходящий 
вариант, так как она уже содержит все необходимое, включая ссылку на 
переменную `AUTH_USER_MODEL`. Оставалось лишь переопределить поле `email`, 
указав его уникальность, и установить его как поле для аутентификации. 
Также была реализована регистрация, после которой выдаются токены для 
аутентификации, чтобы уменьшить количество обращений к базе данных. 
Были созданы кастомные классы `JWT` для их документирования через 
`drf_spectacular`. Чтобы `drf_spectacular` не занимал много места в файле с 
представлениями, во всех приложениях был создан отдельный файл 
`schema_examples.py`, где хранится вся документация.
- В заказах было решено разделить представления, тесты и маршрутизаторы для 
обычных заказов и админских заказов, чтобы сократить количество кода в 
отдельных файлах, если представления админа будут расти со временем. В 
методе `create` сериализатора заказов объекты создаются в блоке кода 
контекстного менеджера `Atomic` для атомарности создания заказа.
- В папке core была создана общая папка `settings`, в которой находятся файлы с 
настройками проекта для разработки, продакшена и файл с настройками `Celery`. 
Файл с настройками `Celery` был реализован с заделом на то, что со временем 
он будет расширяться, например, может быть добавлено расписание и другие 
настройки, которые могут потребовать большое количество строк.
- Таски `Celery` создают `PDF-файлы`, поэтому для этих файлов в приложении `orders` 
есть отдельная папка `orders_reports`.
- Так как в проекте можно использовать разные базы данных, в разработке 
использовалась `SQLite`, а в продакшене (при развертывании в `Docker`) будет 
использоваться `PostgreSQL`. Для этого были созданы файлы `.docker.env` и `.env`: 
в одном файле находятся данные для разработки, в другом — для продакшена. 
Если проект будет развернут на локальной машине, будут использоваться 
настройки для разработки и `SQLite`, если разворачивать проект в контейнере, 
он будет запущен как продакшен с `PostgreSQL`.
- Файлы `.env` и `.docker.env` не были добавлены в `.gitignore` для облегчения 
запуска проекта. Также в проект была добавлена папка `screenshots` для 
возможности отображения работы сервисов в файле `README.md`.

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