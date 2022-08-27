from itsdangerous.url_safe import URLSafeSerializer
from flask import current_app


def generate_referral_code():
    s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt="activate")
    return s
