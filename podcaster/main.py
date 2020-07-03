import click

from podcaster import Podcast
from podcaster.db import PodcastDatabase
from podcaster.gui import GUI


@click.group()
def cli():
    """Command line podcast player."""
    pass


@cli.command(name="play")
def play_cmd():
    """Play podcasts."""
    db = PodcastDatabase()
    podcasts = db.fetch_all_podcasts()
    GUI(podcasts)


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
        if db.add_podcast(url):
            print(f"Added '{podcast.title}'")
