import boto3
from django.conf import settings
from innotter.celery import app
from innotter.aws import ses


@app.task
def send_email_to_subscribers(page, follower_list):
    ses.send_email(
        Source=settings.DEFAULT_FROM_EMAIL,
        Destination={"ToAddresses": follower_list},
        Message={
            "Subject": {
                "Data": f"New post on {page}.",
                "Charset": "utf-8"
            },
            "Body": {
                "Text": {
                    "Data": f"{page} has published a new post",
                    "Charset": "utf-8"
                },
            }
        }
    )