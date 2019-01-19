from flaskauth import mail
from flask_mail import Message
from threading import Thread
from flaskauth import app

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)


def threaded_email_send(msg):
    th = Thread(target=send_email, args=(app, msg)).start()



