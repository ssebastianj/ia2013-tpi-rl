#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QCoreApplication
from gui.mainwindow import MainWindow
from info import app_info


def main():
    u""" Punto de entrada de la aplicación. """
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName(app_info.__app_name__)
    QCoreApplication.setApplicationVersion(app_info.__version__)
    QCoreApplication.setOrganizationName(app_info.__org_name__)
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
