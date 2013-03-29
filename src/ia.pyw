#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import info
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QCoreApplication
from gui.mainwindow import MainWindow


def main():
    u""" Punto de entrada de la aplicación. """
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName(info.__app_name__)
    QCoreApplication.setApplicationVersion(info.__version__)
    QCoreApplication.setOrganizationName(info.__org_name__)
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
