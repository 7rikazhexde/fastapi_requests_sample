from typing import Any, Dict, List, Optional, cast

import requests

endpoint = "http://localhost:5000/"


def get_item(item_id: str, date_val: str) -> Optional[Dict[str, Any]]:
    url = f"{endpoint}items/{item_id}/{date_val}"
    response = requests.get(url)
    if response.text:  # Check if the response is not empty
        try:
            return cast(Dict[str, Any], response.json())
        except ValueError:
            print(f"Unexpected response: {response.text}")
            return None
    else:
        return None


def get_items() -> Optional[List[Dict[str, Any]]]:
    url = f"{endpoint}items/"
    response = requests.get(url)
    if response.text:  # Check if the response is not empty
        try:
            return cast(List[Dict[str, Any]], response.json())
        except ValueError:
            print(f"Unexpected response: {response.text}")
            return None
    else:
        return None


def get_items_dates(date_from: str, date_to: str) -> Optional[List[Dict[str, Any]]]:
    url = f"{endpoint}items/dates/{date_from}/{date_to}"
    response = requests.get(url)
    if response.text:  # Check if the response is not empty
        try:
            return cast(List[Dict[str, Any]], response.json())
        except ValueError:
            print(f"Unexpected response: {response.text}")
            return None
    else:
        return None


if __name__ == "__main__":
    item = get_item(
        "1", "2023-03-04T00:05:14.487122"
    )  # Replace with your actual date value
    if item is not None:
        print(item)
    else:
        print("No item found.")

    items = get_items()
    if items is not None:
        print(items)
    else:
        print("No items found.")

    items = get_items_dates(
        "2023-03-03", "2023-03-06"
    )  # Replace with your actual date range
    print(f"items:{items}")
    if items is not None:
        print(items)
    else:
        print("No items found.")
