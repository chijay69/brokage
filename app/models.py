import hashlib
from time import time

import jwt
from flask import current_app, request
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.BigInteger)
    country = db.Column(db.String(64))
    btc_balance = db.Column(db.Float, default=None)
    cash_balance = db.Column(db.Float, default=None)
    level = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(64))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    counter = db.Column(db.Integer)
    last_checked = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    referee = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    referred = db.relationship('User', remote_side=id, backref='sub_users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.btc_balance is None:
            self.btc_balance = 0.0
        if self.cash_balance is None:
            self.cash_balance = 0.0
        if self.counter is None:
            self.counter = 0
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
        if self.created_date is None:
            self.created_date = datetime.now(timezone.utc)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def get_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def is_administrator(self):
        return current_user.email == 'chijay59@gmail.com'

    def __repr__(self):
        return '<User %r>' % self.first_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
