import os
import boto3
from dotenv import load_dotenv

load_dotenv()


AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_URL": os.getenv("AWS_S3_ENDPOINT_URL"),
    "AWS_SES_REGION_NAME": os.getenv("AWS_SES_REGION_NAME"),
}


def init_db():
    db = boto3.resource("dynamodb",
        endpoint_url=AWS_CREDENTIALS.get("AWS_URL"),
        aws_access_key_id=AWS_CREDENTIALS.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=AWS_CREDENTIALS.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_CREDENTIALS.get("AWS_SES_REGION_NAME")
    )

    if len(list(db.tables.all())) < 1:
        db.create_table(
            TableName = "Pages",
            AttributeDefinitions = [
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "page_name",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput = {
                "WriteCapacityUnits": 5,
                "ReadCapacityUnits": 5
            },
            KeySchema = [
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "page_name",
                    "KeyType": "Range"
                }
            ]
        )
        
    return db 