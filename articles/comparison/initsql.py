import sqlite3

dbname = "comparison.db"
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)

# SQLiteを操作するためのカーソルを作成
cur = conn.cursor()

# テーブルの作成
# cur.execute(
#     "CREATE TABLE qiita(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, items_count INTEGER)"
# )
# cur.execute(
#     "CREATE TABLE zenn(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, items_count INTEGER)"
# )
# cur.execute(
#     "CREATE TABLE add_node(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, items_count INTEGER)"
# )
# cur.execute(
#     "CREATE TABLE connection(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, connect_node_id STRING, connection_strength INTEGER)"
# )

# articleを消す
cur.execute("DROP TABLE articles")

cur.execute(
    "CREATE TABLE articles(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, article STRING, date STRING)"
)
