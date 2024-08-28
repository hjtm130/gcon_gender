from flask import render_template
from testapp import app

@app.route('/')
def index():
    return render_template('Home.html')
@app.route('/AIChat')
def index():
    return render_template('AIChat.html')
@app.route('/CounselorChat')
def index():
    return render_template('CounselorChat.html')
@app.route('/Tips')
def index():
    return render_template('Tips.html')
@app.route('/JuniorHighSchool')
def index():
    return render_template('JuniorHighSchool.html')
@app.route('/HighSchool')
def index():
    return render_template('HighSchool.html')