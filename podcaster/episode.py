from datetime import datetime
import os
from time import mktime


class Episode:
    def __init__(self, feed_entry):
        self.rss = feed_entry
        self.url = feed_entry.link
        self.title = feed_entry.title
        self.subtitle = feed_entry.subtitle
        self.summary = feed_entry.summary
        self.date = datetime.fromtimestamp(mktime(feed_entry.published_parsed))

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Episode({self.url})"

    def play(self):
        os.system(f"mpv --no-video {self.url}")
