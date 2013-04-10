#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui
from gui.genrndvalsdialog import GenRndValsDialog
from gui.qt.mainwindow import Ui_MainWindow
from core.estado.estado import TIPOESTADO, TipoEstado
from core.gridworld.gridworld import GridWorld
from core.qlearning.qlearning import QLearning
from core.tecnicas.egreedy import EGreedy
from core.tecnicas.softmax import Softmax
from tools.circular import Circular  # http://www.juanjoconti.com.ar/2007/02/28/lista-circular-en-python/


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

    def _initialize_window(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        # Aspectos de la ventana principal
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))

        # Cargar técnicas posibles
        tecnicas = {0: "Greedy", 1: "ε-Greedy", 2: "Softmax"}
        self.WMainWindow.cbQLTecnicas.clear()
        for key, value in tecnicas.items():
            self.WMainWindow.cbQLTecnicas.addItem(_tr(value), key)
            self.WMainWindow.cbQLTecnicas.addAction(QtGui.QAction(_tr(value), self))
        self.WMainWindow.cbQLTecnicas.setCurrentIndex(1)
        self.WMainWindow.lblTau.hide()
        self.WMainWindow.sbQLTau.hide()

        # Cargar dimensiones posibles del tblGridWorld
        gw_dimensiones = ["6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"]

        self.WMainWindow.cbGWDimension.clear()
        for dimension in gw_dimensiones:
            self.WMainWindow.cbGWDimension.addItem(_tr(dimension), dimension)
            self.WMainWindow.menuDimension.addAction(QtGui.QAction(_tr(dimension), self))

        # Establece la dimensión por defecto del tblGridWorld en 6x6
        self.set_gw_dimension(self.WMainWindow.cbGWDimension.currentText())

        # Conexión de señales
        self._set_window_signals()

    def convert_dimension(self, dim_str):
        u"""
        Devuelve una tupla conteniendo el ancho y alto del GridWorld.

        :param dim_str: Cadena en forma {Ancho} x {Alto} representando la dimensión
        """
        dimension = str(dim_str)
        dimension = dimension.lower()
        dimension = dimension.split("x")
        return (int(dimension[0]), int(dimension[1]))

    def set_gw_dimension(self, dimension):
            u"""
            Configura el tblGridWorld a la dimensión seleccionada e Inicializa los estados en Neutros.

            :param dimension: Dimensión
            """
            # Obtener ancho y alto del GridWorld
            ancho_gw, alto_gw = self.convert_dimension(dimension)
            # Crear un nuevo GridWorld dados el ancho y el alto del mismo
            self.gridworld = GridWorld(ancho_gw, alto_gw)
            ancho_estado_px = 40
            ancho_gw_px = ancho_estado_px * ancho_gw

            # Establecer propiedades visuales de la tabla
            self.WMainWindow.tblGridWorld.setRowCount(alto_gw)
            self.WMainWindow.tblGridWorld.setColumnCount(ancho_gw)
            self.WMainWindow.tblGridWorld.horizontalHeader().setDefaultSectionSize(ancho_estado_px)
            self.WMainWindow.tblGridWorld.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            self.WMainWindow.tblGridWorld.verticalHeader().setDefaultSectionSize(ancho_estado_px)
            self.WMainWindow.tblGridWorld.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            self.WMainWindow.tblGridWorld.setCursor(QtCore.Qt.PointingHandCursor)
            ancho_contenedor = ancho_gw_px + self.WMainWindow.tblGridWorld.verticalHeader().width() + 1
            alto_contenedor = ancho_gw_px + self.WMainWindow.tblGridWorld.horizontalHeader().height() + 1
            self.WMainWindow.tblGridWorld.setFixedSize(ancho_contenedor, alto_contenedor)
            self.WMainWindow.tblGridWorld.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

            # Rellenar tabla con items
            for fila in range(0, self.gridworld.alto):
                for columna in range(0, self.gridworld.ancho):
                    estado = self.gridworld.get_estado(fila, columna)
                    letra_estado = estado.tipo.letra
                    # Cada item muestra la letra asignada al estado
                    item = QtGui.QTableWidgetItem(str(letra_estado))
                    item.setBackgroundColor(QtGui.QColor(estado.tipo.color))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
                    self.WMainWindow.tblGridWorld.setItem(fila, columna, item)

    def _set_window_signals(self):
        u"""
        Establece las señales correspondientes a los controles
        """
        self.WMainWindow.actionAppSalir.triggered.connect(self.exit)
        # Cambia la Dimensión del GridWorld al seleccionar la dimensión en el ComboBox
        self.WMainWindow.cbGWDimension.currentIndexChanged[str].connect(self.set_gw_dimension)
        # Cambia el Tipo de Estado al clickear un casillero del tblGridWorld
        self.WMainWindow.tblGridWorld.cellClicked[int, int].connect(self.switch_tipo_estado)
        # Empieza el Entrenamiento al clickear el btnEntrenar
        self.WMainWindow.btnEntrenar.clicked.connect(self.entrenar)
        # Interrumpe el Entrenamiento al clickear el btnTerminarTraining
        self.WMainWindow.btnTerminarProceso.clicked.connect(self.terminar_proceso)
        # Muestra sólo los parámetros utilizados en la técnica seleccionada en el ComboBox
        self.WMainWindow.cbQLTecnicas.currentIndexChanged.connect(self.parametros_segun_tecnica)
        self.WMainWindow.tblGridWorld.customContextMenuRequested.connect(self.show_item_menu)
        self.WMainWindow.btnGenValAleatorios.clicked.connect(self.show_gen_rnd_vals_dialog)

    def parametros_segun_tecnica(self, tecnica):
        u"""
        Muestra u oculta los parámetros en función de la técnica seleccionada.

        :param tecnica: Técnica seleccionada
        """
        # Obtener valor asociado al item seleccionado
        key = self.WMainWindow.cbQLTecnicas.itemData(tecnica).toInt()[0]

        if key == 0:
            # Greedy
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setValue(0.00)
            self.WMainWindow.sbQLEpsilon.setEnabled(False)
        elif key == 1:
            # E-Greedy
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setEnabled(True)
        elif key == 2:
            # Softmax
            self.WMainWindow.lblEpsilon.hide()
            self.WMainWindow.sbQLEpsilon.hide()
            self.WMainWindow.lblTau.show()
            self.WMainWindow.sbQLTau.show()

    def show_item_menu(self, posicion):
        u"""
        Muestra un menú contextual al hacer clic derecho sobre un item de la tabla

        :param posicion: Posición relativa del item clickeado
        """
        tipos_estados = self.gridworld.tipos_estados

        # Crear menu contextual para los items de la tabla
        menu_item = QtGui.QMenu("Tipo de estado")
        for tipo in tipos_estados.values():
            action = QtGui.QAction(tipo.nombre, self.WMainWindow.tblGridWorld)
            # Asociar al texto del menu el tipo de estado correspondiente
            action.setData(tipo.ide)
            menu_item.addAction(action)

        # Mostrar el menú y obtener el item de menu clickeado
        action = menu_item.exec_(self.WMainWindow.tblGridWorld.mapToGlobal(posicion))
        # Obtener el tipo de estado asociado al texto clickeado
        tipo_num = action.data().toInt()[0]
        # Averiguar en cual item de la tabla se hizo clic
        item = self.WMainWindow.tblGridWorld.itemAt(posicion)
        # Actualizar texto del item de la tabla en función del tipo de estado
        item.setText(tipos_estados[tipo_num].letra)
        # Establecer color de fondo de acuerdo al tipo de estado
        item.setBackgroundColor(QtGui.QColor(tipos_estados[tipo_num].color))
        estado = self.gridworld.get_estado(item.row(), item.column())
        # Establecer tipo de estado seleccionado al estado en la matriz
        estado.tipo = tipos_estados[tipo_num]

    def entrenar(self):
        u"""
        Probando si anda la señal clicked()
        """
        pass

    def terminar_proceso(self):
        u"""
        Probando si anda la señal clicked()
        """
        pass

    def switch_tipo_estado(self, fila, columna):
        tipos_estados = self.gridworld.tipos_estados.keys()
        # TODO: Cambiar tipo de estado al ir haciendo clic sobre el estado

    def show_gen_rnd_vals_dialog(self):
        self.GenRndValsDialog = GenRndValsDialog(self)
        self.GenRndValsDialog.show()

    def show_about_dialog(self):
        u"""
        Muestra el cuadro de diálogo Acerca de...
        """
        # TODO: Implementar AboutDialog
        self.DAboutDialog = AboutDialog(self)
        self.DAboutDialog.show()

    def closeEvent(self, event):
        """
        Reimplementa el evento 'closeEvent' de la clase padre.

        :param event: Evento.
        """
        pass

    def exit(self):
        u"""
        Finaliza la ejecución de la aplicación.
        """
        self.close()
