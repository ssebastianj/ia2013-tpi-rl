#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from gui.qt.mainwindow import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class MainWindow(QtGui.QMainWindow):
    u"""
    Clase heredada de QMainWindow encargada de mostrar la ventana principal de
    la aplicación.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.WMainWindow = Ui_MainWindow()
        self.WMainWindow.setupUi(self)
        self._initialize_window()

    def _initialize_window(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))

        ancho_cuadrado = 40
        cant_cuadrados = 10
        ancho_gridworld = ancho_cuadrado * cant_cuadrados

        self.WMainWindow.GridWorld.setRowCount(cant_cuadrados)
        self.WMainWindow.GridWorld.setColumnCount(cant_cuadrados)
        self.WMainWindow.GridWorld.horizontalHeader().setDefaultSectionSize(ancho_cuadrado)
        self.WMainWindow.GridWorld.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.WMainWindow.GridWorld.verticalHeader().setDefaultSectionSize(ancho_cuadrado)
        self.WMainWindow.GridWorld.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.WMainWindow.GridWorld.setCursor(QtCore.Qt.PointingHandCursor)
        ancho_contenedor = ancho_gridworld + self.WMainWindow.GridWorld.verticalHeader().width() + 1
        alto_contenedor = ancho_gridworld + self.WMainWindow.GridWorld.horizontalHeader().height() + 1
        self.WMainWindow.GridWorld.setFixedSize(ancho_contenedor, alto_contenedor)

        for fila in range(0, 10):
            for columna in range(0, 10):
                elemento = QtGui.QTableWidgetItem("({0},{1})".format(fila, columna))
                elemento.setFlags(QtCore.Qt.ItemIsEnabled)
                self.WMainWindow.GridWorld.setItem(fila, columna, elemento)
