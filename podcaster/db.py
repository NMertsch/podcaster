import shutil
from os.path import expanduser

import sqlalchemy as db

import podcaster.config as config
from podcaster.podcast import Podcast


class PodcastDatabase:
    def __init__(self):
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
        connection = self.engine.connect()
        connection.execute(insertion)
        connection.close()

    def delete_podcast(self, podcast: Podcast):
        deletion = self.podcast_table.delete().where(self.podcast_table.c.url == podcast.url)
        connection = self.engine.connect()
        connection.execute(deletion)
        connection.close()

    def get_all_podcasts(self, print_progress=False):
        selection = db.select([self.podcast_table])
        connection = self.engine.connect()
        podcasts = list()

        terminal_width = shutil.get_terminal_size(fallback=(80, 20)).columns
        for i, podcast_entry in enumerate(connection.execute(selection), start=1):
            if print_progress:
                opening = f"Fetching podcast {i}: "
                print("\033[K" + (opening + podcast_entry.title)[:terminal_width], end="\r")  # "\003[K": clear line
            podcasts.append(Podcast(podcast_entry.url))
        connection.close()

        return tuple(podcasts)
