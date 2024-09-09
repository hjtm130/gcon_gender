from flask import Flask
from models import db, migrate
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)
    app.config.from_pyfile('config.py', silent=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///public.db'
    app.config['SQLALCHEMY_BINDS'] = {
        'private': 'sqlite:///private.db'
    }

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
    app.run(debug=True, threaded=True)
