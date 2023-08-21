import sqlite3

dbname = "data.db"
# DBを作成する（既に作成されていたらこのDBに接続する）
conn = sqlite3.connect(dbname)

# SQLiteを操作するためのカーソルを作成
cur = conn.cursor()

# テーブルの作成
cur.execute(
    "CREATE TABLE node(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, items_count INTEGER)"
)
cur.execute("CREATE TABLE url(id INTEGER PRIMARY KEY AUTOINCREMENT, url STRING)")
cur.execute(
    "CREATE TABLE connection(id INTEGER PRIMARY KEY AUTOINCREMENT, node STRING, connect_node_id STRING, connection_strength INTEGER)"
)
