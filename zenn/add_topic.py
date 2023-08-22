import requests
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

conn = sqlite3.connect("data.db")
c = conn.cursor()

for i in range(1, 21):
    response = requests.get(f"https://zenn.dev/api/articles{i}")
    articles_json = response.json()["articles"]

    # pathを取得
    paths = [article["path"] for article in articles_json]
    # print(paths)
    for path in paths:
        # DBの中に同じpathがあるかどうかを確認
        c.execute("SELECT * FROM url WHERE url=?", (path,))
        # ある場合は操作をパス
        if c.fetchone() is not None:
            continue

        # pathをDBに保存
        c.execute("INSERT INTO url(url) VALUES (?)", (path,))

        # tagsを取得
        url = f"https://zenn.dev/{path}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # div class="View_topics__OVMdM"の中のaタグを取得
        tags = [tag.text for tag in soup.select("div.View_topics__OVMdM a")]

        # 最後の一個は消す
        tags.pop()
        print(tags)

        for tag in tags:
            # 文字列の最初に#がついていたら消す
            if tag[0] == "#":
                tag = tag.replace("#", "")

            # タグの重複チェック
            existing_tag = c.execute(
                "SELECT * FROM node WHERE node=?", (tag,)
            ).fetchone()
            if existing_tag:
                c.execute(
                    "UPDATE node SET items_count = items_count + 1 WHERE node=?", (tag,)
                )
                conn.commit()
            else:
                c.execute("INSERT INTO node(node, items_count) VALUES (?, ?)", (tag, 1))
                conn.commit()

            # tags のほかのtagを取得
            other_tags = [other_tag for other_tag in tags if other_tag != tag]
            tag_id = c.execute("SELECT id FROM node WHERE node=?", (tag,)).fetchone()[0]

            # connection_strengthの値を取得
            strength = c.execute(
                "SELECT connection_strength FROM connection WHERE node=?", (tag,)
            ).fetchone()

            if strength:
                strength = strength[0]
            else:
                strength = 0

            for other_tag in other_tags:
                c.execute(
                    "INSERT INTO connection(node, connect_node_id, connection_strength) VALUES (?, ?, ?)",
                    (tag, other_tag, strength + 1),
                )
                conn.commit()

        sleep(2)
    conn.close()
