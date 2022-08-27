"""Example of adding tasks on app startup."""
from datetime import datetime, timezone

from . import db
from . import scheduler
from .models import User


def counter_to_db(u):
    try:
        u.counter = 0
        db.session.add(u)
        print('saved counter to 0')
    except:
        print('can not assign to counter')
    return None


def reset_every_user_counter():
    users = get_users()
    [counter_to_db(u) for u in users]
    db.session.commit()
    print('committed to db')
    return None


def reset_counter(user_email):
    user = User.query.filter_by(email=user_email).first_or_404()
    user.counter = 0
    db.session.add(user)
    db.session.commit()
    print('{} counter resets'.format(user.first_name))
    return None


def percent(value, percentage):
    return round((value * (percentage / 100)), 4)


def Quota(user):
    user.btc_balance += percent(user.btc_balance, 20)
    user.cash_balance += percent(user.cash_balance, 20)
    db.session.add(user)
    db.session.commit()
    return None


def Hybrid(user):
    user.btc_balance += percent(user.btc_balance, 0.007)
    user.cash_balance += percent(user.cash_balance, 0.007)
    db.session.add(user)
    db.session.commit()
    return None


def Contract(user):
    user.btc_balance += percent(user.btc_balance, 0.035)
    user.cash_balance += percent(user.cash_balance, 0.035)
    db.session.add(user)
    db.session.commit()
    return None


def check_day(user):
    if user.level == 'QUOTA':
        if user.counter == 1:
            reset_counter(user.email)

    if user.level == 'HYBRID':
        if user.counter == 7:
            reset_counter(user.email)

    if user.level == 'CONTRACT':
        if user.counter == 30:
            reset_counter(user.email)
    return None


def check_24(user):
    now = datetime.now(timezone.utc)
    current_time = user.last_checked
    if (now - current_time).days > 1:  # checks if 24hr has passed
        user.last_checked = datetime.now(timezone.utc)
        print('24 hrs has passed therefore adding percentages, check day commences')
        Quota(user)
        Hybrid(user)
        Contract(user)
        check_day(user)
    return None


def get_users():
    # fetch user from db
    u = User.query.all()
    print('Some Users\n', u[0:4])
    return u


def check_users_counter(users):
    for user in users:
        check_24(user)
        print('checked all users')
    return None


def add_counter(users):
    for user in users:
        # if user.counter is None:
        #    user.counter = 0
        # if user.last_checked is None:
        #    user.last_checked = datetime.now(timezone.utc)
        user.counter = user.counter + 1
        # user.counter = 0
        # user.last_checked = datetime.now(timezone.utc)
        print(user.counter)  # increases counter by 1
        # save to db
        db.session.add(user)
        db.session.commit()
    return None


# 86400 secs = 1day
@scheduler.task(
    "interval",
    id="job_sync",
    seconds=86400,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def task1():
    """Sample task 1.
    Added when app starts.
    """

    print("running task 1!")  # noqa: T001
    # oh, do you need something from config?
    with scheduler.app.app_context():
        users = get_users()
        add_counter(users)
        print('Every users gets a counter')
        check_users_counter(users)
        print('Checked all, done!')


def task2():
    """Sample task 2.
    Added when /add url is visited.
    """
    print("running task 2!")  # noqa: T001
