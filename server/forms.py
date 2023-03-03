from flask_wtf import FlaskForm
from server.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    
    email = StringField('Email',
                        validators=[DataRequired(), Email() , ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])


    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None :
            raise ValidationError('Email is already registred')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is None :
            raise ValidationError('Email is not registred yet')
    
    def validate_password(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None :
            comp = bcrypt.check_password_hash(user.password, password.data)
            if comp == False :
                raise ValidationError('Password doesn\'t match')