#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import time

from epapermpd.mpd_displayer import MpdDisplayer

logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    hostname = os.getenv("MPDHOST", default = "localhost")
    displayer = MpdDisplayer(hostname)
    displayer.show_song()
