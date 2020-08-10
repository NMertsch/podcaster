Podcaster
=========

Podcaster is a command line podcast player. It uses `mpv <https://mpv.io/>`_ as media player.

How it works:

- read podcast RSS feeds from :code:`~/.config/podcaster.conf`
- parse them using the `feedparser <https://github.com/kurtmckee/feedparser>`_ library
- user selects podcast and episode using a `curses <https://docs.python.org/3/library/curses.html>`_ interface
- extract audio file URL via `youtube-dl <https://github.com/ytdl-org/youtube-dl>`_
- play via `python-mpv <https://github.com/jaseg/python-mpv>`_

For a more versatile and feature-complete program, check out `podcast-player <https://github.com/aziezahmed/podcast-player/>`_ or `castero <https://github.com/xgi/castero>`_.

Requirements
============

- :code:`python`, version 3.6 or later
- :code:`pip` as package manager for Python
- Python packages are automatically installed via :code:`setup.py`
- :code:`libmpv` must be available for :code:`python-mpv` to work
- :code:`notify-send` must be available for error notifications

Debian/Ubuntu:

- :code:`apt install python3 python3-pip libmpv1 libnotify-bin`

Installation
============

.. code::

    git clone [this repository]
    cd podcaster/
    pip install .

Usage
=====

Add URLs to RSS feeds of your favourite podcasts to :code:`~/.config/podcaster.conf` like this (comments and blank lines are optional):

.. code::

    # Python-specific
    https://realpython.com/podcasts/rpp/feed
    http://feeds.soundcloud.com/users/soundcloud:users:82237854/sounds.rss  # import this

    # AI
    https://lexfridman.com/category/ai/feed/

    # General
    https://feeds.simplecast.com/XA_851k3  # stack overflow podcast

Then use :code:`podcaster` from the terminal.

Details
=======

- Should work on any Linux system, tested on Ubuntu 20.04
- Might work on Windows, besides the desktop notification (`this <https://github.com/vaskovsky/notify-send>`_ might be useful)
- The podcast list file is specified in :code:`config.py`
- The curses interface is not very elaborate and quite fragile. I might fix that later. Pull requests are welcome
