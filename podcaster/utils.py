import os
from contextlib import contextmanager, redirect_stderr
from datetime import datetime as dt
from typing import Any


def notify(title: Any, message: Any = ""):
    os.system(f"notify-send '{title}' '{message}' >/dev/null")


@contextmanager
def suppress_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    # 2020-07-01 https://stackoverflow.com/a/52442331/9568847
    with open(os.devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err:
            yield err


def date2str(timestamp: dt):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    date = timestamp.date()
    days_passed = (dt.now().date() - date).days
    if days_passed == 0:
        ret = "Today"
    elif days_passed == 1:
        ret = "Yesterday"
    elif days_passed < 7:
        ret = weekdays[date.weekday()]
    else:
        ret = str(timestamp.date())

    return ret.ljust(10)


def time2str(seconds: float):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"
