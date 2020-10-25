#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output
import time

def get_current(host="localhost", info=""):
    if info:
        cmd = ["mpc", "-h", host, "-f", info, "current"]
    else:
        cmd = ["mpc", "-h", host, "current"]
    return check_output(cmd)

def get_info(host="localhost", info=["artist","album","title","track","time","file"]):
    formatted_info = "\n".join(["%{}%".format(i) for i in info])
    raw_info = get_current(host, formatted_info).decode("utf8").split('\n')
    json_info = {}
    for i in range(len(info)):
        json_info[info[i]] = raw_info[i]
    return json_info

def wait_for_idle(host="localhost"):
    check_output(["mpc", "-h", host, "idle", "player"])

def wait_until_playing(host="localhost"):
    while not get_current(host):
        wait_for_idle(host)

def wait_until_stopped(host="localhost"):
    while get_current(host):
        wait_for_idle(host)
