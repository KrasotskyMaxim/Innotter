from enum import Enum

from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException

from botocore.exceptions import ClientError

from models import Page
from utils import init_db


db = init_db()
app = FastAPI() 


class DynamoDBFields(str, Enum):
    ITEM = "Item"
    ITEMS = "Items"
    ATTRS = "Attributes"
    ALL_NEW = "ALL_NEW"



@app.post("/create_page")
async def new_page(page: Page):
    item = db.Table("Pages").get_item(Key={"id": page.id})
    
    if DynamoDBFields.ITEM in item:
        return "Page already exist.", status.HTTP_400_BAD_REQUEST

    put_item = {
        "id": str(page.id),
        "user_id": str(page.user_id),
        "name": page.name,
        "likes": 0,
        "followers": 0,
        "follow_requests": 0
    }

    if db.Table("Pages").put_item(Item=put_item):
        stat = status.HTTP_200_OK
        data = put_item
        
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/update_page")
async def update_page(page_name: str, user_id: str, page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
    if item[DynamoDBFields.ITEM]["user_id"] != user_id:
        return "You have not permissions to perform this operation.", status.HTTP_400_BAD_REQUEST

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

    if item:
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)

    return data


@app.delete("/delete_page")
async def delete_page(user_id: str, page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
    if item[DynamoDBFields.ITEM]["user_id"] != user_id:
        return "You have not permissions to perform this operation.", status.HTTP_400_BAD_REQUEST
    
    if db.Table("Pages").delete_item(Key={"id": page_id}):
        stat = status.HTTP_200_OK
        data = {"Status": "Deleted"}
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)

    return data


@app.get("/pages", response_model=list[Page])
async def get_pages(user_id: str):
    response = db.Table("Pages").query(
        IndexName="user_id",
        KeyConditionExpression="user_id=:user_id",
        ExpressionAttributeValues={
            ":user_id": user_id
        }
    )
    
    if response:
        data = response[DynamoDBFields.ITEMS]
        stat = status.HTTP_200_OK
    
    return data


@app.put("/pages/{page_id}/new_like/", response_model=Page)
async def new_like(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD likes :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    if item:
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/pages/{page_id}/new_follower/", response_model=Page)
async def new_follower(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD followers :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    if item:
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/pages/{page_id}/new_follow_request/", response_model=Page)
async def new_follow_request(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
    item = db.Table("Pages").update_item(
        Key={"id": page_id},
        UpdateExpression="ADD follow_requests :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues=DynamoDBFields.ALL_NEW
    )

    if item:
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/pages/{page_id}/undo_like/", response_model=Page)
async def undo_like(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
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
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return "Cannot undo like action because likes count already equals to 0.", status.HTTP_400_BAD_REQUEST
        raise err

    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/pages/{page_id}/undo_follower/", response_model=Page)
async def undo_follower(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
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
        data = item[DynamoDBFields.ATTRS]
        stat = status.HTTP_200_OK
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return "Cannot undo follower action because followers count already equals to 0.", status.HTTP_400_BAD_REQUEST
        raise err
    
    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data


@app.put("/pages/{page_id}/undo_follow_request/", response_model=Page)
async def undo_follow_request(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    if not DynamoDBFields.ITEM in item:
        return "Undefined page.", status.HTTP_404_NOT_FOUND
    
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
        data = item[DynamoDBFields.ITEM]
        stat = status.HTTP_200_OK
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return "Cannot undo follow request action because follow requests count already equals to 0.", status.HTTP_400_BAD_REQUEST
        raise err

    if stat != status.HTTP_200_OK:
        raise HTTPException(status_code=stat, detail=data)
    
    return data
