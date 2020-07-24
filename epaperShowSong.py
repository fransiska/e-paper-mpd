#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd1in54b
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import traceback
import textwrap
from tinytag import TinyTag
import urllib.parse
from subprocess import check_output
import os
import datetime

host="pi.local"


def get_current_filename():
    filename = check_output(["mpc", "current", "-h", host, "-f","'%file%'"])
    return filename.decode("utf8").strip()[1:-1].split('/')[-1]

def get_track_info():
    try: artist = check_output(["mpc", "current", "-h", host, "-f","'%artist%'"]).decode('utf8').strip()[1:-1]
    except: artist = ""
    try: album = check_output(["mpc", "current", "-h", host, "-f","'%album%'"]).decode('utf8').strip()[1:-1]
    except: album = ""
    title = check_output(["mpc", "current", "-h", host, "-f","'%title%'"]).decode('utf8').strip()[1:-1]
    if len(title) == 0:
        raise Exception("title not found")
    try: track = check_output(["mpc", "current", "-h", host, "-f","'%track%'"]).decode('utf8').strip()[1:-1]
    except: track = ""
    try: duration = check_output(["mpc", "current", "-h", host, "-f","'%time%'"]).decode('utf8').strip()[1:-1]
    except: duration = ""
    return artist, album, title, track, duration

def clear():
    epd = epd1in54b.EPD()
    epd.init()
    blackimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
    time.sleep(1)
    epd.sleep()

def display_filename(filename):
    epd = epd1in54b.EPD()
    epd.init()
    blackimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame    
    redimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    font22 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

    # filename
    starting_line = 10
    print(filename)
    filename = os.path.basename(filename)
    print(filename)

    lines = textwrap.wrap(filename, width=17)
    for i in range(len(lines)):
        drawred.text((5, starting_line + i*20), lines[i], font = font18, fill = 0)
    starting_line += (i+1)*20
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
    time.sleep(1)
    epd.sleep()    

def display(artist, album, title, track, duration):
    epd = epd1in54b.EPD()
    epd.init()

    # Drawing on the image
    blackimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd1in54b.EPD_WIDTH, epd1in54b.EPD_HEIGHT), 255)  # 255: clear the frame
    print("drawing")
    drawblack = ImageDraw.Draw(blackimage)
    drawred = ImageDraw.Draw(redimage)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    font22 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    width = 17

    # artist
    starting_line = 10
    i = 0
    lines = textwrap.wrap(artist, width=width)
    for i in range(len(lines)):
        drawred.text((5, starting_line + i*22), lines[i], font = font22, fill = 0)
    starting_line += (i+1)*22

    # album
    lines = textwrap.wrap(album, width=width)
    for i in range(len(lines)):
        drawblack.text((5, starting_line + i*20), lines[i], font = font18, fill = 0)
    starting_line += (i+1)*20

    # track
    lines = textwrap.wrap(track, width=width)
    for i in range(len(lines)):
        drawred.text((5, starting_line + i*20), lines[i], font = font18, fill = 0)
    starting_line += (i+1)*20 + 20

    # title
    lines = textwrap.wrap(title, width=width-2)
    for i in range(len(lines)):
        drawblack.text((5, starting_line + i*20), lines[i], font = font18, fill = 0)
    starting_line += (i+1)*20 + 2

    # duration
    lines = textwrap.wrap(duration, width=width)
    for i in range(len(lines)):
        drawblack.text((5, starting_line + i*20), lines[i], font = font18, fill = 0)
    starting_line += (i+1)*20

    #newimage = Image.open('atari.bmp')
    #blackimage.paste(newimage, (0,0))
    epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))

    blackimage.save('/tmp/b.png')
    redimage.save('/tmp/r.png')

    print("sleep")
    epd.sleep()

if __name__ == "__main__":
    # Wait until mpc starts playing
    while not check_output(["mpc", "-h", host, "current"]):
        time.sleep(1)

    currFilename=""
    while True:
        while True:
            print("new loop")
            # Check for new filename
            while True:
                try:
                    newFilename=get_current_filename()
                    break
                except Exception as e:
                    print(str(e))
                    time.sleep(1)

            print("curr",currFilename,"new",newFilename)
            if currFilename==newFilename:
                time.sleep(1)
                break

            # Display track
            try:            
                try:
                    print("displaying")
                    artist, album, title, track, duration = get_track_info()
                    display(artist,album,title,track,duration)
                except Exception as e:
                    print("error, displaying filename: {}".format(e))
                    display_filename(newFilename)
            except Exception as e:
                print("cannot display filename " + 'traceback.format_exc():\n%s',traceback.format_exc())
                clear()
            currFilename=newFilename
        print("waiting")
        check_output(["mpc", "-h", host, "idle", "player"])
