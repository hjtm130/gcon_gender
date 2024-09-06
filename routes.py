from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, ChatLog, Tip, Tag, TipTag # データベースのインポート
import openai
from markupsafe import escape
import os
import sqlite3

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
    conn = sqlite3.connect('chattest.db')
    cursor = conn.cursor()
    cursor.execute("select id, name from user")
    user_info = cursor.fetchall()
    conn.close()
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

@main_bp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('Tips/tags.html', tags=tags)

@main_bp.route('/tag/<tag_id>')
def tips_by_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tips = tag.tips
    return render_template('Tips/tips_by_tag.html', tag=tag, tips=tips)

@main_bp.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        # タグの追加
        if 'tag_name' in request.form:
            tag_name = request.form['tag_name']
            if tag_name:
                existing_tag = Tag.query.filter_by(name=tag_name).first()
                if not existing_tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.commit()
        
        # ティップの追加
        elif 'tip_title' in request.form and 'tip_content' in request.form:
            title = request.form['tip_title']
            content = request.form['tip_content']
            link = request.form.get('tip_link', '')
            tag_ids = request.form.getlist('tip_tags')

            if title and content:
                tip = Tip(title=title, content=content, link=link)
                for tag_id in tag_ids:
                    tag = Tag.query.get(int(tag_id))
                    if tag:
                        tip.tags.append(tag)
                db.session.add(tip)
                db.session.commit()
    
    tags = Tag.query.all()
    tips = Tip.query.all()
    return render_template('Admin/admin_dashboard.html', tags=tags, tips=tips)

@main_bp.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))

@main_bp.route('/delete_tip/<int:tip_id>', methods=['POST'])
def delete_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    db.session.delete(tip)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))

#カウンセラーチャット関係の処理