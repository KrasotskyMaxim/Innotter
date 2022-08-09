import json, os
import pika

from dotenv import load_dotenv


load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, credentials=credentials, heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()
    channel.queue_declare(queue="statistic")

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(method, properties, data)

    channel.basic_consume(queue="statistic", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    main() 
