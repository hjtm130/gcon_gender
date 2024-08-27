from flask import Flask, render_template, jsonify, request
from markupsafe import escape
import openai  # openaiパッケージを直接インポート
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Flaskアプリケーションの初期化
app = Flask(__name__)

# OpenAI APIキーの設定
openai.api_key = openai_api_key

# テキスト生成関数
def text_generate(message=None):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"以下の質問に答えてあげてください：{message}",
            }
        ]
    )
    
    # GPT-3.5からの応答を抽出
    generated_text = res['choices'][0]['message']['content']
    return generated_text

# トップページのルート
@app.route('/', methods=['GET'])
def toppage():
    return render_template('AIChat.html')

# テキスト生成エンドポイント
@app.route('/create_text', methods=['POST'])
def create_text():
    message = request.form['message']
    generated_text = text_generate(message=message)
    generated_text = escape(generated_text)
    return jsonify({'message': generated_text})

# アプリケーションのエントリーポイント
if __name__ == '__main__':
    app.run(debug=True)