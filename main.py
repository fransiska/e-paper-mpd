#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import time

from epapermpd.mpd_displayer import MpdDisplayer

logging.basicConfig(level=logging.ERROR)

if __name__ == "__main__":
    settings = {
        "host": os.getenv("MPDHOST", default = "localhost"),
        "type": "1in54b"
    }
    displayer = MpdDisplayer(settings)
    displayer.run()
