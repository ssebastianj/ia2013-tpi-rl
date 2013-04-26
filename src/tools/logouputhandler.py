#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import


import logging
from PyQt4 import QtGui


class LogOutputHandler(logging.Handler):
    u"""
    Fuente 1: http://stackoverflow.com/questions/8356336/how-to-capture-output-of-pythons-interpreter-and-show-in-a-text-widget
    Fuente 2: http://pantburk.info/?blog=77
    """
    def __init__(self, widget):
        super(LogOutputHandler, self).__init__()
        self.widget = widget

    def emit(self, record):
        self.widget.appendPlainText(record.message)

    def setLevel(self, level):
        super(LogOutputHandler, self).setLevel(level)
