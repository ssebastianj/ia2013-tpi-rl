#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import numpy

from PyQt4 import QtCore, QtGui
from gui.qtgen.matrizdialog import Ui_MatrizDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class ShowMatrizDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Opciones' heredada de QDialog.
    """
    def __init__(self, matriz, titulo_corto, titulo_largo=None, parent=None):
        u"""
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super(ShowMatrizDialog, self).__init__(parent)

        self.ShowMatrizD = Ui_MatrizDialog()
        self.ShowMatrizD.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint |
                            QtCore.Qt.WindowMinMaxButtonsHint)

        self.matriz = matriz
        self.titulo_corto_dialogo = titulo_corto
        self.titulo_largo_dialogo = titulo_largo

        self.init_vars()
        self.initialize_dialog()

    def init_vars(self):
        self.window_config = {"item":
                              {"show_tooltip": False,
                               "size": 30}}

    def initialize_dialog(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        self._set_dialog_signals()
        self.setWindowTitle(self.titulo_corto_dialogo)

        # Cachear acceso a atributos y métodos
        matriz = self.matriz
        tbl_set_item = self.ShowMatrizD.tblMatriz.setItem

        # Dimensiones de la matriz
        ancho_mat, alto_mat = matriz.shape

        # Dimensiones del GridWorld
        self.alto_gw = int(alto_mat ** 0.5)
        self.ancho_gw = int(ancho_mat ** 0.5)

        alto_gw = self.alto_gw
        ancho_gw = self.ancho_gw

        ancho_estado_px = self.window_config["item"]["size"]
        # ancho_gw_px = ancho_estado_px * ancho_gw

        # Establecer propiedades visuales de la tabla
        self.ShowMatrizD.tblMatriz.setRowCount(alto_mat)
        self.ShowMatrizD.tblMatriz.setColumnCount(ancho_mat)

        # Desactivar actualización de la tabla para optimizar la carga
        self.ShowMatrizD.tblMatriz.setUpdatesEnabled(False)

        headers_horizontales = []
        headers_verticales = []

        for fila in xrange(alto_mat):
            # Coordenadas del estado
            coord_x = int(fila / alto_gw)
            coord_y = fila - (coord_x * ancho_gw)

            # Armar headers horizontales (Acciones)
            headers_horizontales.append("A{0}\n({1},{2})".format(fila + 1,
                                                                 coord_x + 1,
                                                                 coord_y + 1))

            # Armar headers verticales (Estados)
            headers_verticales.append("E{0} ({1},{2})".format(fila + 1,
                                                              coord_x + 1,
                                                              coord_y + 1))

        # Ítem para transición válida
        item_bg_color_val = QtGui.QColor("#FFFFFF")
        item_flags_val = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        # Ítem para transición inválida
        item_bg_color_inv = QtGui.QColor(240, 240, 240)
        item_flags_inv = QtCore.Qt.ItemIsEnabled
        item_text_align = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter

        for i, accion in numpy.ndenumerate(matriz):
            if numpy.isnan(accion):
                item = QtGui.QTableWidgetItem('-')
                item.setBackgroundColor(item_bg_color_inv)
                item.setFlags(item_flags_inv)
                item.setTextAlignment(item_text_align)
            else:
                # Cada item muestra el valor asociado a la acción
                if isinstance(accion, float):
                    item = QtGui.QTableWidgetItem("{0:.2f}".format(accion))
                elif isinstance(accion, int):
                    item = QtGui.QTableWidgetItem(str(accion))

                item.setBackgroundColor(item_bg_color_val)
                item.setFlags(item_flags_val)
                item.setTextAlignment(item_text_align)

            # Coordenadas de origen
            coord_x_orig = int(i[0] / alto_gw)
            coord_y_orig = i[0] - (coord_x_orig * ancho_gw)

            # Coordenadas de destino
            coord_x_dest = int(i[1] / alto_gw)
            coord_y_dest = i[1] - (coord_x_dest * ancho_gw)

            item.setToolTip(u"({0},{1}) --> ({2},{3})".format(coord_x_orig + 1,
                                                              coord_y_orig + 1,
                                                              coord_x_dest + 1,
                                                              coord_y_dest + 1))

            # Agregar ítem a GridWorld
            tbl_set_item(i[0], i[1], item)

        self.ShowMatrizD.tblMatriz.setHorizontalHeaderLabels(headers_horizontales)
        self.ShowMatrizD.tblMatriz.setVerticalHeaderLabels(headers_verticales)

        # Reactivar la actualización de la tabla
        self.ShowMatrizD.tblMatriz.setUpdatesEnabled(True)

        self.ShowMatrizD.tblMatriz.horizontalHeader().setDefaultSectionSize(ancho_estado_px)
        self.ShowMatrizD.tblMatriz.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.ShowMatrizD.tblMatriz.verticalHeader().setDefaultSectionSize(ancho_estado_px)
        self.ShowMatrizD.tblMatriz.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.ShowMatrizD.tblMatriz.resizeColumnsToContents()

    def _set_dialog_signals(self):
        pass

    def accept(self):
        super(ShowMatrizDialog, self).accept()

    def reject(self):
        super(ShowMatrizDialog, self).reject()
