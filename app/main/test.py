from datetime import datetime, timezone

print(datetime.utcnow())
now = datetime.utcnow()
last = datetime.strptime('2021 11 13 12 19 00 007480', '%Y %m %d %H %M %S %f')
if (now - last).days > 1:
    print('24 hours passed')
else:
    print('Under 24 hrs')
