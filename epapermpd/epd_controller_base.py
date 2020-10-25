#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class EpdControllerBase():
    def __init__(self, size):
        raise NotImplementedError

    def get_size(self):
        return self.epd.width, self.epd.height

    def display(self, image):
        try:
            logging.info("Drawing")
            self.clear()
            self.display_image(image)
        except Exception as e:
            logging.info("Error: {}".format(e))

    def clear(self):
        self.epd.Clear()

    def display_image(self, image):
        raise NotImplementedError
        
