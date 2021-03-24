# Python world

Mentoring Web App based on Django. Provides possibility to create courses
and modules of courses. Defined custom user for permission for authors of
courses and for students. Email verification for creating a new account
(shown in terminal).

## Technology:
Python, Django, Django-Crispy-Roms, Django-Allauth, Pillow,
Docker, DockerCompose.

## How tu run:

###Prerequisites
You have to have installed docker and docker-compose on your computer.

###Starting

Type command `docker-compose up --build` in terminal in project root directory.
Do preparation of migrations: `docker-compose exec backend python manage.py makemigrations courses users`
Migrate `docker-compose exec backend python manage.py migrate`
To test app fully superuser will be useful `docker-compose exec backend python manage.py createsuperuser`

Open browser with url http://0.0.0.0:8000 or http://127.0.0.1:8000 on Windows.

Enjoy!