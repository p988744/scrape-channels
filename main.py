from datetime import datetime, timedelta

import pytz as pytz

from celery_apps import celeryconfig
from celery_apps.tasks import add

if __name__ == '__main__':
    my_tz = pytz.timezone(celeryconfig.timezone)
    now_tw = datetime.now(tz=my_tz)
    now = datetime.now()
    print(now_tw, now)
    eta = now_tw + timedelta(seconds=10)

    print(eta)
    # eta = None
    result = add.apply_async(kwargs={'x': 4, 'y': 4}, eta=eta)
    print(result.ready)
    print(result.get(timeout=20))
