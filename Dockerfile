FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./static /code/static
COPY ./app /code/app
COPY ./.env /code/.env

RUN pip3 install --no-cache-dir -r /code/requirements.txt