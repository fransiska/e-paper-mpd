#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PIL import Image,ImageDraw,ImageFont
import textwrap
import logging

font_face = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/waveshare_epd", 'Font.ttc')

DISPLAY_TYPES = {
    "1in54b": {
        "color": 2,
        "width": 200,
        "height": 200,
        "font_size": 26,
        "text_width": 10
    },
    "4in2": {
        "color": 1,
        "width": 300,
        "height": 400,
        "font_size": 26,
        "text_width": 22
    }
}

class AlbumDrawer():
    def __init__(self, settings):
        display_type = DISPLAY_TYPES[settings["type"]]
        self.width = display_type["width"]
        self.height = display_type["height"]
        self.color = display_type["color"]

        font_size = display_type["font_size"]
        self.font = ImageFont.truetype(font_face, font_size)
        self.sub_font = ImageFont.truetype(font_face, font_size-4)
        self.text_width = display_type["text_width"]
        self.sub_text_width = self.text_width+10

        self.image = settings.get("image", {})
        try: self.image_pos = (int((self.width-self.image["size"])/2),int(self.height-self.image["size"]))
        except: pass

        logging.debug("Drawing to {}x{}px".format(self.width,self.height))

    def create_album_image(self, info):
        image_black = Image.new('1', (self.width, self.height), 255) # 255: clear the frame
        image_red = Image.new('1', (self.width, self.height), 255) # 255: clear the frame

        if self.color > 1:
            y_padding = self.write_title_text(image_red, info)
        else:
            y_padding = self.write_title_text(image_black, info)
        self.write_other_text(image_black, info, y_padding)
        self.write_image(image_black, info)
        image_black.save("/tmp/black.png")
        image_red.save("/tmp/red.png")
        return [image_black, image_red]

    def write_title_text(self, image_black, info):
        draw = ImageDraw.Draw(image_black)
        y_padding = 0
        if len(info["title"]):
            y_padding = self.write_centered_text(draw, info["track"] + ". " + info["title"], self.text_width, y_padding)
        else:
            y_padding = self.write_centered_text(draw, info["file"], self.sub_text_width, y_padding, font=self.sub_font)
        return y_padding

    def write_other_text(self, image_black, info, y_padding):
        draw = ImageDraw.Draw(image_black)
        if len(info["title"]):
            y_padding = self.write_centered_text(draw, info["artist"], self.sub_text_width, y_padding, font=self.sub_font)
            y_padding = self.write_centered_text(draw, info["album"], self.sub_text_width, y_padding, font=self.sub_font)

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

    def write_image(self, image_black, info):
        try:
            mono_image = self.get_mono_image(info["image"], size=(self.image["size"],self.image["size"]))
            image_black.paste(mono_image, self.image_pos)
        except Exception as e:
            logging.error("No image to show: {}".format(e))
        
    def get_mono_image(self, path, img, size=None):
        if not len(path):
            return None
        if not size:
            size = (self.width, self.height)
        image_file = Image.open(path) # open colour image
        if image_file.size[0] > size[0] or image_file.size[1] > size[1]:
            image_file.thumbnail((size[0],size[1]), Image.ANTIALIAS)
        image_file = image_file.convert('1') # convert image to black and white
        return image_file
