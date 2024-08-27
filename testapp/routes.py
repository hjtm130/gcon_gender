from flask import render_template
from testapp import app

@app.route('/')
def index():
    return render_template('Home.html')
