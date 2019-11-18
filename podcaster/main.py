from datetime import datetime as dt
from typing import List, Union, Callable

import PyInquirer
import click
from PyInquirer import Separator

from podcaster.db import PodcastDatabase
from podcaster.episode import Episode
from podcaster.podcast import Podcast


def date2str(datetime: dt):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    date = datetime.date()
    days_passed = (dt.now().date() - date).days
    if days_passed == 0:
        ret = "Today"
    elif days_passed == 1:
        ret = "Yesterday"
    elif days_passed < 7:
        ret = weekdays[date.weekday()]
    else:
        ret = str(datetime.date())

    return ret.ljust(10)


def selection_menu(prompt: str, choices: List[Union[Episode, Podcast]], multiselect: bool = False, back_function: Callable = None):
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


@click.group()
def cli():
    """Command line podcast player."""
    pass


@cli.command(name="play")
def play_cmd():
    """Play podcasts."""
    db = PodcastDatabase()
    podcasts = db.get_all_podcasts(print_progress=True)
    play(podcasts)


def play(podcasts):
    if len(podcasts) == 0:
        print("No podcast available. Use 'podcaster add [URL]' first.")
        return

    podcast = None
    while podcast is None:
        podcast = selection_menu(prompt="Select podcast:", choices=podcasts)

    episode = None
    while episode is None:
        episode = selection_menu(prompt="Select episode:", choices=podcast.episodes,
                                 back_function=lambda: play(podcasts))
        if episode is None:
            continue

        episode.play()
        episode = None  # endless loop


@cli.command()
@click.argument("URLs", nargs=-1, required=True)
def add(urls):
    """
    Add URLs or podcast feeds to the podcast database.
    e.g. https://my.podcast/feed/mp3
    """
    db = PodcastDatabase()
    for url in urls:
        podcast = Podcast(url)
        db.add_podcast(url)
        print(f"Added '{podcast.title}'")


@cli.command()
def delete():
    """Delete podcasts from the database."""
    db = PodcastDatabase()
    all_podcasts = db.get_all_podcasts(print_progress=True)

    podcasts = None
    while podcasts is None:
        podcasts = selection_menu(prompt="Select podcasts to delete:", choices=all_podcasts, multiselect=True)

    for podcast in podcasts:
        db.delete_podcast(podcast)
        print(f"Deleted '{podcast.title}'")
