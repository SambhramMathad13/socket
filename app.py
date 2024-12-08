import eventlet

# Monkey-patch for compatibility with eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SocketIO with eventlet support
socketio = SocketIO(app, async_mode='eventlet')

# Client status dictionary (to track whether a client is capturing or idle)
client_status = {}


@app.route('/')
def index():
    """Render the main dashboard HTML."""
    return render_template('index.html')


@socketio.on('send_command')
def handle_command(data):
    """
    Handle start/stop commands from the dashboard.
    Emit the command to the specific client.
    """
    client_id = data['clientId']
    command = data['command']
    print(f"Command '{command}' received for client '{client_id}'.")

    # Update client status
    client_status[client_id] = command

    # Send the command to the specific client's room
    emit('capture_command', {'command': command}, room=client_id)


@socketio.on('send_image')
def handle_image(data):
    """
    Receive an image from a capturing client, process it, and broadcast to all clients.
    """
    client_id = data['clientId']
    print(f"Image received from client: {client_id}")

    # Decode image data and process
    image_data = data['image']
    image_message = data['message']

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Broadcast image and message to all connected clients
    emit('new_image', {
        "clientId": client_id,
        "image": f"data:image/jpeg;base64,{image_data}",
        "message": image_message,
        "timestamp": timestamp  # Include timestamp for display
    }, broadcast=True)


@socketio.on('join')
def handle_join(data):
    """
    Handle client joining its specific room.
    """
    client_id = data['clientId']
    join_room(client_id)
    print(f"Client '{client_id}' joined its room.")


if __name__ == '__main__':
    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=10000)

# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit, join_room
# from datetime import datetime

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

# # Initialize SocketIO
# socketio = SocketIO(app)

# # Client status dictionary (to track whether a client is capturing or idle)
# client_status = {}


# @app.route('/')
# def index():
#     """Render the main dashboard HTML."""
#     return render_template('index.html')


# @socketio.on('send_command')
# def handle_command(data):
#     """
#     Handle start/stop commands from the dashboard.
#     Emit the command to the specific client.
#     """
#     client_id = data['clientId']
#     command = data['command']
#     print(f"Command '{command}' received for client '{client_id}'.")

#     # Update client status
#     client_status[client_id] = command

#     # Send the command to the specific client's room
#     emit('capture_command', {'command': command}, room=client_id)


# @socketio.on('send_image')
# def handle_image(data):
#     """
#     Receive an image from a capturing client, process it, and broadcast to all clients.
#     """
#     client_id = data['clientId']
#     print(f"Image received from client: {client_id}")

#     # Decode image data and process
#     image_data = data['image']
#     image_message = data['message']

#     # Get the current timestamp
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     # Broadcast image and message to all connected clients
#     emit('new_image', {
#         "clientId": client_id,
#         "image": f"data:image/jpeg;base64,{image_data}",
#         "message": image_message,
#         "timestamp": timestamp  # Include timestamp for display
#     }, broadcast=True)


# @socketio.on('join')
# def handle_join(data):
#     """
#     Handle client joining its specific room.
#     """
#     client_id = data['clientId']
#     join_room(client_id)
#     print(f"Client '{client_id}' joined its room.")


# if __name__ == '__main__':
#     # Run the Flask app with SocketIO
#     socketio.run(app, debug=True)
