import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import json
from time import sleep
import re

DB_PATH = "/comparison/comparison.db"

# データベースに接続
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# article_tmpのarticleを取得
cursor.execute("SELECT * FROM article_tmp")
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=["node_name", "article", "date"])
counter = 0
errors = []

for article in df["article"]:
    node_name = df["node_name"][counter]
    counter += 1
    article = (
        article.replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .replace("\u3000", "")
        .replace(" ", "")
    )
    # 正規表現で日本語を含む場合は翻訳しない
    if re.search("[ぁ-んァ-ン一-龥]", article):
        continue
    try:
        url = f"https://script.google.com/macros/s/AKfycbz75gst14sUdgdFBflmAs_91Eqbna6jZwDJ0g3o7jBc-2BDuKQgBu9WMjkpH8Qx_65ZHg/exec?text={article}&source=en&target=ja"
        output = requests.get(url)
        output = output.json()
        text = output["text"]
        cursor.execute(
            "UPDATE article_tmp SET article = ? WHERE node_name = ?", (text, node_name)
        )
        conn.commit()
        print(f"{counter}.commited:{node_name}")
        sleep(2)
    except:
        print(f"{counter}.commited:{node_name}.error")
        errors.append(node_name)

errors = pd.DataFrame(errors, columns=["node_name"])
errors.to_csv("errors.csv", index=False)
