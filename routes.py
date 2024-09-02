from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, ChatLog # データベースのインポート
import openai
from markupsafe import escape
import os

# Blueprintの作成
main_bp = Blueprint('main', __name__)

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            # ユーザー名がすでに存在する場合の処理
            return "Username already exists!"
    return render_template('Signup.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
             return redirect(url_for('main.home'))
        else:
            # ログイン失敗の場合の処理
            return "Invalid username or password!"
    return render_template('Login.html')

@main_bp.route('/')
def home():
    return render_template('Home.html')

# --------AIchatに関する処理--------

# 環境変数からAPIキーを取得
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key

@main_bp.route('/AIChat', methods=['GET'])
def aichat_page():
    return render_template('AIChat.html')

@main_bp.route('/create_text', methods=['POST'])
def create_text():
    message = request.form['message']
    
    # 過去のチャットログを取得する
    past_logs = ChatLog.query.order_by(ChatLog.created_at.desc()).all()
    
    # ログからメッセージをフォーマットする
    messages = []
    for log in reversed(past_logs):  # 最新のログが先に来るように逆順で処理
        messages.append({"role": "user", "content": log.user_message})
        messages.append({"role": "assistant", "content": log.ai_response})
    
    # 現在のメッセージを追加
    messages.append({"role": "user", "content": message})
    
    # OpenAI APIを使って応答を生成
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    generated_text = res['choices'][0]['message']['content']
    generated_text = escape(generated_text)
    
    # チャットログをデータベースに保存
    chat_log = ChatLog(user_message=message, ai_response=generated_text)
    db.session.add(chat_log)
    db.session.commit()
    
    return jsonify({'message': generated_text})


@main_bp.route('/chat_logs', methods=['GET'])
def chat_logs():
    logs = ChatLog.query.order_by(ChatLog.created_at.desc()).all()
    return render_template('chat_logs.html', logs=logs)

@main_bp.route('/get_chat_log', methods=['GET'])
def get_chat_log():
    chat_logs = ChatLog.query.order_by(ChatLog.id.asc()).all()
    chat_log_list = [{'user_message': chat.user_message, 'ai_response': chat.ai_response} for chat in chat_logs]
    return jsonify(chat_log_list)

@main_bp.route('/delete_logs', methods=['POST'])
def delete_logs():
    # チャットログを全て削除
    ChatLog.query.delete()
    db.session.commit()
    
    # JSONレスポンスを返す
    return jsonify({'message': 'ログが削除されました！'})

#-------------以上---------------

@main_bp.route('/CounselorChat')
def counselor_chat():
    return render_template('CounselorChat.html')

@main_bp.route('/Tips')
def tips():
    return render_template('Tips.html')

@main_bp.route('/JuniorHighSchool')
def junior_high_school():
    return render_template('JuniorHighSchool.html')

@main_bp.route('/HighSchool')
def high_school():
    return render_template('HighSchool.html')

@main_bp.route('/header')
def header():
    return render_template('header.html')