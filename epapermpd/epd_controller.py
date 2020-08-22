#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from .epd_4in2_controller import Epd4in2Controller
from .epd_1in54b_controller import Epd1in54bController

from .album_drawer import AlbumDrawer

class EpdController():
    def __init__(self, size):
        if size == "4in2":
            self.epd = Epd4in2Controller()
        elif size == "1in54b":
            self.epd = Epd1in54bController()
        else:
            raise Exception("Display type is not supported")

    def display(self, image):
        try:
            logging.info("Drawing")
            self.epd.display(image)
        except Exception as e:
            logging.info("Error: {}".format(e))

