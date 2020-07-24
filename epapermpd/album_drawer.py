#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PIL import Image,ImageDraw,ImageFont
import logging

logging.basicConfig(level=logging.DEBUG)

font24 = ImageFont.truetype(os.path.join("waveshare_epd", 'Font.ttc'), 24)

class AlbumDrawer():
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        logging.info("Drawing to {}x{}px".format(size[0],size[1]))

    def create_album_image(self, title):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(img)
        draw.text((10, 0), title, font=font24, fill=0)
        return img

    def create_mono_image(self, path):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        image_file = Image.open(path) # open colour image
        if image_file.size[0] > self.width or image_file.size[1] > self.height:
            image_file.thumbnail((self.width,self.height), Image.ANTIALIAS)
        image_file = image_file.convert('1') # convert image to black and white
        img.paste(image_file, (0,0))
        return img

