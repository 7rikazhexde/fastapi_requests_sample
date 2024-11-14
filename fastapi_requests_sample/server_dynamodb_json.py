from typing import Dict, List, Optional

import boto3
import uvicorn
from boto3.dynamodb.conditions import Key
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# DynamoDBオブジェクトを取得
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

# テーブルオブジェクトを取得
table = dynamodb.Table("tbl_json1")


# レスポンスの形式を定義
class Item(BaseModel):
    detected_date_time: str
    date_val: str
    detected_status: str
    id: str
    skeletal_points: str
    num_of_people: str


app = FastAPI()


@app.get("/items/", response_model=Dict[str, List[Item]])
async def read_items() -> Dict[str, List[Item]]:
    # DynamoDBから全てのアイテムを取得
    response = table.scan()

    # 'result'キーでラップして返す
    return {"result": response["Items"]}


@app.get("/items/{id}/", response_model=Dict[str, List[Item]])
async def read_items_by_id(
    id: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> Dict[str, List[Item]]:
    if start_date and end_date:
        # start_dateとend_dateが指定されている場合、その範囲内のアイテムを取得する
        response = table.query(
            KeyConditionExpression=Key("id").eq(id)
            & Key("date_val").between(start_date, end_date)
        )
    else:
        # start_dateとend_dateが指定されていない場合、指定されたidのすべてのアイテムを取得する
        response = table.query(KeyConditionExpression=Key("id").eq(id))

    # アイテムが見つからない場合は404エラーを返す
    if not response["Items"]:
        raise HTTPException(status_code=404, detail="Items not found")

    # 'result'キーでラップして返す
    return {"result": response["Items"]}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
