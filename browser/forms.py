from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, SubmitField


class ServerCredentialForm(Form):
	server = StringField('Server',  validators=[validators.Required("Please Enter Server")])
	servername = StringField('Server Name',  validators=[validators.Required("Please Enter Server Address.")])
	username = StringField('User Name',  validators=[validators.Required("Please Enter User Name.")])
	password = PasswordField('Enter Password',  validators=[validators.Required("Please Enter User Name.")])
	submit = SubmitField("Login")