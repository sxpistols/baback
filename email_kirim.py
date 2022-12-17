# #email


from flask import Flask
from flask_mail import Mail, Message
import os
from threading import Thread
from flask import render_template

app = Flask(__name__)

mail_settings = {
	"MAIL_SERVER": 'smtp.gmail.com',
	"MAIL_PORT": 465,
	"MAIL_USE_TLS": False,
	"MAIL_USE_SSL": True,
	# "MAIL_USERNAME": os.environ['EMAIL_USER'],
	"MAIL_USERNAME": 'adolants@gmail.com',
	# "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD'],
	"MAIL_PASSWORD": 'iycbdjfkpnppwypd',
	
	}

#ztgpjzxupdibpizw
app.config.update(mail_settings)
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# if __name__ == '__main__':
def sendM(assignmentdata,data,emailadd):
	print(len(assignmentdata),flush=True)
	print(data,flush=True)
	# print(data['email'])
	email_recipient = emailadd
	subject="Assignment_"+data['fullname']+"_"+data['dateassignment']
	with app.app_context():
	    msg = Message(subject=subject,
	                  sender=app.config.get("MAIL_USERNAME"),
	                  # recipients=["arief.dolants@solusi247.com","dany.agustiyanto@solusi247.com","rini@solusi247.com","reza.ikramullah@solusi247.com","fiki.ferdian@solusi247.com","septian.priyatna@solusi247.com"], # replace with your email for testing
	                  recipients=[email_recipient], # replace with your email for testing
	                  html=render_template("email_assignment.html", data=data, assignmentdata=assignmentdata))

	                  # html="<p>This is a test email I sent with Gmail and Python!</p>")
	    # mail.send(msg)
	    thr = Thread(target=send_async_email, args=[app, msg])
	    thr.start()


def userReg(data):
	print(data,flush=True)
	# print(data['email'])
	email_recipient = data['email']

	print(email_recipient,flush=True)
	email_recipient = 'arief.dolants@solusi247.com'
	subject="User Created - BSO Manager"
	with app.app_context():
	    msg = Message(subject=subject,
	                  sender=app.config.get("MAIL_USERNAME"),
	                  # recipients=["arief.dolants@solusi247.com","dany.agustiyanto@solusi247.com","rini@solusi247.com","reza.ikramullah@solusi247.com","fiki.ferdian@solusi247.com","septian.priyatna@solusi247.com"], # replace with your email for testing
	                  recipients=[email_recipient], # replace with your email for testing
	                  html=render_template("email_newuser.html", data=data))

	                  # html="<p>This is a test email I sent with Gmail and Python!</p>")
	    # mail.send(msg)
	    thr = Thread(target=send_async_email, args=[app, msg])
	    thr.start()

# from flask_mail import Message
# from app import mail

# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)