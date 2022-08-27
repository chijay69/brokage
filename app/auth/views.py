from datetime import timezone, datetime

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, PasswordForm
from .. import db
from ..emails import send_async
from ..models import User


@auth.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data,
                    password=form.password.data, level=form.level.data,
                    phone=form.phone.data, country=form.country.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')

        send_async('Tokenvaultonline@gmail', 'User Registered', 'auth/email/admin_email_register.html',
                   user={'fname': form.firstname.data, 'email': form.email.data, 'date': datetime.now(timezone.utc)})

        send_async(form.email.data, 'User Registeration Successful', 'auth/email/confirm.html',
                   user={'fname': form.firstname.data})

        # send_async(to=['Tokenvaultonline@gmail'], subject='User Registeration Complete',
        #            template='auth/email/admin_email_confirm.html',
        #            user={'fname': form.firstname.data, 'email': form.email.data, 'date': datetime.now(timezone.utc)})
        # send_async(to=[form.email.data], subject='User Registeration Complete',
        #                    template='auth/email/email_confirm.html',
        #                    user={'fname': form.firstname.data})

        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.user', name=current_user.first_name)
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_async(current_user.email, 'Confirm Your Account', 'auth/email/confirm.html', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_async(user.email, 'Password reset requested', 'auth/email/recover.html', token=token)
            flash('An email has been set on how to reset your password')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset.html', form=form)


@auth.route('/reset_password_token/<token>', methods=["GET", "POST"])
def reset_password_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Expired or invalid token', 'warning')
        return redirect(url_for('auth.reset'))
    form = PasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        password_hash = generate_password_hash(password)
        user.password_hash = password_hash
        flash('just added password')
        db.session.add(user)
        db.session.commit()
        flash('Password Reset Complete, login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_with_token.html', form=form, token=token)
