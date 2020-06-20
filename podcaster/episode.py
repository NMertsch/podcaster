from datetime import datetime
import os
from time import mktime

from feedparser import FeedParserDict


class Episode:
    def __init__(self, feed_entry: FeedParserDict):
        self.rss = feed_entry
        self.date = datetime.fromtimestamp(mktime(feed_entry.published_parsed))
        self.title = feed_entry.title
        try:
            self.url = feed_entry.link
        except AttributeError:
            self.url = feed_entry.links[0]["href"]

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Episode({self.rss})"

    def play(self):
        os.system(f"mpv --no-video {self.url}")
