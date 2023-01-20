FROM python:3.11.1-alpine3.17

RUN apk update && apk add --no-cache --virtual .build-deps \
    gcc libffi-dev mariadb-dev musl-dev

WORKDIR /app 

COPY requirements.txt /app/requirements.txt 

RUN pip install --upgrade --no-cache-dir -r requirements.txt 

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
