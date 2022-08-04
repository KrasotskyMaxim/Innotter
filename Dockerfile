# pull official base image
FROM python:3.10.4-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . /app/

# run entrypoint.sh
RUN chmod +x ./entrypoint.sh
RUN chmod +x ./entrypoint_celery.sh