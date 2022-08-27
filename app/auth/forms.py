from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, SelectField
from wtforms.validators import Email, DataRequired, Length, ValidationError, EqualTo
from wtforms.widgets import HiddenInput
from app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    level = SelectField('Plan', validators=[DataRequired()], choices=[('PLANS', 'PLANS'), ('QUOTA', 'QUOTA'), ('HYBRID', 'HYBRID'), ('CONTRACT', 'CONTRACT')])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    @staticmethod
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class LoginForm(FlaskForm):
    next = StringField('next', widget=HiddenInput())
    email = StringField('Your Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Login')


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('This account does not Exist')
