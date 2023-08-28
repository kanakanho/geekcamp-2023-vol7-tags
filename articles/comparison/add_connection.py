import sqlite3
import pandas as pd

# db読み込み
conn_qiita = sqlite3.connect("qiita.db")
cur_qiita = conn_qiita.cursor()

conn_zenn = sqlite3.connect("zenn.db")
cur_zenn = conn_zenn.cursor()

conn_com = sqlite3.connect("comparison.db")
cur_com = conn_com.cursor()


# qiita.dbのconnectionテーブルをcomparison.dbのconnectionテーブルに追加
cur_qiita.execute("SELECT node_id,connect_node_id,connection_strength FROM connection")
for row in cur_qiita.fetchall():
    cur_com.execute(
        "INSERT INTO connection(node, connect_node_id, connection_strength) VALUES (?, ?, ?)",
        (row[0], row[1], row[2]),
    )
    conn_com.commit()

# zenn.dbのconnectionテーブルをcomparison.dbのconnectionテーブルに追加
# 同じものがあればconnection_strengthを足す、なければそのまま追加
cur_zenn.execute("SELECT node,connect_node_id,connection_strength FROM connection")
for row in cur_zenn.fetchall():
    cur_com.execute(
        "SELECT * FROM connection WHERE node = ? AND connect_node_id = ?",
        (row[0], row[1]),
    )
    if cur_com.fetchone() is not None:
        cur_com.execute(
            "SELECT connection_strength FROM connection WHERE node = ? AND connect_node_id = ?",
            (row[0], row[1]),
        )
        connection_strength = cur_com.fetchone()
        add_connection_strength = row[2] + connection_strength[0]
        cur_com.execute(
            "UPDATE connection SET connection_strength = ? WHERE node = ? AND connect_node_id = ?",
            (add_connection_strength, row[0], row[1]),
        )
        conn_com.commit()
    else:
        cur_com.execute(
            "INSERT INTO connection(node, connect_node_id, connection_strength) VALUES (?, ?, ?)",
            (row[0], row[1], row[2]),
        )
        conn_com.commit()
