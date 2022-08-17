import pika
import uuid
import json
from innotter.settings import RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST, STAT_SERVICE_QUEUE


def init_producer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()

    qd_result = channel.queue_declare(queue="", exclusive=True)
    callback_queue = qd_result.method.queue

    corr_map = {}

    def on_response(ch, method, props, body):
        nonlocal corr_map
        if str(props.correlation_id) in corr_map:
            corr_map[props.correlation_id] = json.loads(body)

    def publish(method, body):
        nonlocal channel, callback_queue, corr_map
        corr_id = str(uuid.uuid4())
        corr_map[corr_id] = None
        channel.basic_publish(exchange="",
                                    routing_key=STAT_SERVICE_QUEUE,
                                    properties=pika.BasicProperties(
                                        reply_to=callback_queue,
                                        correlation_id=corr_id,
                                        content_type=method
                                    ),
                                    body=json.dumps(body))
        while corr_map[corr_id] is None and method == "get_stat":
            connection.process_data_events()

            
        return corr_map[corr_id]

    channel.basic_consume(on_message_callback=on_response, auto_ack=True,
                                    queue=callback_queue)
    return publish


publish = init_producer()
