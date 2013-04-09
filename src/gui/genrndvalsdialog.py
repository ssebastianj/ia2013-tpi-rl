#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, os, info
from PyQt4 import QtCore, QtGui
from gui.qt.genrndvalsdialog import Ui_GenRndValsDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GenRndValsDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Conectar a puerto' heredada de QDialog.
    """
    def __init__(self, parent=None):
        """
        Constructor de la clase GenRndValsDialog.

        :param parent: Widget padre.
        """
        super(GenRndValsDialog, self).__init__(parent)
        self.GenRndValsDialog = Ui_GenRndValsDialog()
        self.GenRndValsDialog.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)
        self._initialize_dialog()
        self.ORG_NAME = info.__org_name__
        self.APP_NAME = info.__app_name__

    def _initialize_dialog(self):
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))
