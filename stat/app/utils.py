import boto3

from settings import AWS_CREDENTIALS


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

