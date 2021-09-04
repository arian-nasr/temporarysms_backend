from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')
twilio_sid = os.environ.get('TWILIO_SID')
twilio_secret = os.environ.get('TWILIO_SECRET')
client = Client(twilio_sid, twilio_secret)

@app.route('/api/incomingmessage/<id>', methods=['POST'])
def inbound_sms(id):
    response = MessagingResponse()
    message_sender = request.form['From']
    message_body = request.form['Body']
    message_date = datetime.now()
    #sql.write_to_database(id, message_date, message_sender, message_body)
    socketio.emit('message', {'sender': message_sender, 'body': message_body, 'date': message_date}, room=id)
    return str(response)

@app.route('/api/readmessages/<id>', methods=['GET'])
def allmessages(id):
    #messages = sql.read_messages_from_database('phone1')
    # return jsonify({
    #     'status': 'success',
    #     'messages': messages
    # })
    return True

@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.21')