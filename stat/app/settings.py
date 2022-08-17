import os
from dotenv import load_dotenv


load_dotenv()


AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_URL": os.getenv("AWS_S3_ENDPOINT_URL"),
    "AWS_SES_REGION_NAME": os.getenv("AWS_DEFAULT_REGION"),
}


RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

STAT_SERVICE_QUEUE = os.getenv("STAT_SERVICE_QUEUE")
