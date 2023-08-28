import requests
import os
from dotenv import load_dotenv
import sqlite3
import datetime
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re

DB_PATH = "comparison/comparison.db"
# GITHUB_TOKENを環境変数から取得
load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# データベースに接続
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 今日の日付を取得
today = datetime.date.today()
today = str(today)
today = today.replace("-", ".")
today = str(today[2:])

nodes = []
# nodeの名前を取得
cursor.execute("SELECT node FROM add_node")
rows = cursor.fetchall()
for row in rows:
    nodes.append(row[0])

until_nodes = []
# node_namesの中で、articlesにないものを取得
cursor.execute("SELECT node FROM articles")
rows = cursor.fetchall()
for row in rows:
    until_nodes.append(row[0])

node_names = []
# あるものは削除
for row in nodes:
    if row not in until_nodes:
        node_names.append(row)


def get_summary_from_github(query):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"https://api.github.com/search/topics?per_page=100&q={query}"
    response = requests.get(url, headers=headers)
    data = response.json()
    low_query = query.lower()
    up_query = query.upper()
    # "name"とquerryの一致するものの、"description","updated_at"を取得
    try:
        for item in data["items"]:
            if (
                item["name"] == query
                or item["name"] == low_query
                or item["name"] == up_query
            ):
                last_up = item["updated_at"]
                last_up = last_up.replace("-", ".")
                # 最初の7文字を取得
                last_up = last_up[:10]
                description = item["description"]

                if description == "NULL":
                    get_summary_from_wikipedia_ja(query)
                # article版の対応するtagのdbのarticleのNULLに書き出す
                cursor.execute(
                    "UPDATE articles SET article = ?, date = ? WHERE node = ?",
                    (description, today, query),
                )
                conn.commit()
                print(f"github:{query}")
    except:
        get_summary_from_wikipedia_ja(query)


def get_summary_from_wikipedia_ja(query):
    text = ""
    url = f"https://ja.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    data = response.json()
    text = data.get("extract", "")
    # textが複数行のとき、textの中身を全て消す
    if "\n" in text:
        text = ""

    # textが空じゃないとき
    if text:
        # article版の対応するtagのdbのarticleのNULLに書き出す
        cursor.execute(
            "UPDATE articles SET article = ?, date = ? WHERE node = ?",
            (text, today, query),
        )
        conn.commit()
        print(f"wiki_ja:{query}")
    else:
        get_summary_from_wikipedia_en(query)


def get_summary_from_wikipedia_en(query):
    text = ""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    data = response.json()
    text = data.get("extract", "")
    # textが複数行のとき、textの中身を全て消す
    if "\n" in text:
        text = ""

    # textが空じゃないとき
    if text:
        cursor.execute(
            "UPDATE articles SET article = ?, date = ? WHERE node = ?",
            (text, today, query),
        )
        conn.commit()
        print(f"wiki_en:{query}")
    else:
        get_summary_from_google(query)


articles = []


def get_summary_from_google(query):
    text = ""
    url = f"https://www.google.com/search?q={query}+%E3%81%A8%E3%81%AF"
    response = requests.get(url)
    sleep(1)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    # span class="BNeawe"の中のテキストを取得
    # text_shift = soup.find("span", class_="BNeawe").get_text()
    try:
        text = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
    except:
        return False
    # text = text.replace(text_shift, "")
    # 最初に"関連する質問"が出てくるとき、yyyy/mm/ddが最初に出てきくるとき、もう一度実行する
    if (
        "関連する質問" in text
        or re.match(r"^\d{4}/\d{1,2}/\d{1,2}", text)
        or re.search(r".+ · ", text)
        or re.search(r"\.\.\.", text)
        or re.search(r"Weblio英和・和英辞書", text)
    ):
        with open("err_num.txt", mode="r", encoding="utf-8") as f:
            err_num = f.read()
        err_num = int(err_num)
        err_num += 1
        with open("err_num.txt", mode="w", encoding="utf-8") as f:
            f.write(str(err_num))
        pass
    else:
        # textの"ウィキペディア"より後ろを全て消す
        text = text.split("ウィキペディア")[0]
        # "{query}すべて表示"は消す
        text = text.replace(f"{query}すべて表示", "")
        text = re.sub(r"概要 ", "", text)
        print(text)
        articles.append(text)
        cursor.execute(
            "UPDATE article_tmp SET article = ? ,last_update = ? WHERE node_name = ?",
            (text, today, query),
        )
        conn.commit()
        # df = pd.DataFrame(articles, columns=["article"])
        # df.to_csv("google_articles.csv", index=False)
        # print(f"{node_name}: {node_name}のarticleを取得しました")


# データを取得
for node_name in node_names:
    get_summary_from_github(node_name)
    sleep(2)
