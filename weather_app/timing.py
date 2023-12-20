import datetime as dt
import time
import math

def current_time(zone):
    a=(int(dt.datetime.timestamp(dt.datetime.now(dt.timezone.utc))))+zone
    return (dt.datetime.utcfromtimestamp(a))

print(dt.datetime.fromtimestamp(1702967400))