from contextlib import contextmanager, redirect_stderr
from datetime import datetime as dt
import os
from typing import List, Callable

import PyInquirer
from PyInquirer import Separator


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


def selection_menu(prompt: str, choices: List, multiselect: bool = False, back_function: Callable = None):
    if len(choices) == 0:
        raise ValueError("No choices given (len(choices) == 0).")
    if not hasattr(choices[0], "date"):
        raise ValueError("Choices are sorted by their 'date' attribute. Given choice has no date.")

    choices_sorted = sorted(choices, key=lambda item: dt.now() - item.date)
    choice_dicts = [dict(name=f"{date2str(item.date)} - {item.title}", value=item) for item in choices_sorted]
    choice_dicts += [Separator()]
    if back_function is not None:
        choice_dicts += [dict(name="Back")]
    choice_dicts += [dict(name="Quit")]

    menu_name = "menu"
    answer = PyInquirer.prompt([dict(
        type="checkbox" if multiselect else "list",
        name=menu_name,
        message=prompt,
        choices=choice_dicts,
    )]).get(menu_name)

    if answer == "Back":
        back_function()
    elif answer == "Quit":
        exit(0)
    else:
        return answer
