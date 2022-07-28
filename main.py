##
# Author  : Sandroputraa
# Name    : Main Script - WhatsApp Blaster
# Build   : 28-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

import webbrowser
import os
import base64
import sys
import time
from flask import Flask, render_template, request, url_for, jsonify, redirect, flash
from flask_paginate import Pagination, get_page_args
from src import WhatsappMain, Database
from flask_socketio import SocketIO, emit
from flask_ckeditor import CKEditor
from datetime import datetime
import eventlet
from engineio.payload import Payload
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from colorama import init, Fore
from eventlet.hubs import epolls, kqueue, selects
from dns import dnssec, e164, namedict, tsigkeyring, update, version, zone

eventlet.monkey_patch()
init(autoreset=True)

Payload.max_decode_packets = 500
app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

file_path = os.path.abspath(os.getcwd()) + "\database.db"

app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

MAX_BUFFER_SIZE = 50 * 1000 * 1000
socketio = SocketIO(app, max_http_buffer_size=MAX_BUFFER_SIZE)
database = Database.Database(file_path)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)
whatsapp = WhatsappMain.WhatsappMain()

count_success_msg = 0
count_failed_msg = 0


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))


@login_manager.user_loader
def get(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('User not found')
            return render_template('sign-in.html')

        if user.username == username and user.password == password:

            login_user(user)
            return redirect('/')
        else:
            flash('Invalid password')
            return redirect('/login')
    else:
        return render_template('sign-in.html')


@app.route('/')
@login_required
def index():
    return render_template('dashboard.html', userlogin=current_user.username)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')


def log_all_messages(message, to, status):
    database.insert("tb_log", "message, contact, status, added_at",
                    "'{}', '{}', '{}', '{}'".format(message, to, status, datetime.now()))


@app.route('/contactlist')
@login_required
def contactlist():
    if whatsapp.session == '':
        return redirect(url_for('index'))

    contact_list = whatsapp.get_all_contact()

    def get_users(offset=0, per_page=10):
        return contact_list[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(contact_list),
                            css_framework='bootstrap4')

    return render_template('contactlist.html', users=pagination_users, page=page, per_page=15, pagination=pagination)


@socketio.on('connect')
def connect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Client connected')


@socketio.on('check_client_whatsapp')
def check_client_whatsapp():
    if whatsapp.check_whatsapp_logedin():
        emit('response_button_connect', {'data': 'Whatsapp Client Terkoneksi 🚀', 'status': 'True'})
        emit('response_info_loggedin',
             {'data': whatsapp.info_loggedin(), 'total_contact': str(len(whatsapp.get_all_contact())), 'status': 'True',
              'type': 'info'})
    else:
        emit('response_button_connect', {'data': 'Whatsapp Client Tidak Terkoneksi ❗️', 'status': 'False'})


@socketio.on('check_contact_whatsapp')
def check_contact_whatsapp():
    if whatsapp.check_whatsapp_logedin():
        emit('response_contact_list', {'data': whatsapp.get_all_contact(), 'status': 'True', 'type': 'contact'})
    else:
        emit('response_contact_list', {'data': '', 'status': 'False', 'type': 'contact'})


@socketio.on('connect_whatsapp')
def connect_whatsapp():
    emit('response_connect_whatsapp', {'data': 'Processing WhatsApp Browser', 'type': 'msg'})
    whatsapp.build_driver()
    socketio.sleep(0.5)
    emit('response_connect_whatsapp', {'data': 'Whatsapp Browser Opened', 'type': 'msg'})
    socketio.sleep(2)
    for i in range(30):
        whatsapp.scan_qr()
        emit('response_connect_whatsapp', {'data': 'Qr Ready to Scan', 'type': 'msg'})
        with open("./qr.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode('utf-8')
        emit('response_connect_whatsapp', {'data': encoded_string, 'type': 'qr'})
        socketio.sleep(5)


@socketio.on('send_message')
def send_message(data):
    global count_failed_msg, count_success_msg
    send_message = whatsapp.send_message(data['to'], data['message'])
    if send_message:
        emit('response_send_message', {'data': 'Message Sent', 'type': 'msg'})
        count_success_msg += 1
        log_all_messages(
            message=data['message'],
            to=data['to'],
            status=1
        )
    else:
        emit('response_send_message', {'data': 'Message Failed', 'type': 'msg'})
        count_failed_msg += 1
        log_all_messages(
            message=data['message'],
            to=data['to'],
            status=0
        )


@socketio.on('counter_message')
def counter_message():
    if whatsapp.check_whatsapp_logedin():
        emit('response_counter_message', {'data': {
            'success': count_success_msg,
            'failed': count_failed_msg,
        }, 'type': 'msg'})
    else:
        emit('response_counter_message', {'data': {
            'success': 0,
            'failed': 0,
        }, 'type': 'msg'})


@socketio.on('disconnect')
def test_disconnect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Client disconnected')


if __name__ == '__main__':
    try:
        print(Fore.GREEN + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Starting Server 🚀')
        webbrowser.open('http://localhost:5000/')
        socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Server Stopped 🛑')
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Exiting Program 🚀')
        time.sleep(1)
        sys.exit()
