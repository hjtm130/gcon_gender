from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User

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

@main_bp.route('/AIChat')
def ai_chat():
    return render_template('AIChat.html')

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