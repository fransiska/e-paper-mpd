#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from waveshare_epd import epd4in2

class EpdController():
    def __init__(self, size="4in2"):
        if size == "4in2":
            self.epd = epd4in2.EPD()
        self.epd.init()

    def clear(self):
        logging.info("Clearing")
        self.epd.Clear()

    def display(self, image):
        try:
            logging.info("Drawing")
            self.clear()
            self.epd.display(self.epd.getbuffer(image))
        except Exception as e:
            logging.info("Error: {}".format(e))

    def get_size(self):
        return self.epd.width, self.epd.height

