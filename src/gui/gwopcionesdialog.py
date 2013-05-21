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
        self.rec_state_bg = "#000000"
        self.ent_state_bg = "#000000"

    def initialize_dialog(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        self._set_dialog_signals()

        self.GWOpcionesD.sbRecomFinal.setEnabled(True)
        self.GWOpcionesD.sbRecomPared.setEnabled(False)
        self.GWOpcionesD.cbRecomPared.addItem("Excluir de vecinos", 0)
        self.GWOpcionesD.cbRecomPared.addItem("Usar recompensa", 1)
        self.GWOpcionesD.sbGWEstadoSize.setValue(40)
        self.GWOpcionesD.sbRecomExcelente.setValue(100)
        self.GWOpcionesD.sbRecomBueno.setValue(50)
        self.GWOpcionesD.sbRecomMalo.setValue(-10)
        self.GWOpcionesD.sbRecomPared.setValue(-100)
        color_ent = QtGui.QColor(self.ent_state_bg)
        color_rec = QtGui.QColor(self.rec_state_bg)
        self.GWOpcionesD.lblEntActStateBG.setPalette(QtGui.QPalette(color_ent))
        self.GWOpcionesD.lblRecActStateBG.setPalette(QtGui.QPalette(color_rec))
        self.GWOpcionesD.lblEntActStateBG.setText(color_ent.name())
        self.GWOpcionesD.lblRecActStateBG.setText(color_rec.name())
        self.GWOpcionesD.lblEntActStateBG.setAutoFillBackground(True)
        self.GWOpcionesD.lblRecActStateBG.setAutoFillBackground(True)

        self.update_recom_final()

    def _set_dialog_signals(self):
        self.GWOpcionesD.cbRecomPared.currentIndexChanged.connect(self.toggle_recom_pared)
        self.GWOpcionesD.sbRecomExcelente.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomBueno.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomMalo.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbRecomPared.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.btnEntSelectActStateBG.clicked.connect(self.select_ent_state_color)
        self.GWOpcionesD.btnRecSelectActStateBG.clicked.connect(self.select_rec_state_color)

    def update_recom_final(self, valor=None):
        self.recomp_max = max([self.GWOpcionesD.sbRecomExcelente.value(),
                               self.GWOpcionesD.sbRecomBueno.value(),
                               self.GWOpcionesD.sbRecomMalo.value(),
                               self.GWOpcionesD.sbRecomPared.value()])
        self.recomp_max += 1
        self.GWOpcionesD.sbRecomFinal.setMinimum(self.recomp_max)
        # self.GWOpcionesD.sbRecomFinal.setValue(self.recomp_max)

    def toggle_recom_pared(self, indice):
        if indice == 0:
            self.GWOpcionesD.sbRecomPared.setEnabled(False)
            self.pared_bloqueante = True
        elif indice == 1:
            self.GWOpcionesD.sbRecomPared.setEnabled(True)
            self.pared_bloqueante = False

    def select_ent_state_color(self):
        qcolordiag = QtGui.QColorDialog(self)
        qcolordiag.setOption(qcolordiag.ShowAlphaChannel)
        state_color = qcolordiag.getColor()

        if state_color.isValid():
            self.GWOpcionesD.lblEntActStateBG.setPalette(QtGui.QPalette(state_color))
            self.GWOpcionesD.lblEntActStateBG.setText(state_color.name())
            self.GWOpcionesD.lblEntActStateBG.setAutoFillBackground(True)
            self.ent_state_bg = state_color.name()

    def select_rec_state_color(self):
        qcolordiag = QtGui.QColorDialog(self)
        qcolordiag.setOption(qcolordiag.ShowAlphaChannel)
        state_color = qcolordiag.getColor()

        if state_color.isValid():
            self.GWOpcionesD.lblRecActStateBG.setPalette(QtGui.QPalette(state_color))
            self.GWOpcionesD.lblRecActStateBG.setText(state_color.name())
            self.GWOpcionesD.lblRecActStateBG.setAutoFillBackground(True)
            self.rec_state_bg = state_color.name()

    def accept(self):
        self.estado_size = self.GWOpcionesD.sbGWEstadoSize.value()
        self.recomp_final = self.GWOpcionesD.sbRecomFinal.value()
        self.recomp_excelente = self.GWOpcionesD.sbRecomExcelente.value()
        self.recomp_bueno = self.GWOpcionesD.sbRecomBueno.value()
        self.recomp_malo = self.GWOpcionesD.sbRecomMalo.value()
        self.recomp_pared = self.GWOpcionesD.sbRecomPared.value()
        self.ent_show_state = self.GWOpcionesD.gbEntShowActualState.isChecked()
        self.ent_usar_color_fondo = self.GWOpcionesD.optEntMostrarColorFondo.isChecked()
        self.ent_usar_icono = self.GWOpcionesD.optEntMostrarIcono.isChecked()
        self.rec_show_state = self.GWOpcionesD.gbRecShowActualState.isChecked()
        self.rec_usar_color_fondo = self.GWOpcionesD.optRecMostrarColorFondo.isChecked()
        self.rec_usar_icono = self.GWOpcionesD.optRecMostrarIcono.isChecked()

        super(GWOpcionesDialog, self).accept()

    def reject(self):
        super(GWOpcionesDialog, self).reject()
