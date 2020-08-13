#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time

from .epd_controller import EpdController
from .album_drawer import AlbumDrawer
from .mpd_controller import MpdController

class MpdDisplayer():
    def __init__(self, host):
        self.epd = EpdController()
        size = self.epd.get_size()
        self.drawer = AlbumDrawer((size[1], size[0]), 26, 22, (270,270))
        self.mpd = MpdController(host)

    def show_song(self):
        current_file = ""
        while True:
            try:
                logging.debug("Waiting until playing")
                self.mpd.wait_until_playing()
                info = self.mpd.get_info()
                title = info["title"] if info["title"] else info["file"]
                if title != current_file:
                    logging.debug("Displaying new info {}".format(info))
                    self.display_info(info)
                    current_file = info["title"]
                    if self.mpd.get_current():
                        logging.debug("Waiting for track change")
                        self.mpd.wait_for_track_change()
            except Exception as e:
                logging.error("Error in displaying current song: {}".format(e))
            time.sleep(1)

    def display_info(self, info):
        img = self.drawer.create_album_image(info)
        self.epd.display(img)

    def display_image(self, path):
        logging.info("Displaying image {}".format(path))
        self.epd.display(self.drawer.create_mono_image(path))

    def print_info(self):
        info = self.mpd.get_info()
