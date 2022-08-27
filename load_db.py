from app import db
from app.models import User


def hybrid():
    users = User.query.all()
    for user in users:
        user.level = "QUOTA"
        db.session.add(user)
        db.session.commit()


hybrid()

with open('users.txt', 'w') as f:
    f.writelines(["{}, {}".format(user, user.level) for user in users])
    f.close()

for count, user in enumerate(u):
...     print("{}, {}, {}, {} ".format(count, user.first_name, user.cash_balance, user.btc_balance))
...
