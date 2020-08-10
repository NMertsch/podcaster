import os
from multiprocessing.pool import ThreadPool

import podcaster.config as config
from podcaster.podcast import Podcast
from podcaster.utils import notify


class PodcastDatabase:
    def __init__(self):
        podcast_file = os.path.expanduser(config.podcast_file)
        podcast_dir, _ = os.path.split(podcast_file)
        os.makedirs(podcast_dir, exist_ok=True)

        self.podcast_file = podcast_file

    def read_podcast_urls(self):
        podcast_urls = []
        if not os.path.isfile(self.podcast_file):
            return []

        for line in open(self.podcast_file):
            line, *comments = line.split("#")
            line = line.rstrip()

            if not line:
                continue

            podcast_urls.append(line)

        return podcast_urls

    def fetch_all_podcasts(self):
        podcast_urls = self.read_podcast_urls()

        if len(podcast_urls) == 0:
            raise ValueError(f"No podcasts found in {self.podcast_file}")

        def fetch(url):
            try:
                return Podcast(url)
            except IOError:
                notify(f"Failed to read {url}")
                return None
            except AttributeError as err:
                notify(f"Failed to read podcast from {url}:", err)
                return None

        print("Fetching podcasts ...")
        pool = ThreadPool(len(podcast_urls))
        podcasts = pool.map(fetch, podcast_urls)

        return [podcast for podcast in podcasts if podcast is not None]
