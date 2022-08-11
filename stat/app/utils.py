import boto3

from settings import AWS_CREDENTIALS


def init_db():
    db = boto3.client("dynamodb",
                       endpoint_url=AWS_CREDENTIALS["AWS_URL"],
                       aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"],
                       region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"]
                       )
    
    return db
