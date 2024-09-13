from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __bind_key__ = 'private'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=False, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class ChatLog(db.Model):
    __bind_key__ = 'private'
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    ai_response = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# タグモデル
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # リレーションシップ: 一つのタグは多くのティップに関連
    tips = db.relationship('Tip', secondary='tip_tags', back_populates='tags')

# ティップモデル
class Tip(db.Model):
    __tablename__ = 'tips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=True)
    
    # リレーションシップ: 一つのティップは多くのタグに関連
    tags = db.relationship('Tag', secondary='tip_tags', back_populates='tips')

# 中間テーブル: ティップとタグの多対多関係を管理
class TipTag(db.Model):
    __tablename__ = 'tip_tags'

    tip_id = db.Column(db.Integer, db.ForeignKey('tips.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class CounselorChatRoom(db.Model):
    __bind_key__ = 'private'
    __tablename__ = 'counselor_chat_room'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    counselor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class CounselorChatMessage(db.Model):
    __bind_key__ = 'private'
    __tablename__ = 'counselor_chat_message'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('counselor_chat_room.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class CounselorChat(db.Model):
    __bind_key__ = 'private'
    room_id = db.Column(db.Integer, db.ForeignKey('counselor_chat_room.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor_chat_message.id'), primary_key=True)