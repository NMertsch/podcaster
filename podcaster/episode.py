from datetime import datetime
import os
from operator import itemgetter
from time import mktime

from feedparser import FeedParserDict
from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from podcaster.utils import suppress_stderr, play_audio


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
        play_audio(self.extract_play_url())

    def extract_play_url(self):
        # extract possible urls from rss feed
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

        # find playable urls via youtube-dl
        with suppress_stderr():
            # youtube-dl prints errors to stderr and has no way to suppress it.
            ydl = YoutubeDL(dict(quiet=True, no_warnings=True, skip_download=True))
            for url in urls:
                try:
                    info_dict = ydl.extract_info(url)
                except YoutubeDLError:
                    continue

                if 'requested_formats' in info_dict:
                    for f in info_dict['requested_formats']:
                        return f['url']
                if 'url' in info_dict:
                    return info_dict['url']
        raise RuntimeError("Failed to find a url to the audio/video file")
