#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import threading

from .mpd_controller import MpdController
from .epd_controller import EpdController
from .album_drawer import AlbumDrawer

DISPLAY_TYPES = {
    "1in54b": {
        "color": 2,
        "width": 200,
        "height": 200
    },
    "4in2": {
        "color": 1,
        "width": 300,
        "height": 400
    }   
}

class MpdDisplayer():
    def __init__(self, settings):
        if settings["type"] not in DISPLAY_TYPES:
            raise Exception("Display not supported")
        self.epd = EpdController(settings["type"])
        self.drawer = AlbumDrawer(DISPLAY_TYPES[settings["type"]])
        self.mpd = MpdController(settings["host"])
        self.info = {}

    def get_info(self):
        current_file = ""
        while True:
            try:
                self.mpd.wait_until_playing()
                info = self.mpd.get_info()
                title = info["title"] if info["title"] else info["file"]
                if title != current_file:
                    with self.mutex:
                        self.info = info
                    try:
                        self.sem.release()
                    except Exception as e:
                        logging.debug("Semaphore not released: {}".format(e))
                    current_file = info["title"]
                    self.mpd.wait_for_track_change()
            except Exception as e:
                logging.error("Error in displaying current song: {}".format(e))
            time.sleep(1)

    def display_info(self):
        info = {}
        while True:
            self.sem.acquire()
            with self.mutex:
                info = dict(self.info)
            try: self.display_album_info(info)
            except: pass

    def display_album_info(self, info):
        image = self.drawer.create_album_image(info)
        self.epd.display(image)

    def run(self):
        self.mutex = threading.Lock()
        self.sem = threading.BoundedSemaphore(1)
        mpd_thread = threading.Thread(target=self.get_info).start()
        epd_thread = threading.Thread(target=self.display_info).start()
