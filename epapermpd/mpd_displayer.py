#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import sys
import logging
import time
import threading

from .mpd_controller import MpdController
from .epd_controller import EpdController
from .album_drawer import AlbumDrawer

class MpdDisplayer():
    def __init__(self, settings):
        self.epd = EpdController(settings["type"])
        self.drawer = AlbumDrawer(settings)
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
                    current_file = title
                self.mpd.wait_for_track_change()
            except (KeyboardInterrupt, SystemExit) as e:
                logging.debug("Keyboard interrupted in loop")
                sys.exit(e)
            except Exception as e:
                logging.error("Error in displaying current song: {}".format(e))

    def display_info(self):
        info = {}
        self.sem.acquire()

        while True and self.alive:
            with self.mutex:
                info = self.info.copy()
            try:
                image = self.drawer.create_album_image(info)
                self.epd.display(image)
            except Exception as e:
                logging.error("Error in displaying info: {}".format(e))

            self.sem.acquire()
    def run(self):
        self.alive = True
        self.mutex = threading.Lock()
        self.sem = threading.BoundedSemaphore(1)

        try:
            mpd_thread = threading.Thread(target=self.get_info).start()
            epd_thread = threading.Thread(target=self.display_info).start()
            signal.pause()

        except (KeyboardInterrupt, SystemExit) as e:
            logging.error("Keyboard interrupted")

            self.alive = False
            try: self.sem.release()
            except Exception as e: logging.debug("RUN: Semaphore not released: {}".format(e))
            sys.exit(e)
        except Exception as e:
            logging.error("Other exception: {}".format(e))
