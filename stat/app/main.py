import stat
from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException

from botocore.exceptions import ClientError

from models import Page
from utils import init_db, DynamoDBFields, check_page_exists


db = init_db()
app = FastAPI() 


@app.post("/create_page")
async def new_page(page: Page):
    item = db.Table("Pages").get_item(Key={"id": page.id})
    
    if DynamoDBFields.ITEM in item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Page already exist."
        )
    
    db.Table("Pages").put_item(Item=page.dict())
    
    return page 


@app.put("/update_page")
async def update_page(page_name: str, user_id: str, page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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
    

@app.delete("/delete_page")
async def delete_page(user_id: str, page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
    check_page_exists(page=item)
    
    if item[DynamoDBFields.ITEM]["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not permissions to perform this operation."
        ) 
    
    db.Table("Pages").delete_item(Key={"id": page_id})
    
    return {"Status": "Deleted"}


@app.get("/pages", response_model=list[Page])
async def get_pages(user_id: str):
    response = db.Table("Pages").query(
        IndexName="user_id",
        KeyConditionExpression="user_id=:user_id",
        ExpressionAttributeValues={
            ":user_id": user_id
        }
    )
    
    return response[DynamoDBFields.ITEMS]
    

@app.put("/pages/{page_id}/new_like/", response_model=Page)
async def new_like(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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


@app.put("/pages/{page_id}/new_follower/", response_model=Page)
async def new_follower(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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


@app.put("/pages/{page_id}/new_follow_request/", response_model=Page)
async def new_follow_request(page_id: str):
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
    
    
@app.put("/pages/{page_id}/undo_like/", response_model=Page)
async def undo_like(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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


@app.put("/pages/{page_id}/undo_follower/", response_model=Page)
async def undo_follower(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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


@app.put("/pages/{page_id}/undo_follow_request/", response_model=Page)
async def undo_follow_request(page_id: str):
    item = db.Table("Pages").get_item(Key={"id": page_id})
    
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

