from datetime import datetime as dt

import feedparser

from podcaster.episode import Episode


class Podcast:
    def __init__(self, url):
        self.url = url
        self.rss = feedparser.parse(url)
        self.feed = self.rss.feed

        if not self.feed:
            msg = f"No podcast feed found at '{self.url}'."
            raise IOError(msg)

        self.title = self.feed.title

        if hasattr(self.feed, "author"):
            self.author = self.feed.author
        else:
            self.author = "Unknown"

        episodes = tuple(Episode(entry) for entry in self.rss.entries)
        self.episodes = sorted(episodes, key=lambda item: dt.now() - item.date)
        self.date = self.episodes[0].date

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Podcast({self.url})"
