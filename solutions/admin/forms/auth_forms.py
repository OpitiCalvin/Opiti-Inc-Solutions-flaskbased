from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, InputRequired, EqualTo, ValidationError

class RegisterForm(FlaskForm):
	email = EmailField(validators=[DataRequired(message="Email is required.")])
	username = StringField(validators=[DataRequired(message="Username is required.")])
	password = PasswordField(validators=[DataRequired(), EqualTo('confirm', message="Passwords must match!"), InputRequired()])
	confirm = PasswordField(validators=[DataRequired(),EqualTo('password', message='Repeat Password')])	
	# terms = BooleanField(validators=[DataRequired(message="Check the box to proceed with registration.")])
	submit = SubmitField('Register Now')

class LoginForm(FlaskForm):
	username = StringField(validators=[InputRequired("Username is required.")])
	password = PasswordField(validators=[InputRequired('Please enter password.')])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log In')