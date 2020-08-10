import mpv


class AudioPlayer:
    def __init__(self):
        self.mpv = mpv.MPV(video=False, ytdl=True)

    def play(self, url):
        # MPV can be in paused-state without playing anything. `play` would then start and immediately pause.
        if self.is_paused:
            self.pause_toggle()
        self.mpv.play(url)

    def pause_toggle(self):
        self.mpv.cycle("pause")

    def mute_toggle(self):
        self.mpv.cycle("mute")

    def stop(self):
        self.mpv.command("stop")

    def quit(self):
        self.mpv.terminate()
        del self.mpv

    def speed_up(self):
        self.mpv.command("add", "speed", 0.1)

    def speed_down(self):
        self.mpv.command("add", "speed", -0.1)

    def speed_reset(self):
        self.mpv.command("set", "speed", 1)

    def seek(self, seconds):
        self.mpv.command('seek', seconds)

    def forward(self, seconds=10):
        self.seek(seconds)

    def backward(self, seconds=10):
        self.mpv.seek(-1 * seconds)

    def _change_volume(self, percent):
        new_volume = self.mpv.volume + percent
        if new_volume > self.mpv.volume_max:
            new_volume = self.mpv.volume_max
        elif new_volume < 0:
            new_volume = 0
        self.mpv["volume"] = new_volume

    def volume_up(self, percent=10):
        self._change_volume(percent)

    def volume_down(self, percent=10):
        self._change_volume(-1 * percent)

    @property
    def time(self):
        return self.mpv.time_pos

    @property
    def volume(self):
        return self.mpv.volume

    @property
    def duration(self):
        return self.mpv.duration

    @property
    def is_paused(self):
        return self.mpv.pause

    @property
    def is_muted(self):
        return self.mpv.mute

    @property
    def speed(self):
        return self.mpv.speed

    def __del__(self):
        try:
            self.quit()
        except:
            pass
