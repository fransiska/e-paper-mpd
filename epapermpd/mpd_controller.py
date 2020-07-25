#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import check_output
import logging

logging.basicConfig(level=logging.DEBUG)

class MpdController():
    def __init__(self, host):
        self.host = host
        self.music_directory = self.get_music_directory()

    def get_current(self):
        return check_output(["mpc", "-h", self.host, "current"])

    def get_value(self, key):
        try:
            value = check_output(["mpc", "current", "-h", self.host, "-f","'%{}%'".format(key)]).decode('utf8').strip()[1:-1]
        except Exception as e:
            logging.error("Error in getting info {}".format(e))
            value = ""
        return value
       
    def get_info(self):
        info = {}
        for i in ["artist","album","title","track","time","file"]:
            info[i] = self.get_value(i)
        info["image"] = self.get_album_image(info["file"])
        return info

    def get_music_directory(self):
        for filename in ["~/.mpdconf","/etc/mpd.conf"]:
            if os.path.exists(filename):
                with open(filename,"r") as f:
                    content = f.read()
                    for line in content.split("\n"):
                        if "music_directory" in line and line[0] != "#":
                            return line.split('"')[1]

        return ""

    def get_album_image(self, filename):
        image_filename = "album.jpg"
        fullpath = os.path.dirname(self.music_directory + "/" + filename) + "/" + image_filename
        if os.path.exists(fullpath):
            return fullpath
        else:
            return ""
