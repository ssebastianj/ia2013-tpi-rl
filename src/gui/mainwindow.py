#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from gui.qt.mainwindow import Ui_MainWindow

from core.estado.estado import Estado, TipoEstado
from core.gridworld.gridworld import GridWorld

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


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
        self._inicializar_estados()

    def _initialize_window(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        # Aspectos de la ventana principal
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))

        # Conexión de señales
        self._set_window_signals()

        # Cargar técnicas posibles
        tecnicas = ["Greedy", "ε-Greedy", "Softmax"]
        self.WMainWindow.cbQLTecnicas.clear()
        for tecnica in tecnicas:
            self.WMainWindow.cbQLTecnicas.addItem(_tr(tecnica))
            self.WMainWindow.cbQLTecnicas.addAction(QtGui.QAction(_tr(tecnica), self))


        # Cargar dimensiones posibles del tblGridWorld
        gw_dimensiones = ["6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"]


        self.WMainWindow.cbGWDimension.clear()
        for dimension in gw_dimensiones:
            self.WMainWindow.cbGWDimension.addItem(_tr(dimension))
            self.WMainWindow.menuDimension.addAction(QtGui.QAction(_tr(dimension), self))

        # Establece la dimensión por defecto del tblGridWorld en 6x6
        self.set_gw_dimension("6 x 6")

    def convert_dimension(self, dim_str):
        """
        Devuelve una tupla conteniendo el ancho y alto del GridWorld
        @param dim_str: Cadena en forma {Ancho} x {Alto} representando la dimensión
        """
        dimension = dim_str.lower()
        dimension = dimension.split("x")
        return (int(dimension[0]), int(dimension[1]))

    def set_gw_dimension(self, dimension):
            u"""Configura el tblGridWorld a la dimensión seleccionada e Inicializa los estados en Neutros"""

            self._inicializar_estados()

            ancho_gw, alto_gw = self.convert_dimension(dimension)
            gridworld = GridWorld(ancho_gw, alto_gw, estados)

            ancho_cuadrado = 40

            ancho_gridworld = ancho_cuadrado * cant_cuadrados

            self.WMainWindow.tblGridWorld.setRowCount(cant_cuadrados)
            self.WMainWindow.tblGridWorld.setColumnCount(cant_cuadrados)
            self.WMainWindow.tblGridWorld.horizontalHeader().setDefaultSectionSize(ancho_cuadrado)
            self.WMainWindow.tblGridWorld.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            self.WMainWindow.tblGridWorld.verticalHeader().setDefaultSectionSize(ancho_cuadrado)
            self.WMainWindow.tblGridWorld.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            self.WMainWindow.tblGridWorld.setCursor(QtCore.Qt.PointingHandCursor)
            ancho_contenedor = ancho_gridworld + self.WMainWindow.tblGridWorld.verticalHeader().width() + 1
            alto_contenedor = ancho_gridworld + self.WMainWindow.tblGridWorld.horizontalHeader().height() + 1
            self.WMainWindow.tblGridWorld.setFixedSize(ancho_contenedor, alto_contenedor)

            for fila in range(0, cant_cuadrados):
                for columna in range(0, cant_cuadrados):
                    elemento = QtGui.QTableWidgetItem("({0},{1})".format(fila, columna))
                    elemento.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.WMainWindow.tblGridWorld.setItem(fila, columna, elemento)


    def _set_window_signals(self):
        self.WMainWindow.actionAppSalir.triggered.connect(self.exit)

        # Cambia la Dimensión del GridWorld al seleccionar la dimensión en el ComboBox
        self.WMainWindow.cbGWDimension.currentIndexChanged[str].connect(self.set_gw_dimension)

        # Cambia el Tipo de Estado al clickear un casillero del tblGridWorld
        self.WMainWindow.tblGridWorld.cellClicked[int, int].connect(self.set_estados)

        # Empieza el Entrenamiento al clickear el btnEntrenar
        self.WMainWindow.btnEntrenar.clicked.connect(self.entrenar)

        # Interrumpe el Entrenamiento al clickear el btnTerminarTraining
        self.WMainWindow.btnTerminarTraining.clicked.connect(self.terminar)

        # Muestra sólo los parámetros utilizados en la técnica seleccionada en el ComboBox
        self.WMainWindow.cbQLTecnicas.currentIndexChanged[str].connect(self.parametros_segun_tecnica)

    def _inicializar_estados(self):
        # Identificadores de estado reservados
        # Ide = 0 (Estado Inicial)
        # Ide = 1 (Estado Intermedio)
        # Ide = 2 (Estado Final)
        # Ide = 3 (Agente)

        tipos_estados = []
        # Estado Inicial
        tipos_estados.append(TipoEstado(1, None, "Inicial", "I", None))
        # Estado Final
        tipos_estados.append(TipoEstado(2, None, "Final", "F", None))
        # Estado Agente
        tipos_estados.append(TipoEstado(7, None, "Agente", "A", None))
        # Estados Intermedios
        tipos_estados.append(TipoEstado(5, 100, "Excelente", "E", None))
        tipos_estados.append(TipoEstado(4, 50, "Bueno", "B", None))
        tipos_estados.append(TipoEstado(3, 10, "Malo", "M", None))
        tipos_estados.append(TipoEstado(0, 0, "Neutro", None, None))
        tipos_estados.append(TipoEstado(6, -100, "Pared", "P", None))

        string_estados = self.WMainWindow.cbGWDimension.currentText()
        cant_estados = int(string_estados.split("x")[1])
        for fila in range(0, cant_estados):
            for columna in range(0, cant_estados):
                    estado = Estado()
                    estado.set_fila(fila)
                    estado.set_columna(columna)
                    estado.set_tipo(0)


        # TODO: Inicializar todos los estados como Neutros


    def parametros_segun_tecnica(self, tecnica):

        if tecnica == "Softmax" :
                self.WMainWindow.sbQLEpsilon.close()
                self.WMainWindow.lbEpsilon.close()
                self.WMainWindow.sbQTau.show()
                self.WMainWindow.lbTau.show()
        elif tecnica == "Greedy" or tecnica == "ε-Greedy":
                self.WMainWindow.sbQTau.close()
                self.WMainWindow.lbTau.close()
                self.WMainWindow.sbQLEpsilon.show()
                self.WMainWindow.lbEpsilon.show()



    def entrenar(self):
        u"""Probando si anda la señal clicked()"""
        self.WMainWindow.label_2.setText("Estoy entrenando")


    def terminar (self):
        u"""Probando si anda la señal clicked()"""
        self.WMainWindow.label_2.setText("Termina")




    def set_estados(self, fila, columna):

        estado = Estado(fila, columna, 1)

        u"""si Estado == 0 es Estado Neutro[blanco] y no hay ningun Estado Inicial |FALTA COMPROBAR ESTO|, cambiar a Estado Inicial[Rojo]"""
        if estado.get_tipo() == 0 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(120, 20, 0))
            estado.set_tipo(1)

            u"""Si Estado == 0 es Estado Neutro,Hay Estado Inicial y no hay ningun Estado Final |FALTA COMPROBAR ESTO|, cambiar a Estado Final [Azul]"""
        elif estado.get_tipo() == 0 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(0, 60, 120))
            estado.set_tipo(2)

            u"""Si Estado == 0 es Estado Neutro, Hay Estado Inicial y Estado Final, cambiar a Estado Malo[Marron] """
        elif estado.get_tipo() == 0 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(59, 44, 120))
            estado.set_tipo(3)

            u"""si Estado ==1 es Estado Inicial[Rojo] y no hay ningun Estado Final |FALTA COMPROBAR ESTO|, cambiar a Estado Final[Azul]"""
        elif estado.get_tipo() == 1 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(0, 60, 120))
            estado.set_tipo(2)

            u"""si Estado ==1 es Estado Inicial[Rojo] y  ya Hay Estado Final, cambiar a Estado Malo[Marron]"""
        elif estado.get_tipo() == 1 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(59, 44, 120))
            estado.set_tipo(3)

            u"""si Estado == 2 es Estado Final[Azul], cambiar a Estado Malo[Marron]"""
        elif estado.get_tipo() == 2 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(59, 44, 120))
            estado.set_tipo(3)

            u"""si Estado == 3 es Estado Malo[Marron], cambiar a Estado Bueno[Violeta]"""
        elif estado.get_tipo() == 3 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(128, 100, 125))
            estado.set_tipo(4)

            u"""si Estado == 4 es Estado Bueno[Violeta], cambiar a Estado Excelente[Verde]"""
        elif estado.get_tipo() == 4 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(154, 176, 155))
            estado.set_tipo(5)

            u"""si Estado == 3 es Estado Excelente[Verde], cambiar a Estado Pared[Negro]"""
        elif estado.get_tipo() == 5 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(0, 0, 0))
            estado.set_tipo(6)

            u"""si Estado == 6 es Estado Pared[Negro], cambiar a Estado Neutro[Blanco]"""
        elif estado.get_tipo() == 6 :
            self.WMainWindow.tblGridWorld.item(fila, columna).setBackgroundColor(QtGui.QColor(255, 255, 255))
            estado.set_tipo(0)





    def show_about_dialog(self):
        u"""
        Muestra el cuadro de diálogo Acerca de...
        """
        self.DAboutDialog = AboutDialog(self)
        self.DAboutDialog.show()

    def closeEvent(self, event):
        """
        Reimplementa el evento 'closeEvent' de la clase padre.

        @param event: Evento.
        """
        pass

    def exit(self):
        u"""
        Finaliza la ejecución de la aplicación.
        """
        self.close()
