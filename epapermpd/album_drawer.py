#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PIL import Image,ImageDraw,ImageFont
import textwrap
import logging

font_face = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/waveshare_epd", 'Font.ttc')

class AlbumDrawer():
    def __init__(self, settings):
        self.width = size[0]
        self.height = size[1]
        self.font = ImageFont.truetype(font_face, font_size)
        self.sub_font = ImageFont.truetype(font_face, font_size-4)
        self.text_width = text_width
        self.sub_text_width = text_width+10
        self.image_size = image_size
        logging.debug("Drawing to {}x{}px".format(size[0],size[1]))

    def create_album_image(self, info):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(img)
        y_padding = 0

        if len(info["title"]):
            y_padding = self.write_centered_text(draw, info["track"] + ". " + info["title"], self.text_width, y_padding)
            y_padding = self.write_centered_text(draw, info["artist"], self.sub_text_width, y_padding, font=self.sub_font)
            y_padding = self.write_centered_text(draw, info["album"], self.sub_text_width, y_padding, font=self.sub_font)
        else:
            y_padding = self.write_centered_text(draw, info["file"], self.sub_text_width, y_padding, font=self.sub_font)

        image_pos = (int((self.width-self.image_size[0])/2),int(self.height-self.image_size[1]))
        try:
            self.paste_mono_image(info["image"], img, image_pos, size=self.image_size)
        except Exception as e:
            logging.error("No image to show: {}".format(e))
        return img

    def write_centered_text(self, draw, text, width, y_padding=0, font=None):
        if not font:
            font = self.font
        lines = textwrap.wrap(text, width=width)
        i = 0
        for i in range(len(lines)):
            w, h = draw.textsize(lines[i], font=font)
            draw.text((int((self.width-w)/2), y_padding + i*20), lines[i], font = font, fill = 0)
        y_padding += (i+1)*26
        return y_padding

    def paste_mono_image(self, path, img, pos=(0,0), size=None):
        if not len(path):
            return
        if not size:
            size = (self.width, self.height)
        image_file = Image.open(path) # open colour image
        if image_file.size[0] > size[0] or image_file.size[1] > size[1]:
            image_file.thumbnail((size[0],size[1]), Image.ANTIALIAS)
        image_file = image_file.convert('1') # convert image to black and white
        img.paste(image_file, pos)

    def show_mono_image(self, path):
        img = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        self.paste_mono_image(path,img)
        return img
