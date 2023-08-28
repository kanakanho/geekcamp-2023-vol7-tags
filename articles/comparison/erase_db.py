import sqlite3

conn = sqlite3.connect("comparison.db")
c = conn.cursor()

text = "勉強メモ"

c.execute("DELETE FROM connection WHERE node = ?", (text,))
c.execute("DELETE FROM connection WHERE connect_node_id = ?", (text,))

# connectionテーブルからnodeとconnect_node_idが同じものを消す
# c.execute(
#     "DELETE FROM connection WHERE node = connect_node_id AND node NOT IN (SELECT node FROM add_node)"
# )


conn.commit()
