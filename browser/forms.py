from flask_wtf import Form
from wtforms import StringField, PasswordField


class ConnectionForm(Form):
	server_name = StringField('Server Name')
	user_name = StringField('User Name')
	password = PasswordField('Enter Password')