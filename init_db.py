import sqlite3


database = "recruitment.db"

with sqlite3.connect(database) as connection:
    connection.execute("PRAGMA foreign_keys = ON")
    for filename in ("kdai3.sql", "insert.sql", "view.sql"):
        with open(filename, encoding="utf-8") as sql_file:
            connection.executescript(sql_file.read())

print(f"データベースを作成しました: {database}")
