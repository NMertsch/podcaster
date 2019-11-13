from datetime import datetime
from time import mktime

import feedparser

from podcaster.episode import Episode


class Podcast:
    def __init__(self, url):
        self.url = url
        self.rss = feedparser.parse(url)
        self.feed = self.rss.feed

        if not self.feed:
            raise IOError(f"No podcast feed found at '{self.url}'.")

        self.link = self.feed.link
        self.title = self.feed.title
        self.date = datetime.fromtimestamp(mktime(self.feed.updated_parsed))
        self.author = self.feed.author
        self._episodes = None

    @property
    def episodes(self):
        if self._episodes is None:
            # read episodes lazily as generating episode lists on podcast initialization would be slow
            self._episodes = tuple(Episode(entry) for entry in self.rss.entries)
        return self._episodes

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Podcast({self.url})"
