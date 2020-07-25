#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time

from .epd_controller import EpdController
from .album_drawer import AlbumDrawer
from .mpd_controller import MpdController

logging.basicConfig(level=logging.DEBUG)

class MpdDisplayer():
    def __init__(self, host):
        self.epd = EpdController()
        self.drawer = AlbumDrawer(self.epd.get_size())
        self.mpd = MpdController(host)

    def show_song(self):
        self.wait_for_mpc()
        self.display_current_mpd()

    def wait_for_mpc(self):
        # Wait until mpc starts playing
        while not self.mpd.get_current():
            time.sleep(1)

    def display_current_mpd(self):
        info = self.mpd.get_info()
        print(info)
        self.epd.display(self.drawer.create_album_image(info))

    def display_image(self, path):
        logging.info("Displaying image {}".format(path))
        self.epd.display(self.drawer.create_mono_image(path))

    def print_info(self):
        info = self.mpd.get_info()
        print(info)
