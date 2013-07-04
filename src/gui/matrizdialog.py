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
                            QtCore.Qt.WindowMaximizeButtonHint)

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

        alto_gw = len(self.matriz)
        ancho_gw = len(self.matriz[0])
        dimension = alto_gw * ancho_gw

        ancho_estado_px = self.window_config["item"]["size"]
        ancho_gw_px = ancho_estado_px * dimension

        # Establecer propiedades visuales de la tabla
        self.ShowMatrizD.tblMatriz.setRowCount(dimension)
        self.ShowMatrizD.tblMatriz.setColumnCount(dimension)

        # Desactivar actualización de la tabla para optimizar la carga
        self.ShowMatrizD.tblMatriz.setUpdatesEnabled(False)

        headers_horizontales = []
        headers_verticales = []

        # Rellenar tabla con transiciones inválidas
        item_bg_color = QtGui.QColor(240, 240, 240)
        item_flags = QtCore.Qt.ItemIsEnabled
        item_align = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter

        item_dash = QtGui.QTableWidgetItem('-')
        item_dash.setBackgroundColor(item_bg_color)
        item_dash.setFlags(item_flags)
        item_dash.setTextAlignment(item_align)

        for fila in xrange(dimension):
            for columna in xrange(dimension):
                self.ShowMatrizD.tblMatriz.setItem(fila, columna, item_dash)

        # Rellenar tabla con items
        item_bg_color = QtGui.QColor("#FFFFFF")
        item_flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        item_align = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter

        # Cachear acceso a atributos y métodos
        matriz = self.matriz

        # Iterador de arreglo de Numpy
        matriz_iter = numpy.nditer(matriz, flags=['buffered'])

        # WIP: Nueva forma de visualizar matrices
        for (i, fila) in numpy.ndenumerate(matriz_iter):
            for (j, columna) in numpy.ndenumerate(fila):

                for key, value in acciones.iteritems():
                    # Cada item muestra la letra asignada al estado
                    if isinstance(value, float):
                        item = QtGui.QTableWidgetItem("{0:.2f}".format(value))
                    elif isinstance(value, int):
                        item = QtGui.QTableWidgetItem(str(value))

                    item.setBackgroundColor(item_bg_color)
                    item.setFlags(item_flags)
                    item.setTextAlignment(item_align)

                    # Coordenadas
                    coord_x = (fila * alto_gw) + columna
                    coord_y = ((key[0] - 1) * ancho_gw) + (key[1] - 1)

                    item.setToolTip(u"({0},{1}) ---> {2}"
                                    .format(fila + 1, columna + 1, key))
                    self.ShowMatrizD.tblMatriz.setItem(coord_x, coord_y, item)

                # Coordenadas
                coord_x = (fila * alto_gw) + columna

                # Armar headers horizontales (Acciones)
                headers_horizontales.append("A{0}\n({1},{2})"
                                            .format(coord_x + 1,
                                                    fila + 1,
                                                    columna + 1))

                # Armar headers verticales (Estados)
                headers_verticales.append("E{0} ({1},{2})"
                                          .format(coord_x + 1,
                                                  fila + 1,
                                                  columna + 1))

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
