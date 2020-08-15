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
        "type": "4in2",
        "size": {
            "width": 300,
            "height": 400
        }
    }
    displayer = MpdDisplayer(settings)
    displayer.show_song()
