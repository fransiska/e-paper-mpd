#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output
import logging

logging.basicConfig(level=logging.DEBUG)

class MpdController():
    def __init__(self, host):
        self.host = host

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
        for i in ["artist","album","title","track","time"]:
            info[i] = self.get_value(i)
        return info
