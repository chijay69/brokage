import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(32)


class Config(object):
    MAIL_SUBJECT_PREFIX = 'TokenVault'
    MAIL_SENDER = 'tokenvaultonline@gmail.com'
    SECRET_KEY = SECRET_KEY
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'tokenvaultonline@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'hiekurqnsqxhwfmn')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'chijay59@gmail.com')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static\pictures')
    UPLOADED_FILES_DEST = os.environ.get('UPLOADED_FILES_DEST', 'static\pictures')
    UPLOADED_FILES_URL = os.environ.get('UPLOADED_FILES_URL')
    UPLOADS_DEFAULT_URL = os.environ.get('UPLOADS_DEFAULT_URL')
    SCHEDULER_API_ENABLED: True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'postgresql://ozvuoscajvqlzf:6a377b9edeaa2e27b5a88144ec7ecd7380f35a97d70cf63d5f4d0a052b22d19e@ec2-44-199-26-122.compute-1.amazonaws.com:5432/dej78ntj7fvjmi'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://ozvuoscajvqlzf:6a377b9edeaa2e27b5a88144ec7ecd7380f35a97d70cf63d5f4d0a052b22d19e@ec2-44-199-26-122.compute-1.amazonaws.com:5432/dej78ntj7fvjmi'


config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig(),
    'default': DevelopmentConfig()
}
