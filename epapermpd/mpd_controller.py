#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import check_output
import time
import glob
import logging
from . import mpd_functions

class MpdController():
    def __init__(self, host):
        self.host = host
        self.music_directory = self.get_music_directory()

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
        folder_name = os.path.dirname(self.music_directory + "/" + filename)
        # Try the default names first
        for name in  ["cover.jpg","album.jpg","front.jpg"]:
            file_path = folder_name + "/" + name
            if os.path.isfile(file_path):
                return file_path
        # If not, get any jpg
        jpg_list = glob.glob(glob.escape(folder_name) + "/*.jpg")
        if len(jpg_list):
            return jpg_list[0]
        else:
            return ""

    def get_current(self):
        return mpd_functions.get_current(self.host)

    def get_info(self):
        info = mpd_functions.get_info(self.host)
        info.update({"image":self.get_album_image(info["file"])})
        return info

    def wait_for_track_change(self):
        mpd_functions.wait_for_idle(self.host)

    def wait_until_playing(self):
        mpd_functions.wait_until_playing(self.host)
