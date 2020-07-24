#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output

class MpdController():
    def __init__(self, host):
        self.host = host

    def get_current(self):
        return check_output(["mpc", "-h", self.host, "current"])

