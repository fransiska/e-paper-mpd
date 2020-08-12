#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE
import logging
import time
import random
import epapermpd.mpd_functions as mpd

logging.basicConfig(level=logging.ERROR)

mpd_music_directory = "/share/music"
mpd_top_directory = "fransiska"
base_directory = mpd_music_directory + "/" + mpd_top_directory

def get_album(directory):
    files = [x for x in os.listdir(directory)]
    music_files = [x for x in files if any([os.path.splitext(x)[1] == ext for ext in [".mp3",".flac",".ape",".m4a"]])]
    if len(music_files):
        return directory
    else:
        folders = [x for x in files if os.path.isdir(os.path.join(directory, x))]
        if len(folders):
            # Go deeper
            random_folder = random.choice(folders)
            return get_album(os.path.join(directory, random_folder))
        else:
            # Start again
            return get_album(base_directory)

def load_album():
    album_path = get_album(base_directory)[len(mpd_music_directory)+1:]
    os.system("mpc clear")
    p1 = Popen(["mpc", "ls", album_path], stdout=PIPE, stderr=PIPE)
    p2 = Popen(["mpc", "add"], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
    out,err = p2.communicate()
    if len(p1.stderr.read()):
        raise Exception(err)
    os.system("mpc play")

def main():
    os.system("mpc stop")
    while True:
        try:
            load_album()
            mpd.wait_until_playing()
            mpd.wait_until_stopped()
        except Exception as e:
            logging.error("Error in loading album: {}".format(e))
            time.sleep(1)

if __name__ == "__main__":
    main()
