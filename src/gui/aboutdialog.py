#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from info import app_info
from gui.qtgen.aboutdialog import Ui_AboutDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class AboutDialog(QtGui.QDialog):
    """docstring for AboutDialog"""
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.AboutDialog = Ui_AboutDialog()
        self.AboutDialog.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)
        self._initialize_dialog()
        self.ORG_NAME = app_info.__org_name__
        self.APP_NAME = app_info.__app_name__

    def _initialize_dialog(self):
        self.AboutDialog.lblAppVersion.setText(_tr("Versión {0}".format(app_info.__version__)))
