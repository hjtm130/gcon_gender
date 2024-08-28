from flask import render_template
from testapp import app

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/AIChat')
def ai_chat():
    return render_template('AIChat.html')

@app.route('/CounselorChat')
def counselor_chat():
    return render_template('CounselorChat.html')

@app.route('/Tips')
def tips():
    return render_template('Tips.html')

@app.route('/JuniorHighSchool')
def junior_high_school():
    return render_template('JuniorHighSchool.html')

@app.route('/HighSchool')
def high_school():
    return render_template('HighSchool.html')
