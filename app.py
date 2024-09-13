from flask import Flask
from models import db, migrate
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///public.db'
    app.config['SQLALCHEMY_BINDS'] = {
        'private': 'sqlite:///private.db'
    }

    db.init_app(app)
    migrate.init_app(app, db)

    socketio.init_app(app, async_mode='eventlet')

    # Blueprintsの登録
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app

def create_socketio(app):
    socketio.init_app(app, async_mode='eventlet')
    from events import register_events
    register_events(socketio)

    return socketio

if __name__ == '__main__':
    app = create_app()
    socketio = create_socketio(app)

    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True)