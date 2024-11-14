import datetime
from typing import Optional, TypedDict

import pymysql
import pymysql.cursors
from fastapi import FastAPI, HTTPException
from pydantic import Field, create_model
from tomlkit.toml_file import TOMLFile


# ItemDict型を定義
class ItemDict(TypedDict):
    id: int
    date: Optional[datetime.datetime]
    action: Optional[str]
    # ps_data1 through ps_data53 を動的に追加
    ps_data1: Optional[float]  # 例として1つ定義


# Obtaining database connection information
toml = TOMLFile("./config.toml")
toml_data = toml.read()
toml_get_data = toml_data.get("database-mac")

HOST = toml_get_data["HOST"]
PORT = int(toml_get_data["PORT"])
USER = toml_get_data["USER"]
PASSWORD = toml_get_data["PASSWORD"]
DATABASE = toml_get_data["DATABASE"]
TABLE = toml_get_data["TABLE"]

app = FastAPI()

# Define the fields for the Item class
fields = {
    "id": (int, Field(alias="id")),
    "date": (Optional[datetime.datetime], Field(alias="date")),
    "action": (Optional[str], Field(alias="action")),
}
for i in range(1, 54):
    fields[f"ps_data{i}"] = (Optional[float], Field(alias=f"ps_data{i}"))

# Dynamically create the Item class
ItemModel = create_model("ItemModel", **fields)


def db_connection() -> pymysql.connections.Connection:
    try:
        conn = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except pymysql.err.OperationalError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database connection error")


@app.get("/items/{id}", response_model=ItemModel)
async def read_item(id: int) -> ItemDict:
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sample_tbl1 WHERE id=%s", (id,))
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Item not found")
    return rows[0]  # type: ignore
