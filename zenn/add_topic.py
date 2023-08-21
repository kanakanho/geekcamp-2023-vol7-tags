import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

response = requests.get("https://zenn.dev/api/articles")
articles_json = response.json()["articles"]

# pathを取得
paths = [article["path"] for article in articles_json]
print(paths)
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
            tag = tag[1:]

        # タグの重複チェック
        existing_tag = c.execute("SELECT * FROM node WHERE node=?", (tag,)).fetchone()
        if not existing_tag:
            c.execute("INSERT INTO node(node) VALUES (?)", (tag,))
            conn.commit()

            # tags のほかのtagを取得
            other_tags = [other_tag for other_tag in tags if other_tag != tag]
            tag_id = c.execute("SELECT id FROM node WHERE node=?", (tag,)).fetchone()[0]

            # connection_strengthの値を取得
            strength = c.execute(
                "SELECT connection_strength FROM connection WHERE node_id=?", (tag_id,)
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

conn.close()
