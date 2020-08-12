#!/usr/bin/env python3

import os
import random
import epapermpd.mpd_functions as mpd
import logging

logging.basicConfig(level=logging.ERROR)

mpd_music_directory = "/share/music"
mpd_top_directory = "fransiska"
base_directory = mpd_music_directory + "/" + mpd_top_directory

def get_random_directory(directory):
    return random.choice([x for x in os.listdir(directory)])

def load_album():
    artist = get_random_directory(base_directory)
    album = get_random_directory(base_directory + "/" + artist)
    album_path = mpd_top_directory + "/" + artist + "/" + album
    logging.debug("Loading {} : {}".format(artist, album))
    cmd = "mpc clear; mpc ls '{}' | mpc add ; mpc play".format(album_path)
    os.system(cmd)

def main():
    while True:
        logging.debug("Loading new album")
        try: load_album()
        except Exception as e: logging.error("Error in loading album: {}".format(e))
        mpd.wait_until_playing()
        mpd.wait_until_stopped()

if __name__ == "__main__":
    main()
