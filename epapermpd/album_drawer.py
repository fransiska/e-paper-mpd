#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PIL import Image,ImageDraw,ImageFont
import textwrap
import logging

logging.basicConfig(level=logging.DEBUG)

font24 = ImageFont.truetype(os.path.join("waveshare_epd", 'Font.ttc'), 24)

class AlbumDrawer():
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        logging.info("Drawing to {}x{}px".format(size[0],size[1]))

    def create_album_image(self, info):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(img)
        y_padding = 0
        for i in ["title","artist"]:
            y_padding = self.write_text(draw, info[i], 20, y_padding)
        print(y_padding)
        self.paste_mono_image(info["image"], img, (0, y_padding), size=(self.width, self.height-y_padding))
        return img

    def write_text(self, draw, text, width, y_padding=0, x_padding=0):
        lines = textwrap.wrap(text, width=width)
        for i in range(len(lines)):
            draw.text((x_padding, y_padding + i*20), lines[i], font = font24, fill = 0)
        y_padding += (i+1)*26
        return y_padding

    def paste_mono_image(self, path, img, pos=(0,0), size=None):
        if not size:
            size = (self.width, self.height)
        image_file = Image.open(path) # open colour image
        if image_file.size[0] > size[0] or image_file.size[1] > size[1]:
            image_file.thumbnail((size[0],size[1]), Image.ANTIALIAS)
        image_file = image_file.convert('1') # convert image to black and white
        img.paste(image_file, pos)

    def create_mono_image(self, path):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        self.paste_mono_image(path,img)
        return img

