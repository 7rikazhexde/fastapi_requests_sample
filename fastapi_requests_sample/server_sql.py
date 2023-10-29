import datetime
from typing import Optional

import pymysql
from fastapi import FastAPI
from pydantic import Field, create_model
from tomlkit.toml_file import TOMLFile

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
Item = create_model("Item", **fields)


def db_connection():
    conn = None
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
    except pymysql.err.OperationalError as e:
        print(e)
    return conn


@app.get("/items/{id}", response_model=Item)
async def read_item(id: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sample_tbl1 WHERE id=%s", (id,))
    rows = cursor.fetchall()
    if rows:
        return rows[0]
