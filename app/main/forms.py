from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField, DateField
from wtforms.validators import Email, DataRequired, Length, ValidationError, Regexp, EqualTo
from .read import get_country_dict

from app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone = IntegerField('Phone number', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    @staticmethod
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class LoginForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    First_name = StringField('First Name', validators=[Length(0, 64)])
    Last_name = StringField('Last Name', validators=[Length(0, 64)])
    Email = StringField('Email', validators=[Length(1, 64)])
    Subject = StringField('Subject', validators=[Length(1, 64)])
    Message = TextAreaField('Messages')
    submit = SubmitField('Send Message')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    btc_balance = FloatField('BTC BALANCE')
    cash_balance = FloatField('CASH BALANCE')
    level = SelectField('Level', validators=[DataRequired()],
                        choices=[('Select', 'Select Plan'), ('QUOTA', 'QUOTA'), ('HYBRID', 'HYBRID'),
                                 ('CONTRACT', 'CONTRACT')])
    submit = SubmitField('Submit')


class BankForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(1, 128)])
    bank_name = StringField('BankName', validators=[DataRequired(), Length(1, 128)])
    account_no = IntegerField('Account Number')
    submit = SubmitField('Withdraw')


class Paypal(FlaskForm):
    name = StringField('FullName', validators=[Length(1, 128)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Withdraw')


class BitCoin(FlaskForm):
    name = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    address = StringField('Address', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Withdraw')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo(fieldname=password,
                                                                                      message='make sure it is the same password')])

    @staticmethod
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('This account does not Exist')


class UpdatePricing(FlaskForm):
    starter1 = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter1_value = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter2 = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter2_value = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter3 = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter3_value = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter4 = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    starter4_value = StringField('FullName', validators=[DataRequired(), Length(1, 128)])


class InvoiceForm(FlaskForm):
    description = SelectField('Plan Type', validators=[DataRequired()],
                              choices=[('Select', 'Select Plan'), ('QUOTA', 'QUOTA'), ('HYBRID', 'HYBRID'),
                                       ('CONTRACT', 'CONTRACT')])
    amount = FloatField('Amount to invest', validators=[DataRequired()])
    submit = SubmitField('Submit')


class WithdrawalForm(FlaskForm):
    level = SelectField('Plan Type', validators=[DataRequired()],
                        choices=[('Select', 'Select Plan'), ('QUOTA', 'QUOTA'), ('HYBRID', 'HYBRID'),
                                 ('CONTRACT', 'CONTRACT')])
    btc_amount = FloatField('Bitcoin amount to invest', validators=[DataRequired()])
    cash_amount = FloatField('Equivalent Cash to invest', validators=[DataRequired()])
    btc = StringField('Wallet Address', validators=[DataRequired(), Length(1, 128), Regexp(regex='^(bc1|[13])['
                                                                                                 'a-zA-HJ-NP-Z0-9]{25,'
                                                                                                 '39}$',
                                                                                           message='must be a '
                                                                                                   'valid btc '
                                                                                                   'address, '
                                                                                                   'no '
                                                                                                   'spaces.')])
    submit = SubmitField('Submit')


class PayoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(0, 64)])
    last_name = StringField('Last Name', validators=[Length(0, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    description = SelectField('Plan Type', validators=[DataRequired()],
                              choices=[('Select', 'Select Plan'), ('QUOTA', 'QUOTA'), ('HYBRID', 'HYBRID'),
                                       ('CONTRACT', 'CONTRACT')])
    amount = FloatField('Amount to invest', validators=[DataRequired()])
    btc = StringField('Wallet Address', validators=[DataRequired(), Length(1, 128), Regexp(regex='^(bc1|[13])['
                                                                                                 'a-zA-HJ-NP-Z0-9]{25,'
                                                                                                 '39}$',
                                                                                           message='must be a '
                                                                                                   'valid btc '
                                                                                                   'address, '
                                                                                                   'no '
                                                                                                   'spaces.')])
    submit = SubmitField('Submit')


class MyPersonId(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    displayname = StringField('Display Name', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    DOB = DateField('Date Of Birth', validators=None)
    DP = BooleanField('Use full name for display', default=False)


class MyAddress(FlaskForm):
    address_one = StringField('Address Line 1', validators=[DataRequired()])
    address_two = StringField('Address Line 2', validators=None)
    state = IntegerField('State', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], choices=get_country_dict())
