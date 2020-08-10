import argparse
import sys
import traceback

from podcaster.db import PodcastDatabase
from podcaster.ui_curses import GUI
from podcaster.podcast import Podcast


def main():
    parser = argparse.ArgumentParser(description="CLI Podcast Player")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    try:
        db = PodcastDatabase()
        podcasts = db.fetch_all_podcasts()
        GUI(podcasts)
    except Exception as ex:
        if args.debug:
            raise
        else:
            print(ex)


if __name__ == '__main__':
    main()
