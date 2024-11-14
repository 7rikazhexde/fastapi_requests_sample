import datetime
from typing import Any, Dict, Optional

import pymysql
import pymysql.cursors
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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


class Item(BaseModel):
    id: int = Field(alias="id")
    date: Optional[datetime.datetime] = Field(alias="date")
    action: Optional[str] = Field(alias="action")
    ps_data1: Optional[float] = Field(alias="ps_data1")
    ps_data2: Optional[float] = Field(alias="ps_data2")
    ps_data3: Optional[float] = Field(alias="ps_data3")
    ps_data4: Optional[float] = Field(alias="ps_data4")
    ps_data5: Optional[float] = Field(alias="ps_data5")
    ps_data6: Optional[float] = Field(alias="ps_data6")
    ps_data7: Optional[float] = Field(alias="ps_data7")
    ps_data8: Optional[float] = Field(alias="ps_data8")
    ps_data9: Optional[float] = Field(alias="ps_data9")
    ps_data10: Optional[float] = Field(alias="ps_data10")
    ps_data11: Optional[float] = Field(alias="ps_data11")
    ps_data12: Optional[float] = Field(alias="ps_data12")
    ps_data13: Optional[float] = Field(alias="ps_data13")
    ps_data14: Optional[float] = Field(alias="ps_data14")
    ps_data15: Optional[float] = Field(alias="ps_data15")
    ps_data16: Optional[float] = Field(alias="ps_data16")
    ps_data17: Optional[float] = Field(alias="ps_data17")
    ps_data18: Optional[float] = Field(alias="ps_data18")
    ps_data19: Optional[float] = Field(alias="ps_data19")
    ps_data20: Optional[float] = Field(alias="ps_data20")
    ps_data21: Optional[float] = Field(alias="ps_data21")
    ps_data22: Optional[float] = Field(alias="ps_data22")
    ps_data23: Optional[float] = Field(alias="ps_data23")
    ps_data24: Optional[float] = Field(alias="ps_data24")
    ps_data25: Optional[float] = Field(alias="ps_data25")
    ps_data26: Optional[float] = Field(alias="ps_data26")
    ps_data27: Optional[float] = Field(alias="ps_data27")
    ps_data28: Optional[float] = Field(alias="ps_data28")
    ps_data29: Optional[float] = Field(alias="ps_data29")
    ps_data30: Optional[float] = Field(alias="ps_data30")
    ps_data31: Optional[float] = Field(alias="ps_data31")
    ps_data32: Optional[float] = Field(alias="ps_data32")
    ps_data33: Optional[float] = Field(alias="ps_data33")
    ps_data34: Optional[float] = Field(alias="ps_data34")
    ps_data35: Optional[float] = Field(alias="ps_data35")
    ps_data36: Optional[float] = Field(alias="ps_data36")
    ps_data37: Optional[float] = Field(alias="ps_data37")
    ps_data38: Optional[float] = Field(alias="ps_data38")
    ps_data39: Optional[float] = Field(alias="ps_data39")
    ps_data40: Optional[float] = Field(alias="ps_data40")
    ps_data41: Optional[float] = Field(alias="ps_data41")
    ps_data42: Optional[float] = Field(alias="ps_data42")
    ps_data43: Optional[float] = Field(alias="ps_data43")
    ps_data44: Optional[float] = Field(alias="ps_data44")
    ps_data45: Optional[float] = Field(alias="ps_data45")
    ps_data46: Optional[float] = Field(alias="ps_data46")
    ps_data47: Optional[float] = Field(alias="ps_data47")
    ps_data48: Optional[float] = Field(alias="ps_data48")
    ps_data49: Optional[float] = Field(alias="ps_data49")
    ps_data50: Optional[float] = Field(alias="ps_data50")
    ps_data51: Optional[float] = Field(alias="ps_data51")
    ps_data52: Optional[float] = Field(alias="ps_data52")
    ps_data53: Optional[float] = Field(alias="ps_data53")


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


@app.get("/items/{id}", response_model=Item)
async def read_item(id: int) -> Dict[str, Any]:
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sample_tbl1 WHERE id=%s", (id,))
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Item not found")
    # type check用にDict[str, Any]を明示的に指定
    result: Dict[str, Any] = rows[0]
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
