import json
import pika

from innotter.settings import RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST


credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST, credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue="statistic")


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="", routing_key="statistic",
                          body=json.dumps(body), properties=properties) 
    