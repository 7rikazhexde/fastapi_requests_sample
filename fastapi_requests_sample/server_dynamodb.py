from decimal import Decimal

import boto3
import uvicorn
from fastapi import FastAPI

# DynamoDBオブジェクトを取得
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

# テーブルオブジェクトを取得
table = dynamodb.Table("TestTable1")

app = FastAPI()


@app.get("/items/{item_id}/{date_val}")
def read_item(item_id: str, date_val: str):
    response = table.get_item(Key={"id": item_id, "date_val": date_val})
    item = response.get("Item")
    if item is not None:
        return item
    else:
        return {"error": "Item not found"}


@app.get("/items/")
def read_items():
    response = table.scan()
    items = response["Items"]
    return items


@app.get("/items/dates/{date_from}/{date_to}")
def get_items_dates(date_from: str, date_to: str):
    response = table.scan(
        FilterExpression="date_val between :date_from and :date_to",
        ExpressionAttributeValues={":date_from": date_from, ":date_to": date_to},
    )
    items = response["Items"]

    # 100は100.0とする
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                if value % 1 == 0:
                    item[key] = f"{value:.1f}"
                else:
                    item[key] = float(value)
    return items


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
