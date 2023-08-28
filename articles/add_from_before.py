import sqlite3

DB_qiita_PATH = "comparison/qiita.db"
DB_comparison_PATH = "comparison/comparison.db"

# データベースに接続
conn_qiita = sqlite3.connect(DB_qiita_PATH)
cursor_qiita = conn_qiita.cursor()

conn_comparison = sqlite3.connect(DB_comparison_PATH)
cursor_comparison = conn_comparison.cursor()

# article_tmpのarticleを取得
cursor_qiita.execute("SELECT * FROM article_tmp")

rows = cursor_qiita.fetchall()

for row in rows:
    node_name = row[0]
    article = row[1]
    date = row[2]

    # INSERT文で値を提供するカラムを明示的に指定
    cursor_comparison.execute(
        "INSERT INTO articles (node, article, date) VALUES (?, ?, ?)",
        (node_name, article, date),
    )

    conn_comparison.commit()  # コミットはコネクションに対して行う
    print(f"commited:{node_name}")

conn_qiita.close()
conn_comparison.close()
