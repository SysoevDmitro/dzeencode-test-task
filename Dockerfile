FROM python:3.11.4-slim-buster

ENV PYTHONUNBUFFERED 1


WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .


CMD ["python", "manage.py", "runserver"]
