from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db, User, ChatLog, Tip, Tag, TipTag, CounselorChat, CounselorChatMessage, CounselorChatRoom # データベースのインポート
import openai
from markupsafe import escape
import os
import sqlite3
from flask_socketio import emit
from app import app, socketio

# Blueprintの作成
main_bp = Blueprint('main', __name__)

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = request.form['status']
        user = User.query.filter_by(username=username, status=status).first()
        if user is None:
            new_user = User(username=username, status=status)
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
        status = request.form['status']
        user = User.query.filter_by(username=username, status=status).first()
        if user and user.check_password(password):
            if user:
                session['userid'] = user.id
                session['username'] = user.username
                session['status'] = user.status
                if user.status == 'admin':
                    return redirect(url_for('main.admin_dashboard'))
                elif user.status == 'user':
                    return redirect(url_for('main.user_dashboard'))
                elif user.status == 'counselor':
                    return redirect(url_for('main.counselor_dashboard'))
            else:
                return 'Invalid username, password, or status', 401
        else:
                return 'Invalid username, password, or status', 401
    return render_template('Login.html')

@main_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('status', None)
    return redirect(url_for('main.home'))

@main_bp.route('/')
def home():
    return render_template('Home.html')

@main_bp.route('/home')
def user_dashboard():
    if session['status'] == 'user':
        return render_template('User_dashboard.html')
    elif session['status'] == 'counselor':
        return render_template('Counselor_dashboard.html')
    else:
        return redirect(url_for('main.access_error'))

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
    return render_template('before_header.html')
@main_bp.route('/header_after')
def header_after():
    username = session.get('username')
    status = session.get('status')
    return render_template('after_header.html', username=username, status=status)

@main_bp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('Tips/tags.html', tags=tags)

@main_bp.route('/<tag_id>')
def tips_by_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tips = tag.tips
    return render_template('Tips/tips_by_tag.html', tag=tag, tips=tips)

# counselorログイン後
@main_bp.route('/counselor_dashboard')
def counselor_dashboard():
    if session['status'] == 'counselor':
        return render_template('Counselor/Counselor_dashboard.html')
    else:
        return redirect(url_for('main.access_error'))

# adminログイン後
@main_bp.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if session['status'] == 'admin':
        status = None
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

            elif 'status' in request.form:
                status = request.form.get('status')
        
        tags = Tag.query.all()
        tips = Tip.query.all()
        users = User.query.filter_by(status=status).all() if status else User.query.all()
        return render_template('Admin/admin_dashboard.html', tags=tags, tips=tips, users=users)
    else:
        return redirect(url_for('main.access_error'))

@main_bp.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag(tag_id):
    if session['status'] == 'admin':
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('main.admin_dashboard'))
    else:
        return redirect(url_for('main.access_error'))

@main_bp.route('/delete_tip/<int:tip_id>', methods=['POST'])
def delete_tip(tip_id):
    if session['status'] == 'admin':
        tip = Tip.query.get_or_404(tip_id)
        db.session.delete(tip)
        db.session.commit()
        return redirect(url_for('main.admin_dashboard'))
    else:
        return redirect(url_for('main.access_error'))

@main_bp.route('/403error')
def access_error():
    return render_template('403error.html')

#カウンセラーチャット関係の処理
@main_bp.route('/CounselorChat')
def counselor():
    if session['status'] == 'user':
        return render_template('CounselorChat/user.html')
    elif session['status'] == 'counselor':
        return render_template('CounselorChat/counselor.html')
    else:
        return redirect(url_for('main.access_error'))

@main_bp.route('/search', methods=['GET'])
def search():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            counselors = User.query.filter(User.username != user.username).all()
            return render_template('CounselorChat/search.html', counselors=counselors)
    return redirect(url_for('CounselorChat'))

@main_bp.route('/select_counselor/<int:counselor_id>', methods=['GET'])
def select_counselor(counselor_id):
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            room = CounselorChatRoom.query.filter_by(user_id=user.id, counselor_id=counselor_id).first()
            if not room:
                room = CounselorChatRoom(user_id=user.id, counselor_id=counselor_id)
                db.session.add(room)
                db.session.commit()
            return redirect(url_for('chat', room_id=room.id))
    return redirect(url_for('CounselorChat'))

@app.route('/chat/<int:room_id>', methods=['GET'])
def chat(room_id):
    room = CounselorChatRoom.query.get(room_id)
    if room:
        messages = CounselorChatMessage.query.filter_by(room_id=room_id).all()
        return render_template('chat.html', room=room, messages=messages)
    return redirect(url_for('CounselorChat'))

@app.route('/counselor_chat', methods=['GET'])
def counselor_chat():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            rooms = CounselorChatRoom.query.filter_by(counselor_id=user.id).all()
            return render_template('CounselorChat/counselor_chat.html', rooms=rooms)
    return redirect(url_for('CounselorChat'))

# SocketIO events
@socketio.on('send_message')
def handle_message(data):
    new_message = CounselorChatMessage(
        room_id=data['room_id'],
        user_id=data['user_id'],
        message=data['message']
    )
    db.session.add(new_message)
    db.session.commit()
    emit('receive_message', data, room=data['room_id'])

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)