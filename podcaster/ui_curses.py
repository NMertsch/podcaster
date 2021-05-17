import curses
import curses.ascii
import os
from math import isclose
from operator import attrgetter
from typing import Tuple, List

from podcaster.audioplayer import AudioPlayer
from podcaster.episode import Episode
from podcaster.podcast import Podcast
from podcaster.utils import date2str, time2str


class Keys:
    L = ord("l")
    K = ord("k")
    J = ord("j")
    H = ord("h")
    Q = ord("q")
    P = ord("p")
    M = ord("m")
    ENTER = ord("\n")
    SPACE = ord(" ")
    SQUARE_BRACKET_LEFT = ord("[")
    SQUARE_BRACKET_RIGHT = ord("]")
    LEFT = 260
    RIGHT = 261
    UP = 259
    DOWN = 258
    ESC = 27


class GUI:
    BACK = "Back"
    QUIT = "Quit"
    SEPARATOR = "---"

    def __init__(self, podcasts: Tuple[Podcast]):
        self.podcasts = sorted(podcasts, key=attrgetter("date"))[::-1]
        os.environ['ESCDELAY'] = '0'  # disable delayed registration of the Escape key by curses
        curses.wrapper(self.run)

    def run(self, screen):
        curses.curs_set(0)
        curses.noecho()
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()
        os.environ.setdefault('ESCDELAY', '25')
        self.select_podcast()

    def draw_title(self, title: str):
        self.screen.addnstr(0, 0, title, self.width, curses.A_BOLD)
        self.screen.noutrefresh()

    def select_podcast(self):

        podcast_strings = [f"{date2str(podcast.date)} - {podcast.title}" for podcast in self.podcasts]
        selection_entries = podcast_strings + [self.SEPARATOR, self.QUIT]
        podcast_selector = SelectionPad((1, 0), (self.height, self.width), selection_entries)

        while True:
            self.screen.clear()
            self.screen.refresh()
            self.draw_title("Select podcast:")
            selected_index = podcast_selector.run()

            selected_entry = selection_entries[selected_index]
            if selected_entry == self.QUIT:
                return
            selected_podcast = self.podcasts[selected_index]

            ret = self.select_episodes(selected_podcast)
            if ret == self.BACK:
                continue
            if ret == self.QUIT:
                return

    def select_episodes(self, podcast: Podcast):
        episode_strings = [f"{date2str(episode.date)} - {episode.title}" for episode in podcast.episodes]
        selection_entries = episode_strings + [self.SEPARATOR, self.BACK, self.QUIT]
        episode_selector = SelectionPad((1, 0), (self.height, self.width), selection_entries)

        while True:
            self.screen.clear()
            self.screen.refresh()
            self.draw_title("Select episode:")
            selected_index = episode_selector.run()

            selected_entry = selection_entries[selected_index]
            if selected_entry == self.BACK:
                return self.BACK
            if selected_entry == self.QUIT:
                return self.QUIT
            episode = podcast.episodes[selected_index]

            self.play(podcast, episode)

    def play(self, podcast: Podcast, episode: Episode):
        self.screen.clear()
        self.draw_title(f"{podcast.title}")
        player = EpisodePlayWindow((1, 0), (self.height, self.width), episode)
        player.run()


