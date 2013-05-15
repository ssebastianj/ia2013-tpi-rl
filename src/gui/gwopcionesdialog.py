#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from gui.qtgen.gwopcionesdialog import Ui_GWOpcionesDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GWOpcionesDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Opciones' heredada de QDialog.
    """
    def __init__(self, parent=None):
        u"""
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super(GWOpcionesDialog, self).__init__(parent)

        self.GWOpcionesD = Ui_GWOpcionesDialog()
        self.GWOpcionesD.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)

        self._init_vars()
        self.initialize_dialog()

    def _init_vars(self):
        self.estado_size = None
        self.pared_bloqueante = None
        self.recomp_final = None
        self.recomp_excelente = None
        self.recomp_bueno = None
        self.recomp_malo = None
        self.recomp_pared = None
        self.recomp_max = None

    def initialize_dialog(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        self._set_dialog_signals()

        self.GWOpcionesD.sbRecomPared.setEnabled(False)
        self.GWOpcionesD.cbRecomPared.addItem("Excluir de vecinos", 0)
        self.GWOpcionesD.cbRecomPared.addItem("Usar recompensa", 1)
        self.GWOpcionesD.sbGWEstadoSize.setValue(40)
        self.GWOpcionesD.sbRecomExcelente.setValue(100)
        self.GWOpcionesD.sbRecomBueno.setValue(50)
        self.GWOpcionesD.sbRecomMalo.setValue(-10)
        self.GWOpcionesD.sbRecomPared.setValue(-100)
        self.GWOpcionesD.sbRecomFinal.setMaximum(self.GWOpcionesD.sbRecomExcelente.maximum() + 50)

    def _set_dialog_signals(self):
        self.GWOpcionesD.cbRecomPared.currentIndexChanged.connect(self.toggle_recom_pared)
        self.GWOpcionesD.sbRecomExcelente.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomBueno.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomMalo.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomPared.valueChanged.connect(self.update_recom_final)

    def update_recom_final(self, valor):
        self.recomp_max = max([self.GWOpcionesD.sbRecomExcelente.value(),
                               self.GWOpcionesD.sbRecomBueno.value(),
                               self.GWOpcionesD.sbRecomMalo.value(),
                               self.GWOpcionesD.sbRecomPared.value()])
        self.recomp_max += 50
        self.GWOpcionesD.sbRecomFinal.setValue(self.recomp_max)

    def toggle_recom_pared(self, indice):
        if indice == 0:
            self.GWOpcionesD.sbRecomPared.setEnabled(False)
            self.pared_bloqueante = True
        elif indice == 1:
            self.GWOpcionesD.sbRecomPared.setEnabled(True)
            self.pared_bloqueante = False

    def accept(self):
        self.estado_size = self.GWOpcionesD.sbGWEstadoSize.value()
        self.recomp_final = self.GWOpcionesD.sbRecomFinal.value()
        self.recomp_excelente = self.GWOpcionesD.sbRecomExcelente.value()
        self.recomp_bueno = self.GWOpcionesD.sbRecomBueno.value()
        self.recomp_malo = self.GWOpcionesD.sbRecomMalo.value()
        self.recomp_pared = self.GWOpcionesD.sbRecomPared.value()

        super(GWOpcionesDialog, self).accept()

    def reject(self):
        super(GWOpcionesDialog, self).reject()
