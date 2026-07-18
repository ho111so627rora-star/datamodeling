# 採用選考管理システム

データモデリング最終課題として作成した、企業の採用情報を管理するWebアプリケーションです。

## 使用環境

- Python 3.13
- Flask 3.1.2
- SQLite3
- データベース接続にはPython標準の `sqlite3` を使用

## ローカルでの初期化

`init_db.py` は空の状態からデータベースを作成するため、初回のみ実行します。

```sh
python init_db.py
```

## ローカルでの起動

```sh
python app.py
```

ブラウザで `http://127.0.0.1:5000` を開きます。

## WS Linux環境への配置

リモートデスクトップでログインした場合も、通常のターミナルから次を実行して
Anaconda用ターミナルを起動します。

```sh
anaconda-shell
```

最初に、授業で用意されたスクリプトを通常のターミナルから実行します。

```sh
~aa124123/dm/setup.sh
```

これにより `~/public_html/dm_app` にサンプルが配置され、公開URLが表示されます。
サンプルに含まれる `.htaccess` と `index.cgi` は変更も上書きも行いません。

サンプルの `app.py`、`database.db`、`templates` を、このアプリの `app.py`、
`recruitment.db`、`templates` に置き換え、`static` ディレクトリを追加します。
DBをWS上で新規作成する場合だけ、公開ディレクトリで次を実行します。

```sh
cd ~/public_html/dm_app
/usr/keio/Anaconda3-2025.12-2/bin/python init_db.py
```

Webサーバーは専用アカウントで動作するため、全ディレクトリと `index.cgi`、`app.py`
を755、その他のファイルを644に設定します。

```sh
chmod 755 ~/public_html ~/public_html/dm_app
cd ~/public_html/dm_app
chmod 755 index.cgi app.py templates static
chmod 644 recruitment.db init_db.py kdai3.sql insert.sql view.sql
chmod 644 templates/* static/*
```

ローカルデバッグはAnaconda用ターミナルで実行します。

```sh
cd ~/public_html/dm_app
flask --debug run
```

配置後は `setup.sh` が表示した公開URLから、一覧表示、登録、更新、削除、検索を確認します。

## 主な機能

- 採用状況ダッシュボード
- 候補者と応募の検索
- 候補者の登録・編集
- 年度別の応募登録・更新・削除
- 面接と評価の登録
- 選考ステージの自動更新
- ステージ別件数の集計
- ビューを利用した候補者・応募一覧
- CSRF対策とサーバー側バリデーション
