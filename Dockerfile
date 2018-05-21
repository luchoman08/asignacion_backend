FROM python:3.4
RUN pip install pipenv --upgrade
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pipenv install --verbose --system