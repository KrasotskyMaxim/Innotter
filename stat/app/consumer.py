import json
import pika

from settings import (RABBITMQ_PASS, 
                      RABBITMQ_HOST,
                      RABBITMQ_PORT,
                      RABBITMQ_USER,
                      STAT_SERVICE_QUEUE)

from models import Page
from utils import (create_new_page, 
                   get_pages, 
                   update_page,
                   delete_page,
                   new_follow_request,
                   new_follower,
                   new_like,
                   undo_follow_request,
                   undo_follower,
                   undo_like,
                   DecimalEncoder)


CONTENT_TYPES = {
    "create_page": create_new_page,
    "update_page": update_page,
    "delete_page": delete_page,
    "get_stat": get_pages,
    "new_like": new_like,
    "new_follower": new_follower,
    "new_follow_request": new_follow_request,
    "undo_like": undo_like,
    "undo_follower": undo_follower,
    "undo_follow_request": undo_follow_request
}


credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST, credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue=STAT_SERVICE_QUEUE)


def callback(ch, method, props, body):
    data = json.loads(body)
    content_type = props.content_type
    
    if content_type in CONTENT_TYPES:
        service = CONTENT_TYPES[content_type]
        
        match content_type:
            case "create_page":
                data = service(Page.parse_obj(data))     
            case "delete_page":
                data = service(data["user_id"], data["id"])
            case "update_page":
                data = service(data["name"], data["id"], data["user_id"])
            case "get_stat":
                data = service(data["user_id"])
            case _:
                data = service(data["id"])
            
    properties = pika.BasicProperties(correlation_id=props.correlation_id)
            
    ch.basic_publish(exchange="",
                     routing_key=props.reply_to,
                     properties=properties,
                     body=json.dumps(data, cls=DecimalEncoder))

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback, queue=STAT_SERVICE_QUEUE)
channel.start_consuming()