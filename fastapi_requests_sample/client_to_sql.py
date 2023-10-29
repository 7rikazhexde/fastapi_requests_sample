import requests

url = "http://localhost:5000/items/"
item_id = 1  # 取得したいアイテムのID

response = requests.get(f"{url}{item_id}")

print(response.status_code)
print(response.text)

print(response.json())
