from flask_socketio import emit, join_room, leave_room
from models import db, CounselorChatMessage
from app import socketio
from flask import session

def register_events(socketio):
    @socketio.on('join')
    def handle_join(data):
        room = data['room']
        username = session.get('username')
        join_room(room)
        emit('status', {'msg': f'{username} has entered the room.'}, room=room)

    @socketio.on('leave')
    def handle_leave(data):
        room = data['room']
        username = session.get('username')
        leave_room(room)
        emit('status', {'msg': f'{username} has left the room.'}, room=room)

    @socketio.on('message')
    def handle_message(data):
        message = Message(room=data['room'], sender=session.get('username'), content=data['message'])
        db.session.add(message)
        db.session.commit()
        emit('response', data, room=data['room'])