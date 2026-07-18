#!/usr/keio/Anaconda3-2025.12-2/bin/python

from wsgiref.handlers import CGIHandler
import os


# CGI の作業ディレクトリに依存せず、DB とテンプレートを読み込めるようにする。
application_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(application_dir)

# /index.cgi を利用者向けURLへ含めず、FlaskのURL生成を公開先に合わせる。
os.environ["SCRIPT_NAME"] = os.environ.get("SCRIPT_NAME", "").removesuffix(
    "/index.cgi"
)

from app import app


CGIHandler().run(app)
