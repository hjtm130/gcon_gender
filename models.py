from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    # __bind_key__ = 'private'
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
    # __bind_key__ = 'private'
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    ai_response = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    serious_score = db.Column(db.String(50), nullable=True)  # 深刻度フィールド
    system_message = db.Column(db.String(500), nullable=True)

    # 新規: Userモデルとのリレーション
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='chat_logs')

# タグモデル
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # リレーションシップ: 一つのタグは多くのティップに関連
    tips = db.relationship('Tip', secondary='tip_tags', back_populates='tags')

class Tip(db.Model):
    __tablename__ = 'tips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=True)
    agenda = db.Column(db.String(500), nullable=True)  # 議題
    expert_comment = db.Column(db.Text, nullable=True)  # 専門家によるコメント

    # 投票カウント
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

    # リレーションシップ
    tags = db.relationship('Tag', secondary='tip_tags', back_populates='tips')

# 中間テーブル: ティップとタグの多対多関係を管理
class TipTag(db.Model):
    __tablename__ = 'tip_tags'

    tip_id = db.Column(db.Integer, db.ForeignKey('tips.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)