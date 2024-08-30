from flask import Flask
from models import db, migrate, User
from flask import render_template, request, redirect, url_for, session

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprintsの登録
    from routes import main_bp
    app.register_blueprint(main_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
