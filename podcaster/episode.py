from datetime import datetime
import os
from operator import itemgetter
from time import mktime

from feedparser import FeedParserDict


class Episode:
    def __init__(self, feed_entry: FeedParserDict):
        self.rss = feed_entry
        self.date = datetime.fromtimestamp(mktime(feed_entry.published_parsed))
        self.title = feed_entry.title

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Episode({self.rss})"

    def play(self):
        urls = self.extract_possible_urls()

        for url in urls:
            url = url.split("?")[0]
            print("trying url:", url)
            ret = os.system(f"mpv --no-video {url}")
            if ret == 0:
                break
            else:
                print("... failed")

    def extract_possible_urls(self):
        urls = list()
        if "link" in self.rss.keys():
            # usually the correct url
            # does not exist for heise podcasts
            # is broken for ZEIT podcasts
            urls.append(self.rss.link)
        if "links" in self.rss.keys():
            # first link is correct for heise
            # second link is correct for ZEIT
            urls.extend(map(itemgetter("href"), self.rss.links))
        return urls
