import os
from multiprocessing.pool import ThreadPool
from os.path import expanduser

import sqlalchemy as db
from sqlalchemy.exc import IntegrityError

import podcaster.config as config
from podcaster.podcast import Podcast
from podcaster.utils import notify


class PodcastDatabase:
    def __init__(self):
        os.makedirs(expanduser(config.config_dir), exist_ok=True)
        self.db_file = f"sqlite:///{expanduser(config.config_dir)}/{config.database_file}"
        self.engine = db.create_engine(self.db_file)
        self.podcast_table = self.initialize_db()

    def __repr__(self):
        return f"PodcastDatabase('{self.db_file}')"

    def __str__(self):
        return self.__repr__()

    def initialize_db(self):
        metadata = db.MetaData()

        podcast_urls = db.Table("podcast_urls", metadata,
                                db.Column("id", db.Integer(), autoincrement=True, primary_key=True),
                                db.Column("url", db.String(255), nullable=False, unique=True),
                                db.Column("title", db.String(255), nullable=False)
                                )

        metadata.create_all(self.engine)

        return podcast_urls

    def add_podcast(self, url):
        podcast = Podcast(url)
        insertion = self.podcast_table.insert().values(url=url, title=podcast.title)
        with self.engine.connect() as connection:
            try:
                connection.execute(insertion)
            except IntegrityError as ex:
                print("Failed to add podcast: " + ex.args[0])
                return False
        return True

    def delete_podcast(self, podcast: Podcast):
        deletion = self.podcast_table.delete().where(self.podcast_table.c.url == podcast.url)
        connection = self.engine.connect()
        connection.execute(deletion)
        connection.close()

    def fetch_all_podcasts(self):
        selection = db.select([self.podcast_table])
        connection = self.engine.connect()
        podcast_urls = [podcast.url for podcast in connection.execute(selection)]

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
        try:
            pool = ThreadPool(len(podcast_urls))
            podcasts = pool.map(fetch, podcast_urls)
            return [podcast for podcast in podcasts if podcast is not None]
        finally:
            connection.close()
