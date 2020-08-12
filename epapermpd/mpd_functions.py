#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output
import time

def get_current(host="localhost"):
    return check_output(["mpc", "-h", host, "current"])

def wait_for_idle(host="localhost"):
    check_output(["mpc", "-h", host, "idle", "player"])

def wait_until_playing(host="localhost"):
    # Wait until mpc starts playing
    while not get_current(host):
        wait_for_idle(host)

def wait_until_stopped(host="localhost"):
    while get_current(host):
        wait_for_idle(host)

