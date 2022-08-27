import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    native = date
    format = "%m/%d/%Y, %H:%M:%S"
    return native.strftime(format)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    app.run()
