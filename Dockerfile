FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
RUN pipenv install
RUN pipenv shell
COPY  . /code/
RUN python manage.py runserver 0.0.0.0:8000