class SelectionPad:
    def __init__(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], entry_list: List[str]):
        self.entries = entry_list
        self.width = bottom_right[1] - top_left[1]
        self.win_height = bottom_right[0] - top_left[0]
        self.top_left = top_left
        self.bottom_right = bottom_right

        self.has_back_option = GUI.BACK in entry_list

        self.pad = curses.newpad(len(entry_list), self.width)
        self.pad.keypad(True)
        self.current_index = 0
        self.item_offset = 0

    def run(self):
        self.draw()
        while True:
            c = self.pad.getch()
            if c in (curses.KEY_DOWN, ord('j')):
                if self.current_index == len(self.entries) - 1:
                    self.current_index = 0
                elif self.entries[self.current_index + 1] == GUI.SEPARATOR:
                    self.current_index += 2
                else:
                    self.current_index += 1
            elif c in (Keys.K, Keys.UP):
                if self.current_index == 0:
                    self.current_index = len(self.entries) - 1
                elif self.entries[self.current_index - 1] == GUI.SEPARATOR:
                    self.current_index -= 2
                else:
                    self.current_index -= 1
            elif self.has_back_option and c in (Keys.ESC, Keys.H, Keys.LEFT):
                return self.entries.index(GUI.BACK)
            elif c in (Keys.Q, Keys.ESC):
                return self.entries.index(GUI.QUIT)
            elif c in (Keys.ENTER, Keys.L, Keys.RIGHT):
                return self.current_index
            self.draw()

    def draw(self):
        self.pad.erase()

        if self.current_index >= self.win_height + self.item_offset:
            # scroll down
            self.item_offset = self.current_index - self.win_height + 1
        elif self.current_index == self.item_offset - 1:
            # scroll up
            self.item_offset -= 1
        elif self.item_offset == 0 and self.current_index == len(self.entries) - 1:
            # scroll past top
            self.item_offset = len(self.entries) - 1 - self.win_height
        elif self.current_index == 0 and self.item_offset > 0:
            self.item_offset = 0

        for i, entry in enumerate(self.entries):
            mode = curses.A_REVERSE if i == self.current_index else curses.A_NORMAL
            self.pad.addnstr(i, 0, entry, self.width, mode)

        # noinspection PyArgumentList
        self.pad.noutrefresh(self.item_offset, 0, *self.top_left, self.win_height, self.width-1)
        curses.doupdate()


class EpisodePlayWindow:
    def __init__(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], episode: Episode):
        self.episode = episode
        self.player = AudioPlayer()

        self.width = bottom_right[1] - top_left[1]
        self.win_height = bottom_right[0] - top_left[0]
        self.window = curses.newwin(self.win_height, self.width, *top_left)
        self.window.keypad(True)

    def run(self):
        self.draw()

        self.player.play(self.episode.url)

        curses.halfdelay(3)
        while True:
            c = self.window.getch()
            if c in (Keys.P, Keys.SPACE):
                self.player.pause_toggle()
            elif c in (Keys.Q, Keys.ESC):
                self.player.quit()
                return
            elif c in (Keys.LEFT, Keys.H):
                self.player.backward()
            elif c in (Keys.RIGHT, Keys.L):
                self.player.forward()
            elif c in (Keys.UP, Keys.K):
                self.player.volume_up()
            elif c in (Keys.DOWN, Keys.J):
                self.player.volume_down()
            elif c in (Keys.SQUARE_BRACKET_LEFT,):
                self.player.speed_down()
            elif c in (Keys.SQUARE_BRACKET_RIGHT,):
                self.player.speed_up()
            elif c in (Keys.M,):
                self.player.mute_toggle()

            self.draw()

    def draw_header(self):
        self.window.addnstr(0, 0, self.episode.title, self.width, curses.A_BOLD)

    def draw(self):
        self.window.erase()
        self.draw_header()

        if self.player.time is None:
            progress_str = "Loading..."
        else:
            progress_str = f"{time2str(self.player.time)} / {time2str(self.player.duration)}"

        if self.player.is_paused:
            progress_str += " (paused)"

        if isclose(self.player.speed, 1) or self.player.duration is None:
            speed_str = ""
        else:
            time_left = (self.player.duration - self.player.time) / self.player.speed
            speed_str = f"Speed: {self.player.speed:.2f}x ({time2str(time_left)} left)"

        if isclose(self.player.volume, 100):
            volume_str = "(muted)" if self.player.is_muted else ""
        else:
            volume_str = f"Volume: {int(self.player.volume)} %"
            if self.player.is_muted:
                volume_str += " (muted)"

        status_string = ", ".join([s for s in [volume_str, speed_str] if s])

        self.window.addnstr(2, 0, progress_str, self.width)
        self.window.addnstr(3, 0, status_string, self.width)
        self.window.noutrefresh()
        curses.doupdate()
