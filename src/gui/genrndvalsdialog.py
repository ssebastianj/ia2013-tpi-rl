#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from info import app_info
from gui.qtgen.genrndvalsdialog import Ui_GenRndValsDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GenRndValsDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Conectar a puerto' heredada de QDialog.
    """
    def __init__(self, parent=None):
        u"""
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
        self.ORG_NAME = app_info.__org_name__
        self.APP_NAME = app_info.__app_name__

    def _initialize_dialog(self):
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))

    def accept(self, *args, **kwargs):
        u"""
        Redefinición del método 'acept' de la clase padre.

        :param \*args: \*args
        :param \**kwargs: \**kwargs
        """
        self.gen_dimension_random = self.GenRndValsDialog.chkDimensionAleatoria.isChecked()
        self.gen_tecnicas_random = self.GenRndValsDialog.chkTecnicaAleatoria.isChecked()
        self.gen_estados_random = self.GenRndValsDialog.optGenerarEstados.isChecked()
        self.gen_vals_param_random = self.GenRndValsDialog.optGenerarValoresParam.isChecked()
        self.gen_todo_random = self.GenRndValsDialog.optGenerarTodo.isChecked()

        super(GenRndValsDialog, self).accept()
