import click

from podcaster.db import PodcastDatabase
from podcaster.podcast import Podcast
from podcaster.utils import selection_menu


@click.group()
def cli():
    """Command line podcast player."""
    pass


@cli.command(name="play")
def play_cmd():
    """Play podcasts."""
    db = PodcastDatabase()
    podcasts = db.fetch_all_podcasts(print_progress=True)
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
    all_podcasts = db.fetch_all_podcasts(print_progress=True)

    podcasts = None
    while podcasts is None:
        podcasts = selection_menu(prompt="Select podcasts to delete:", choices=all_podcasts, multiselect=True)

    for podcast in podcasts:
        db.delete_podcast(podcast)
        print(f"Deleted '{podcast.title}'")
