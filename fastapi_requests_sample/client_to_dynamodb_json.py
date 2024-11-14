from typing import Dict, List, Optional

import pandas as pd
import requests


def get_items() -> None:
    # FastAPIサーバーのURL
    endpoint = "http://localhost:5000/"
    url = f"{endpoint}items/"

    # GETリクエストを送る
    response = requests.get(url)

    # レスポンスをJSON形式で取得
    data = response.json()

    # データを表示
    for item in data["result"]:
        print(item)


def get_items_by_id(
    id: str,
    columns: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    # FastAPIサーバーのURL
    endpoint = "http://localhost:5000/"
    url = f"{endpoint}items/{id}/"

    # クエリパラメータ（start_dateとend_dateはオプション）
    params: Dict[str, str] = {}
    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date

    # GETリクエストを送る
    response = requests.get(url, params=params)

    # レスポンスをJSON形式で取得
    data = response.json()

    # data['result']の各要素（ここではitemと呼びます）に対して、
    # columnsリストの各要素（ここではcolumnと呼びます）を取得し、その結果を新しいリストに格納する。
    new_data = [[item[column] for column in columns] for item in data["result"]]

    # new_dataは上記で作成したリスト
    df = pd.DataFrame(new_data, columns=columns)
    return df


if __name__ == "__main__":
    columns = ["id", "date_val", "detected_status", "num_of_people"]
    get_items_by_id("camera1", columns)
    # get_items_by_id('camera1', columns,'2023-11-02', '2023-11-03')
    # get_items_by_id('camera1', columns,'2023-11-02T00:00:00', '2023-11-03T00:00:00')
    # get_items_by_id('camera1', columns,'2023-11-02T06:49:52.158', '2023-11-02T06:50:18.430')
    # get_items()
