# `Foodgram` - сайт "Продуктовый помощник"

[![foodgram-project-react workflow](https://github.com/laser54/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)](https://github.com/laser54/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

#### О проекте:
 Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин скачивать сводный список всех продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
 
#### Технологии:
- Python 3.8
- Django 3.2
- Django REST Framework
- Postgre SQL
- Nginx
- Gunicorn
- Docker

#### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

`https://github.com/laser54/foodgram-project-react.git`

`cd foodgram-project-react`

Установить docker и Docker-Compose (нативная ОС для Docker — Linux, поэтому запуск Docker-контейнеров должен происходить внутри виртуальной машины с ОС Linux):

`sudo apt install docker-ce docker-compose -y`

Для работы с базой данных создать файл .env c переменными окружения. В директории backend/ проекта расположен файл .env.example, в котором описаны примеры переменных и их значений.

Запуск контейнера:

`docker-compose up -d`

Заполнение базы данными:

`sudo docker-compose exec backend python manage.py collectstatic --no-input`

`sudo docker-compose exec backend python manage.py makemigrations --noinput`

`sudo docker-compose exec backend python manage.py migrate --noinput`

`sudo docker-compose exec backend python manage.py createsuperuser`

`sudo docker-compose exec backend python manage.py loaddata ingredients.json`


Проект:


`http://foodgramtest.zapto.org`

Суперпользователь:

`Адрес электронной почты: admin10@mail.ru`

`Пароль: Parol123`



