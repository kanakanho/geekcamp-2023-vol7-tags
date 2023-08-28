import sqlite3
import pandas as pd

# db読み込み
conn = sqlite3.connect("qiita.db")
c = conn.cursor()

# dfに変換
df_qiita = pd.read_sql(
    "SELECT tag,items_count FROM node ORDER BY items_count DESC", conn
)

# items_countから正規化
df_qiita["items_count"] = df_qiita["items_count"] / df_qiita["items_count"].max()

conn.close()

# db読み込み
conn = sqlite3.connect("zenn.db")
c = conn.cursor()

# dfに変換
df_zenn = pd.read_sql(
    "SELECT node,items_count FROM node WHERE items_count > 1 ORDER BY items_count DESC",
    conn,
)

# items_countから正規化
df_zenn["items_count"] = df_zenn["items_count"] / df_zenn["items_count"].max()

conn.close()
# # csvに出力
# df.to_csv("zenn.csv", index=False)

print(df_qiita)
print(df_zenn)

# df_qiitaをdbに書き込み
pd.io.sql.to_sql(
    df_qiita,
    "qiita",
    conn,
    if_exists="replace",
    index=False,
    index_label=None,
    chunksize=None,
    dtype=None,
    method=None,
)

pd.io.sql.to_sql(
    df_zenn,
    "zenn",
    conn,
    if_exists="replace",
    index=False,
    index_label=None,
    chunksize=None,
    dtype=None,
    method=None,
)
