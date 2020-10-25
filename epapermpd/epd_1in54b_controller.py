#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from waveshare_epd import epd1in54b
from .epd_controller_base import EpdControllerBase

class Epd1in54bController(EpdControllerBase):
    def __init__(self):
        self.epd = epd1in54b.EPD()
        self.epd.init()

    def display_image(self, image):
        self.epd.display(self.epd.getbuffer(image[0]),self.epd.getbuffer(image[1]))
