# pull official base image
FROM python:3.10.4-alpine

# set work directory
WORKDIR /home/maks/myfolder/python/Innotter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/home/maks/myfolder/python/Innotter/entrypoint.sh"]