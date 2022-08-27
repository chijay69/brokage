from app import db


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
    user = User.query.filter_by(email=user_email).first()
    user.counter = 0
    db.session.add(user)
    db.session.commit()
    return None


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
    user.cash_balance = percent(user.cash_balance, 105)


def check_day(user):
    if user.level.lower() == 'quota':
        if user.counter == 1:
            print('Quota user')
            Quota(user)
            reset_counter(user.email)

    elif user.level.lower() == 'hybrid':  # no divisible by 7
        if user.counter == 7:
            print('Hybrid user')
            Hybrid(user)
            reset_counter(user.email)

    elif user.level.lower() == 'contract' == 30:
        if user.counter == 30:
            print('Contract user')
            Contract(user)
            reset_counter(user.email)

    else:
        raise Exception
    return None


def check_24(user):
    now = datetime.now(timezone.utc)
    current_time = user.last_checked
    if (now - current_time).days > 1:  # checks if 24hr has passed
        user.last_checked = datetime.now(timezone.utc)
        print('24 hrs has passed check day commences')
        check_day(user)
    return None


def get_users():
    # fetch user from db
    u = User.query.all()
    print(u[0:4])
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


for i in [a_email, b_email, c_email]:
    for j in [a_btc, b_btc, c_btc]:
        for k in [a_cash, b_cash, c_cash]:
            use = User.query.filter_by(email=i).first()
            use.btc_balance = j
            use.cash_balance = k
            db.session.add(use)
            db.session.commit()

for user in User.query.all():
...     user.btc_balance=0.0
...     user.cash_balance=0.0
...     db.session.add(user)
...     db.session.commit()
