#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import time
from PIL import Image,ImageDraw,ImageFont

from waveshare_epd import epd4in2

logging.basicConfig(level=logging.DEBUG)

font24 = ImageFont.truetype(os.path.join("waveshare_epd", 'Font.ttc'), 24)

class AlbumDrawer():
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        logging.info("Drawing to {}x{}px".format(size[0],size[1]))

    def get_image(self):
        Himage = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), 'hello world', font = font24, fill = 0)
        draw.text((10, 20), '4.2inch e-Paper', font = font24, fill = 0)
        draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
        draw.line((20, 50, 70, 100), fill = 0)
        draw.line((70, 50, 20, 100), fill = 0)
        draw.rectangle((20, 50, 70, 100), outline = 0)
        draw.line((165, 50, 165, 100), fill = 0)
        draw.line((140, 75, 190, 75), fill = 0)
        draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
        draw.rectangle((80, 50, 130, 100), fill = 0)
        draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
        return Himage

class Epd4in2Controller():
    def __init__(self):
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

if __name__ == "__main__":
    epd = Epd4in2Controller()
    drawer = AlbumDrawer(epd.get_size())
    epd.display(drawer.get_image())
    time.sleep(2)

