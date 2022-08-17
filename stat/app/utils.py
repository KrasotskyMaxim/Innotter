from enum import Enum
import boto3

from botocore.exceptions import ClientError

import json
from decimal import Decimal

from fastapi import HTTPException, status 

from settings import AWS_CREDENTIALS


class DynamoDBFields(str, Enum):
    ITEM = "Item"
    ITEMS = "Items"
    ATTRS = "Attributes"
    ALL_NEW = "ALL_NEW"


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        
        return json.JSONEncoder.default(self, obj)


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


db = init_db()


def create_new_page(page):
    item = db.Table("Pages").get_item(Key={"id": page.id})
    
    if DynamoDBFields.ITEM in item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Page already exist."
        )
    
    put_item = page.dict()
    print(put_item)
    
    db.Table("Pages").put_item(Item=put_item)
    
    return put_item


def update_page(page_name, page_id, user_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
        
    if item[DynamoDBFields.ITEM]["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not permissions to perform this operation."
        ) 

    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="SET #name = :n",
        ExpressionAttributeValues={
            ":n": page_name
        },
        ExpressionAttributeNames={
            "#name": "name"
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )
    
    return item[DynamoDBFields.ATTRS]


def delete_page(user_id, page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
    
    if item[DynamoDBFields.ITEM]["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not permissions to perform this operation."
        ) 
    
    db.Table("Pages").delete_item(Key={"id": page_id})
    
    return {"Status": "Deleted"}


def get_pages(user_id):
    response = db.Table("Pages").query(
        IndexName="user_id",
        KeyConditionExpression="user_id=:user_id",
        ExpressionAttributeValues={
            ":user_id": user_id
        }
    )
    
    return response[DynamoDBFields.ITEMS]


def new_like(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD likes :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    return item[DynamoDBFields.ATTRS]


def new_follower(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)    
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD followers :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    return item[DynamoDBFields.ATTRS]


def new_follow_request(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    
    check_page_exists(page=item)
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD follow_requests :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    return item[DynamoDBFields.ATTRS]
    

def undo_like(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
    
    try:
        item = db.Table("Pages").update_item(
            Key={"id": page_id},
            UpdateExpression="ADD likes :inc",
            ConditionExpression="likes > :zero",
            ExpressionAttributeValues={
                ":inc": -1,
                ":zero": 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW
        )
    except ClientError as err:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot undo like action because likes count already equals to 0."
        ) 

    return item[DynamoDBFields.ATTRS]



def undo_follower(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
    
    try:
        item = db.Table("Pages").update_item(
            Key={"id": page_id},
            UpdateExpression="ADD followers :inc",
            ConditionExpression="followers > :zero",
            ExpressionAttributeValues={
                ":inc": -1,
                ":zero": 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW
        )
    except ClientError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot undo follower action because followers count already equals to 0."
        )  
        
    return item[DynamoDBFields.ATTRS]


def undo_follow_request(page_id):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    print(item)
    
    check_page_exists(page=item)
    
    try:
        item = db.Table("Pages").update_item(
            Key={"id": page_id},
            UpdateExpression="ADD follow_requests :inc",
            ConditionExpression="follow_requests > :zero",
            ExpressionAttributeValues={
                ":inc": -1,
                ":zero": 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW
        )
    except ClientError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot undo follow request action because follow requests count already equals to 0."
        )  

    return item[DynamoDBFields.ATTRS]


def check_page_exists(page):
    if not DynamoDBFields.ITEM in page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Undefined page." 
        )
    
    return True 
