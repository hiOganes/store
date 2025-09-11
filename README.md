# StoreAPI

#### Основные функции:

#### Технологии и решения:

1.Example

## Table of Contents

- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Running the Project](#running-the-project)
- [Testing](#testing)

## Technologies

- Python 3.12.3
- Django 5.2.5
- PostgreSQL 17.0
- Redis 8.2

## Installation and start project

1. Clone the repository
    ```
    git@github.com:hiOganes/store.git
    ```

2. In the terminal, at the docker-compose.yaml file level, run the command:
    ```
    docker compose up
    ```

3. Next, you need to connect to the project terminal using the command:
    ```
    docker compose exec web bash
    ```

4. Apply migrations:
    ```
    python manage.py migrate
    ```

5. Create a superuser:
    ```
    python manage.py createsuperuser
    ```

## Running the Project

1. Open your browser and go to [OpenAPI](http://0.0.0.0:8001/api/schema/swagger-ui/)
2. Open your browser and go to [ReDoc](http://0.0.0.0:8001/api/schema/redoc/)

## Testing

   ```
 python manage.py test .
   ```

### Скриншоты Celery
#### Flower
![celery_flower](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_flower.png)
![celery_flower_tasks](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_flower_tasks.png)
#### Terminal
![celery_terminal_gen_pdf](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminal_gen_pdf.png)
![celery_terminal_sending_email](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminal_sending_email.png)
![celery_terminsl_api_simulation](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_terminsl_api_simulation.png)
#### Admin
![celery_admin](https://raw.githubusercontent.com/hiOganes/store/main/screenshots/celery_admin.png)

### Скриншоты Memcached

<p align="center">
 <img width="1000px" src="https://raw.githubusercontent.com/hiOganes/store/main/screenshots/memcache.png" alt="qr"/>
</p>