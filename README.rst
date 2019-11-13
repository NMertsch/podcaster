Podcaster
=========

Podcaster is a command line podcast player. It uses `mpv <https://mpv.io/>`_ as media player and stores podcast feeds in a SQLite database.

The general approach is adapted from `podcast-player <https://github.com/aziezahmed/podcast-player/>`. Please check it out!

Development Status
==================

The state of this project is well described by "kinda works for me". Contributions are always welcome.

- No Windows support
- No configuration
- No documentation
- No error handling
- No tests
- No convenience-functions like playing multiple episodes

Installation
============

.. code::

    git clone [this repository]
    cd podcaster
    pip install .

Usage
=====

.. code::

    podcaster add URL  # saves podcast(s) to database
    podcaster play     # opens menu to select podcast and episode
    podcaster delete   # opens menu to select podcast(s) to remove from database

Dependencies
============

These are automatically installed when using `pip` to install podcaster:

- `click <https://github.com/pallets/click>`_ - Python composable command line interface toolkit
- `feedparser <https://github.com/kurtmckee/feedparser>`_ - Parse Atom and RSS feeds in Python
- `sqlalchemy <https://github.com/sqlalchemy/sqlalchemy>`_ - The Database Toolkit for Python
- `PyInquirer <https://github.com/CITGuru/PyInquirer>`_ - A Python module for common interactive command line user interfaces

This needs to be installed separately using your system's package manager:

- `mpv <https://mpv.io>`_ - a free, open source, and cross-platform media player
