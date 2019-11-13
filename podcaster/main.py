"""
delete: podcast-menu -> delete Podcast object
- / play: podcast-menu, ordered by date + Quit -> episode-menu, ordered by date + Back + Quit -> play Episode object -> episode menu
"""
from datetime import datetime as dt
from typing import List, Union

import PyInquirer
import click

from podcaster.db import PodcastDatabase
from podcaster.episode import Episode
from podcaster.podcast import Podcast


def selection_menu(prompt: str, choices: List[Union[Episode, Podcast]], multiselect: bool = False):
    choices_sorted = sorted(choices, key=lambda item: dt.now() - item.date)
    choices_dict = [dict(name=item.title, value=item) for item in choices_sorted]

    menu_name = "menu"
    answer = PyInquirer.prompt([dict(
        type="checkbox" if multiselect else "list",
        name=menu_name,
        message=prompt,
        choices=choices_dict,
    )])[menu_name]

    return answer


@click.group()
def cli():
    pass


@cli.command()
def play():
    db = PodcastDatabase()
    podcasts = db.get_all_podcasts()
    if len(podcasts) == 0:
        print("No podcast available. Use 'podcaster add URLs' first.")
        return

    podcast = selection_menu(prompt="Select podcast:", choices=podcasts)
    episode = selection_menu(prompt="Select episode:", choices=podcast.episodes)
    episode.play()


@cli.command()
@click.argument("URLs", nargs=-1, required=True)
def add(urls):
    """URLs of podcast feeds. Example: podcast-url/feed/mp3"""
    db = PodcastDatabase()
    for url in urls:
        podcast = Podcast(url)
        db.add_podcast(url)
        print(f"Added '{podcast.title}'")


@cli.command()
def delete():
    db = PodcastDatabase()
    podcasts = selection_menu(prompt="Select podcasts to delete:", choices=db.get_all_podcasts(), multiselect=True)
    for podcast in podcasts:
        db.delete_podcast(podcast)
        print(f"Deleted '{podcast.title}'")
