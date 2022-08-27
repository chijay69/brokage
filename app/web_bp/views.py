from datetime import datetime

from . import web_bp
from .. import db
from .. import scheduler
from ..models import User
from ..tasks import task2


def percent(no, percentage):
    no = float(no)
    percentage = float(percentage)
    return no * (percentage / 100)


def Quota(user):
    user.btc_balance = percent(user.btc_balance, 20)
    user.cash_balance = percent(user.cash_balance, 20)


def Hybrid(user):
    user.btc_balance = percent(user.btc_balance, 21)
    user.cash_balance = percent(user.cash_balance, 21)


def Contract(user):
    user.btc_balance = percent(user.btc_balance, 105)
    user.cash_balance = percent(user.cash_balance, user)


def check_day(user):
    if user.description.lower() == 'quota':
        if user.counter == 1:
            Quota(user)
    elif user.description.lower() == 'hybrid':  # no divisible by 7
        if user.counter == 7:
            Hybrid(user)
    elif user.description.lower() == 'contract' == 30:
        if user.counter == 30:
            Contract(user)
    else:
        raise Exception
    return None


def check_24(user):
    c_time = datetime.now()
    if (c_time - user.last_checked).days > 1:  # checks if 24hr has passed
        user.last_checked = datetime.now()
        check_day(user)
        return True
    else:
        return False


def get_users():
    # fetch user from db
    return User.query.all()


def check_users_counter(users):
    for user in users:
        check_24(user)
        print('checked all users')
    return None


def add_counter(users):
    for user in users:
        user.counter += 1  # increases counter by 1
        # save to db
        db.session.add(user)
        db.session.commit()
    return None


@web_bp.route("/")
def index():

    return


@web_bp.route("/add")
def add():
    """Add a task.
    :url: /add/
    :returns: job
    """
    job = scheduler.add_job(
        func=task2,
        trigger="interval",
        seconds=10,
        id="test job 2",
        name="test job 2",
        replace_existing=True,
    )
    return "%s added!" % job.name
