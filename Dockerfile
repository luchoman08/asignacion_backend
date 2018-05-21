FROM kennethreitz/pipenv
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN python manage.py runserver 0.0.0.0:8000


