#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import time

from epapermpd.mpd_displayer import MpdDisplayer

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    hostname = os.getenv("MPDHOST", default = "localhost")
    displayer = MpdDisplayer(hostname)
    displayer.print_info()
    exit()
    displayer.display_image("/home/pi/gone.jpg")
    displayer.show_song()
