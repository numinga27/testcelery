FROM python:3.8-slim-buster

# Установите рабочую директорию в /app
WORKDIR /app

# Скопируйте текущий каталог в рабочую директорию /app
ADD . /app

# Установите необходимые пакеты и psycopg2-binary
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt


# Установите PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
COPY testcelery/ /app
WORKDIR /app

# Скопируйте скрипт init.sql в контейнер Docker
CMD ["python3", "manage.py", "runserver", "0:8000"] 
