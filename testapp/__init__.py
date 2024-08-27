# testapp/__init__.py
from flask import Flask

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# アプリケーションの設定やルートのインポート
import testapp.routes as routes
