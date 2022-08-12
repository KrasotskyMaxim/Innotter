from enum import Enum
import boto3

from fastapi import HTTPException, status 

from settings import AWS_CREDENTIALS


class DynamoDBFields(str, Enum):
    ITEM = "Item"
    ITEMS = "Items"
    ATTRS = "Attributes"
    ALL_NEW = "ALL_NEW"



def init_db():
    db = boto3.resource("dynamodb",
                       endpoint_url=AWS_CREDENTIALS["AWS_URL"],
                       aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"],
                       region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"]
                       )
    
    if len(list(db.tables.all())) < 1:
        db.create_table(
            TableName="Pages",
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "WriteCapacityUnits": 5,
                "ReadCapacityUnits": 5
            },
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user_id",
                    "KeySchema": [
                        {
                            "AttributeName": "user_id",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                }
            ]
        )
    
    return db

def check_page_exists(page):
    if not DynamoDBFields.ITEM in page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Undefined page." 
        )
    
    return True 
