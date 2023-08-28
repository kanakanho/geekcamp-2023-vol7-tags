import sqlite3
import pandas as pd


# dbに書き込み
conn = sqlite3.connect("comparison.db")
c = conn.cursor()

# comparison.dbからデータをdfに変換
df_comparison = pd.read_sql(
    "SELECT tag,items_count FROM qiita ORDER BY items_count DESC", conn
)

# df_comparisonの中身を一つずつ表示
for row in df_comparison.itertuples():
    print(row.tag, row.items_count)


# df_comparisonに登場したnodeがcomparison.dbのzennテーブルにあるか確認、あれば値を足して2で割る、その後add_nodeテーブルに追加、なければそのままadd_nodeテーブルに追加
for row in df_comparison.itertuples():
    c.execute("SELECT node FROM zenn WHERE node = ?", (row.tag,))
    if c.fetchone() is not None:
        c.execute("SELECT items_count FROM zenn WHERE node = ?", (row.tag,))
        zenn_items_count = c.fetchone()
        add_items_count = (row.items_count + zenn_items_count[0]) / 2
        c.execute(
            "INSERT INTO add_node(node, items_count) VALUES (?, ?)",
            (row.tag, add_items_count),
        )
        conn.commit()
    else:
        c.execute(
            "INSERT INTO add_node(node, items_count) VALUES (?, ?)",
            (row.tag, row.items_count),
        )
        conn.commit()

# add_nodeに存在していないnodeをzennから取得、その後add_nodeに追加
c.execute(
    "SELECT node,items_count FROM zenn WHERE node NOT IN (SELECT node FROM add_node)"
)
for row in c.fetchall():
    c.execute("INSERT INTO add_node(node, items_count) VALUES (?, ?)", (row[0], row[1]))
    conn.commit()

conn.close()
