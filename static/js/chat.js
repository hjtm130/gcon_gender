var socket = io();

function sendMessage() {
    var message = document.getElementById('message_input').value;
    var roomId = {{ room.id }}; // Replace with actual room ID from the server
    var userId = 1; // Replace with actual user ID from the server
    socket.emit('send_message', {
        'room_id': roomId,
        'user_id': userId,
        'message': message
    });
    document.getElementById('message_input').value = '';
}

socket.on('receive_message', function(data) {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += '<div>' + data.message + '</div>';
});
