from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from  wtforms.validators import InputRequired, Email,EqualTo
from ..models import User
from wtforms import ValidationError 
from wtforms import BooleanField

class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[InputRequired(),Email()])
    username = StringField('Enter your username',validators = [InputRequired()])
    password = PasswordField('Password',validators = [InputRequired(), EqualTo('password_confirm',message = 'Passwords are not matching')])
    password_confirm = PasswordField('Confirm Passwords',validators = [InputRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email. try another one')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username already  taken')
        
class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators =[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')