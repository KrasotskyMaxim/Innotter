import json
import pika

from settings import (RABBITMQ_PASS, 
                      RABBITMQ_HOST,
                      RABBITMQ_PORT,
                      RABBITMQ_USER)


def callback(ch, method, properties, body):
        data = json.loads(body)
        print(method, properties, data)


def start_consuming(channel):
    channel.queue_declare(queue="statistic")
    channel.basic_consume(queue="statistic", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, credentials=credentials, heartbeat=600, blocked_connection_timeout=300))
    
    channel = connection.channel()
    
    start_consuming(channel=channel)    
    

if __name__ == "__main__":
    main() 
