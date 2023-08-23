import requests

i = 22
response = requests.get(f"https://zenn.dev/api/articles{i}")
articles_json = response.json()["articles"]

print(articles_json)
