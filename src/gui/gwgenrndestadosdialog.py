#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from gui.qtgen.gwgenrndestadosdialog import Ui_GWGenRndEstadosDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GWGenRndEstadosDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Opciones' heredada de QDialog.
    """
    def __init__(self, parent=None):
        u"""
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super(GWGenRndEstadosDialog, self).__init__(parent)

        self.GWGenRndEstadosD = Ui_GWGenRndEstadosDialog()
        self.GWGenRndEstadosD.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)

        self.initialize_dialog()

    def initialize_dialog(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        pass
