#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from waveshare_epd import epd4in2
from .epd_controller_base import EpdControllerBase

class Epd4in2Controller(EpdControllerBase):
    def __init__(self):
        self.epd = epd4in2.EPD()
        self.epd.init()

    def display_image(self, image):
        self.epd.display(self.epd.getbuffer(image[0]))
