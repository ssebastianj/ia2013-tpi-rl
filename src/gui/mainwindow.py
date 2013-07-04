#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    import cdecimal as decimal
except ImportError:
    import decimal

import csv
import logging
import multiprocessing
import Queue
import random
import threading
import time

from PyQt4 import QtCore, QtGui

from info import app_info

from gui.aboutdialog import AboutDialog
from gui.qtgen.mainwindow import Ui_MainWindow
from gui.gwgenrndestadosdialog import GWGenRndEstadosDialog
from gui.gwopcionesdialog import GWOpcionesDialog
from gui.matrizdialog import ShowMatrizDialog

from core.estado.estado import TIPOESTADO, TipoEstado
from core.gridworld.gridworld import GridWorld
from core.qlearning.qlearning import QLearning
from core.tecnicas.aleatorio import Aleatorio
from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax

from graphs.avgrwds.worker import GraphRecompensasPromedioWorker
from graphs.sucessfuleps.worker import GraphSucessfulEpisodesWorker
# from graphs.itersep.worker import GraphIteracionesXEpisodioWorker
from graphs.matdiffs.worker import GraphMatrizDiffsWorker

from tools.queue import get_item_from_queue
from tools.taskbar import taskbar

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

        # Logging Config
        logging.basicConfig(level=logging.DEBUG,
                           format="[%(levelname)s] – %(threadName)-10s : %(message)s")
        self._logger = logging.getLogger()
        self._logger.disabled = not app_info.__DEBUG__

        # Freeze Support
        self._logger.debug("Activar Freeze Support")
        multiprocessing.freeze_support()
        self._logger.debug("Cantidad de CPUs: {0}"
                      .format(multiprocessing.cpu_count()))

        self._init_vars()
        self._initialize_window()

    def _init_vars(self):
        u"""
        Inicializa las variables 'globales'.
        """
        self.estado_inicial = None
        self.estado_final = None
        self.pre_estado_inicial = None
        self.pre_estado_final = None
        self.matriz_q = None
        self.mat_est_acc = None
        self.wnd_timer = None
        self.ql_entrenar_error_q = None
        self.ql_entrenar_out_q = None
        self.ql_recorrer_error_q = None
        self.ql_recorrer_out_q = None
        self.working_process = None
        self.worker_queues_list = None
        self.entrenar_is_running = False
        self.recorrer_is_running = False
        self.wnd_taskbar = None
        self.last_state_bkp = None
        self.last_state_bg = None
        self.last_state_text = None
        self.camino_optimo = None
        self.camino_optimo_active = None

        # Variables necesarias para los gráficos
        self.graph_recompensas_promedio = None
        self.graph_episodios_finalizados = None
        # self.graph_iters_por_episodio = None
        self.graph_mat_diff = None

        self.tecnicas = {  # 0: "Greedy",
                           1: "ε-Greedy",
                           2: "Softmax",
                           # 3: "Aleatorio"
                         }

        self.gw_dimensiones = ["3 x 3", "4 x 4", "5 x 5",
                               "6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"]

        self.window_config = {"item":
                              {"show_tooltip": True,
                               "menu_estado":
                               {"ocultar_tipos":
                                [TIPOESTADO.AGENTE],
                                "enabled": True
                                },
                               "size": 40},
                              "gw":
                             {"entrenamiento": {"actual_state": {"show": True, "color": "#000000", "icono": None},
                                                "recompfinalauto": True,
                                                "maxitersreached": {"action": 1, "warn": False}
                                                },
                              "recorrido": {"actual_state": {"show": True, "color": "#000000", "icono": None}}
                              },
                              "tipos_estados":
                              {0: TipoEstado(0, None, _tr("Inicial"), _tr("I"), "#FF5500", None),
                               1: TipoEstado(1, 1000, _tr("Final"), _tr("F"), "#00AB00", None),
                               2: TipoEstado(2, None, _tr("Agente"), _tr("A"), "#474747",
                                             QtGui.QIcon(QtGui.QPixmap(":/iconos/Agente_1.png"))),
                               3: TipoEstado(3, 0, _tr("Neutro"), _tr("N"), "#FFFFFF", None),
                               4: TipoEstado(4, 100, _tr("Excelente"), _tr("E"), "#BB0011", None),
                               5: TipoEstado(5, 50, _tr("Bueno"), _tr("B"), "#4F0ACC", None),
                               6: TipoEstado(6, -50, _tr("Malo"), _tr("M"), "#EB00A1", None),
                               7: TipoEstado(7, None, _tr("Pared"), _tr("P"), "#000000", None),
                               },
                              "opt_path":
                             {"color": "#55FF00",
                                 "pintar_inicial": False,
                                 "pintar_final": False,
                                 "delay": 0,
                                 "show_icon": False
                              },
                              "exponentes_final": {6: 13,
                                                   7: 18,
                                                   8: 20,
                                                   9: 29,
                                                   10: 32
                                                   }
                              }

    def _initialize_window(self):
        u"""
        Inicializa el aspecto y características de la ventana.
        """
        # Aspectos de la ventana principal
        screen_geometry = QtGui.QApplication.desktop().screenGeometry()
        y_wnd = (screen_geometry.height() - self.height()) / 2.0
        x_wnd = (screen_geometry.width() - self.width()) / 2.0
        # Centrar la ventana en la pantalla
        self.move(x_wnd, y_wnd)

        self.setWindowFlags(QtCore.Qt.WindowSoftkeysVisibleHint)

        # Configurar statusbar
        # Agregar barra de progreso
        self._ent_progress_bar = QtGui.QProgressBar()
        self.WMainWindow.statusBar.addPermanentWidget(self._ent_progress_bar)
        self._ent_progress_bar.setFixedSize(350, 14)
        self._ent_progress_bar.setFormat(_tr(" %p% / %m episodios"))
        self._ent_progress_bar.setVisible(False)

        # Agregar etiqueta para mostrar coordenadas actuales
        self.lbl_item_actual = QtGui.QLabel()
        self.lbl_item_actual.setFixedWidth(120)
        self.WMainWindow.statusBar.addPermanentWidget(self.lbl_item_actual)

        self.WMainWindow.tblGridWorld.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.WMainWindow.tblGridWorld.setSortingEnabled(False)
        self.WMainWindow.tblGridWorld.setMouseTracking(True)
        self.WMainWindow.btnTerminarProceso.setEnabled(False)
        self.WMainWindow.btnRecorrer.setEnabled(False)
        self.WMainWindow.actionAgenteRecorrer.setDisabled(True)
        self.WMainWindow.actionAgenteCancelar.setDisabled(True)
        self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)
        self.WMainWindow.btnMostrarMatrizR.setDisabled(True)
        self.WMainWindow.lblCantMaxIteraciones.setDisabled(True)
        self.WMainWindow.sbCantMaxIteraciones.setDisabled(True)
        self.WMainWindow.gbCOAcciones.setDisabled(True)
        self.WMainWindow.gbCOAnimacion.setDisabled(True)
        self.WMainWindow.lblMatQDiff.setDisabled(True)
        self.WMainWindow.lblMatQIntervalo.setDisabled(True)
        self.WMainWindow.sbIntervaloDiffCalc.setDisabled(True)
        self.WMainWindow.sbMatricesMinDiff.setDisabled(True)
        self.WMainWindow.gbCOAnimacion.setVisible(False)
        self.WMainWindow.btnGWGenerarEstados.setVisible(False)

        # Asignar shorcuts
        entrenar_shortcut = "F5"
        recorrer_shortcut = "F6"
        cancelar_shortcut = "Esc"
        self.WMainWindow.btnEntrenar.setShortcut(QtGui.QKeySequence(entrenar_shortcut))
        self.WMainWindow.btnRecorrer.setShortcut(QtGui.QKeySequence(recorrer_shortcut))
        self.WMainWindow.btnTerminarProceso.setShortcut(QtGui.QKeySequence(cancelar_shortcut))

        self.WMainWindow.btnEntrenar.setToolTip("<html><head/><body><p>\
                                                Entrenar agente \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(entrenar_shortcut))
        self.WMainWindow.btnRecorrer.setToolTip("<html><head/><body><p>\
                                                Explotar conocimiento \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(recorrer_shortcut))
        self.WMainWindow.btnTerminarProceso.setToolTip("<html><head/><body><p>\
                                                    Detener proceso \
                                                    <span style='font-size:7pt;'>\
                                                    {0}</span></p></body></html>"
                                                    .format(cancelar_shortcut))

        # Asignar shortcuts
        mostrar_mat_r_sc = "Ctrl+R"
        mostrar_mat_q_sc = "Ctrl+Q"
        self.WMainWindow.btnMostrarMatrizR.setShortcut(QtGui.QKeySequence(mostrar_mat_r_sc))
        self.WMainWindow.btnMostrarMatrizQ.setShortcut(QtGui.QKeySequence(mostrar_mat_q_sc))

        self.WMainWindow.btnMostrarMatrizR.setToolTip("<html><head/><body><p>\
                                                Mostrar matriz de recompensas \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(mostrar_mat_r_sc))
        self.WMainWindow.btnMostrarMatrizQ.setToolTip("<html><head/><body><p>\
                                                Mostrar matriz Q \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(mostrar_mat_q_sc))

        generar_estados_rnd_sc = "Ctrl+G"
        generar_estados_rnd_fast_sc = "Ctrl+Shift+G"
        self.WMainWindow.btnGWGenerarEstados.setShortcut(QtGui.QKeySequence(generar_estados_rnd_sc))
        self.WMainWindow.btnGenEstRndRapida.setShortcut(QtGui.QKeySequence(generar_estados_rnd_fast_sc))

        self.WMainWindow.btnGWGenerarEstados.setToolTip(u"<html><head/><body><p>\
                                                Generar estados aleatorios \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(generar_estados_rnd_sc))
        self.WMainWindow.btnGenEstRndRapida.setToolTip(u"<html><head/><body><p>\
                                                Generar estados y dimensión aleatorios (incluyendo al Estado Final) \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(generar_estados_rnd_fast_sc))

        self.setMouseTracking(True)

        self.generar_menu_pruebas()
        # self.generar_menu_edicion()
        # self.generar_menu_estadisticas()

        self.inicializar_todo()

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

        :param dimension: Dimensión del GridWorld.
        """
        # Desactivar la visualización de la Matriz R
        self.WMainWindow.btnMostrarMatrizR.setDisabled(True)

        # Desactiva la visualización de la Matriz Q y el Juego
        self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)
        self.WMainWindow.btnRecorrer.setDisabled(True)

        # Desactivar controles para mostrar camino optimo
        self.WMainWindow.gbCOAcciones.setDisabled(True)
        self.WMainWindow.gbCOAnimacion.setDisabled(True)

        # Obtener ancho y alto del GridWorld
        self._logger.debug("Dimensión: {0}".format(dimension))
        ancho_gw, alto_gw = self.convert_dimension(dimension)

        # Crear un nuevo GridWorld dados el ancho y el alto del mismo
        self.gridworld = GridWorld(ancho_gw,
                                   alto_gw,
                                   self.window_config["tipos_estados"],
                                   None,
                                   [TIPOESTADO.PARED]
                                   )

        self.calcular_recompensa_final()
        idx_tecnica = self.WMainWindow.cbQLTecnicas.currentIndex()
        if self.WMainWindow.cbQLTecnicas.itemData(idx_tecnica).toInt()[0] == 2:
            self.calcular_gamma_minimo()

        ancho_estado_px = self.window_config["item"]["size"]
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
        # self.WMainWindow.tblGridWorld.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.estado_final = None
        self.estado_inicial = None

        # Recargar estados del GridWorld en pantalla
        self.recargar_estados()

        self.WMainWindow.btnMostrarMatrizR.setEnabled(True)

    def _set_window_signals(self):
        u"""
        Establece las señales correspondientes a los controles
        """
        self.WMainWindow.actionAppSalir.triggered.connect(self.exit)
        # Cambia la Dimensión del GridWorld al seleccionar la dimensión en el ComboBox
        self.WMainWindow.cbGWDimension.currentIndexChanged.connect(self.set_gw_dimension_cb)
        # Cambia el Tipo de Estado al clickear un casillero del tblGridWorld
        self.WMainWindow.tblGridWorld.cellClicked[int, int].connect(self.switch_tipo_estado)
        # Empieza el Entrenamiento al clickear el btnEntrenar
        self.WMainWindow.btnEntrenar.clicked.connect(self.entrenar)
        # Interrumpe el Entrenamiento al clickear el btnTerminarTraining
        self.WMainWindow.btnTerminarProceso.clicked.connect(self.terminar_proceso)
        # Muestra sólo los parámetros utilizados en la técnica seleccionada en el ComboBox
        self.WMainWindow.cbQLTecnicas.currentIndexChanged.connect(self.parametros_segun_tecnica)
        # Al hacer clic derecho sobre un item del GridWorld
        self.WMainWindow.tblGridWorld.customContextMenuRequested.connect(self.show_item_menu)
        self.WMainWindow.btnInicializarTodo.clicked.connect(self.inicializar_todo)
        self.WMainWindow.btnRecorrer.clicked.connect(self.recorrer_gw)
        # Emite cuando se coloca el cursor del mouse sobre un ítem
        self.WMainWindow.tblGridWorld.itemEntered.connect(self.mostrar_item_actual)
        self.WMainWindow.menuGridWorld.aboutToShow.connect(self.generar_menu_dimensiones)
        self.WMainWindow.menuQLearning.aboutToShow.connect(self.generar_menu_tecnicas)
        self.WMainWindow.menuGridWorld.triggered.connect(self.set_gw_dimension_menu)
        self.WMainWindow.menuQLearning.triggered.connect(self.parametros_segun_tecnica_menu)
        self.WMainWindow.actionAcercaDe.triggered.connect(self.mostrar_dialogo_acerca)
        self.WMainWindow.btnGWGenerarEstados.clicked.connect(self.mostrar_gen_rnd_estados_dialog)
        self.WMainWindow.btnInicializarGW.clicked.connect(self.refresh_gw)
        self.WMainWindow.btnInicializarValoresQL.clicked.connect(self.inicializar_ql_vals)
        self.WMainWindow.actionInicializarTodo.triggered.connect(self.inicializar_todo)
        self.WMainWindow.btnGWOpciones.clicked.connect(self.mostrar_opciones_gw)
        self.WMainWindow.actionAgenteEntrenar.triggered.connect(self.entrenar)
        self.WMainWindow.actionAgenteRecorrer.triggered.connect(self.recorrer_gw)
        self.WMainWindow.actionAgenteCancelar.triggered.connect(self.terminar_proceso)
        self.WMainWindow.btnMostrarMatrizQ.clicked.connect(self.show_matriz_q)
        self.WMainWindow.btnMostrarMatrizR.clicked.connect(self.show_matriz_r)
        self.WMainWindow.btnCOAnimCancel.clicked.connect(self.animar_camino_optimo)
        self.WMainWindow.btnCOShowHide.clicked.connect(self.show_hide_camino_optimo)
        self.WMainWindow.btnGenEstRndRapida.clicked.connect(lambda: self.refresh_gw_random(True, True))
        self.WMainWindow.sbQLGamma.valueChanged.connect(self.calcular_recompensa_final)
        self.WMainWindow.menuEstadisticas.triggered.connect(self.show_estadisticas)
        self.WMainWindow.menuEstadisticas.aboutToShow.connect(self.generar_menu_estadisticas)
        self.WMainWindow.sbQLTau.editingFinished.connect(self.calcular_gamma_minimo)

    def parametros_segun_tecnica(self, indice):
        u"""
        Muestra u oculta los parámetros en función de la técnica seleccionada.

        :param tecnica: Técnica seleccionada
        """
        # Obtener valor asociado al item seleccionado
        key = self.WMainWindow.cbQLTecnicas.itemData(indice).toInt()[0]

        if key == 0:
            # Greedy
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setMinimum(0.00)
            self.WMainWindow.sbQLEpsilon.setValue(0.00)
            self.WMainWindow.sbQLEpsilon.setEnabled(False)
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
            self.WMainWindow.sbCantEpisodiosDec.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setEnabled(True)
        elif key == 1:
            # E-Greedy
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setMinimum(0.01)
            self.WMainWindow.sbQLEpsilon.setEnabled(True)
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
            self.WMainWindow.sbCantEpisodiosDec.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setMaximum(0.99)
            self.WMainWindow.sbDecrementoVal.setValue(0.01)
            self.WMainWindow.sbQLGamma.setMinimum(0.01)
        elif key == 2:
            # Softmax
            self.WMainWindow.lblEpsilon.hide()
            self.WMainWindow.sbQLEpsilon.hide()
            self.WMainWindow.lblTau.show()
            self.WMainWindow.sbQLTau.show()
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
            self.WMainWindow.sbCantEpisodiosDec.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setMaximum(1000000000)
            self.WMainWindow.sbDecrementoVal.setValue(20)

            # Hack para calcular el gamma mínimo de acuerdo al hardware
            self.calcular_gamma_minimo()
        elif key == 3:
            # Aleatorio
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setMinimum(1.00)
            self.WMainWindow.sbQLEpsilon.setValue(1.00)
            self.WMainWindow.sbQLEpsilon.setEnabled(False)
            self.WMainWindow.chkDecrementarParam.setDisabled(True)
            self.WMainWindow.sbCantEpisodiosDec.setDisabled(True)
            self.WMainWindow.sbDecrementoVal.setDisabled(True)

    def show_item_menu(self, posicion):
        u"""
        Muestra un menú contextual al hacer clic derecho sobre un item de la tabla

        :param posicion: Posición relativa del item clickeado
        """
        if not self.window_config["item"]["menu_estado"]["enabled"]:
            return None

        selected_items = self.WMainWindow.tblGridWorld.selectedItems()
        cant_selected = len(selected_items)

        tipos_estados = self.gridworld.tipos_estados
        item_actual = self.WMainWindow.tblGridWorld.itemAt(posicion)
        estado_actual = self.gridworld.get_estado(item_actual.row() + 1,
                                                  item_actual.column() + 1)

        # Crear menu contextual para los items de la tabla
        self.menu_item = QtGui.QMenu("Tipo de estado")
        tipos_estados_group = QtGui.QActionGroup(self.WMainWindow.tblGridWorld)
        for tipo in tipos_estados.values():
            if tipo.ide not in self.window_config["item"]["menu_estado"]["ocultar_tipos"]:

                # Verificar si el tipo de estado posee un ícono
                if tipo.icono is None:
                    action = QtGui.QAction(tipo.nombre,
                                           self.WMainWindow.tblGridWorld)
                else:
                    action = QtGui.QAction(QtGui.QIcon(tipo.icono),
                                           tipo.nombre,
                                           self.WMainWindow.tblGridWorld)

                # Asociar al texto del menu el tipo de estado correspondiente
                action.setData(tipo.ide)
                action.setActionGroup(tipos_estados_group)
                action.setCheckable(True)

                if estado_actual.tipo.ide == tipo.ide:
                    action.setChecked(True)

                action.setStatusTip("Establecer calidad de estado a {0}"
                                   .format(tipo.nombre))
                self.menu_item.addAction(action)

                if tipo.ide == TIPOESTADO.FINAL:
                    if (self.estado_final is not None) or (cant_selected > 1):
                        action.setEnabled(False)
                    else:
                        action.setEnabled(True)
                elif tipo.ide == TIPOESTADO.INICIAL:
                    if (self.estado_inicial is not None) or (cant_selected > 1):
                        action.setEnabled(False)
                    else:
                        action.setEnabled(True)

        # Mostrar el menú y obtener el item de menu clickeado
        action = self.menu_item.exec_(self.WMainWindow.tblGridWorld.mapToGlobal(posicion))

        if action is not None:
            # Cachear acceso a métodos y atributos
            gw_get_estado = self.gridworld.get_estado
            show_tooltip = self.window_config["item"]["show_tooltip"]

            for item in selected_items:
                # Obtener el tipo de estado asociado al texto clickeado
                tipo_num = action.data().toInt()[0]
                # Actualizar texto del item de la tabla en función del tipo de estado
                item.setText(tipos_estados[tipo_num].letra)
                # Establecer color de fondo de acuerdo al tipo de estado
                item.setBackgroundColor(QtGui.QColor(tipos_estados[tipo_num].color))
                item.setSelected(False)

                estado_actual = gw_get_estado(item.row() + 1,
                                              item.column() + 1)

                if tipo_num == TIPOESTADO.INICIAL:
                    self.estado_inicial = estado_actual
                elif tipo_num == TIPOESTADO.FINAL:
                    self.estado_final = estado_actual

                if estado_actual.tipo.ide == TIPOESTADO.INICIAL:
                    self.estado_inicial = None
                    self.ocultar_camino_optimo()
                    self.camino_optimo = None
                    self.WMainWindow.btnCOShowHide.setDisabled(True)
                elif estado_actual.tipo.ide == TIPOESTADO.FINAL:
                    self.estado_final = None
                    self.WMainWindow.btnRecorrer.setDisabled(True)
                    self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)

                # Establecer tipo de estado seleccionado al estado en la matriz de
                # Estados
                estado_actual.tipo = tipos_estados[tipo_num]

                if show_tooltip:
                    item.setToolTip("Fila: {0}\nColumna: {1}\nTipo: {2}\nRecompensa: {3}"
                                    .format(item.row() + 1, item.column() + 1,
                                            estado_actual.tipo.nombre,
                                            estado_actual.tipo.recompensa))

    def entrenar(self):
        u"""
        Ejecuta la magia de Q-Learning. Se encarga de realizar el aprendizaje
        mediante el mismo en otro hilo/proceso.
        """

        if self.estado_final is None:
            QtGui.QMessageBox.warning(self,
                                          _tr('QLearning - Entrenamiento'),
                                          "Debe establecer un Estado Final antes de realizar el entrenamiento.")
            return None

        if self.estado_inicial is not None:
            QtGui.QMessageBox.warning(self,
                                          _tr('QLearning - Entrenamiento'),
                                          "Quite el Estado Inicial y elija otro tipo de estado antes de realizar el entrenamiento.")
            return None

        # Bloquear GridWorld
        self.window_config["item"]["menu_estado"]["enabled"] = False
        self.window_config["item"]["show_tooltip"] = False

        # Ocultar camino antes óptimo antes de entrenar
        self.ocultar_camino_optimo()
        self.camino_optimo = None

        # Inicializar variables de gráficos
        self.graph_episodios_finalizados = None
        self.graph_recompensas_promedio = None
        self.graph_mat_diff = None
        # self.graph_iters_por_episodio = None

        # Parámetros para mostrar el estado actual en pantalla
        self.ent_warn_loop_alarm = self.window_config["gw"]["entrenamiento"]["maxitersreached"]["warn"]
        self.ent_show_estado_act = self.window_config["gw"]["entrenamiento"]["actual_state"]["show"]
        self.ent_color_estado_act = QtGui.QColor(self.window_config["gw"]["entrenamiento"]["actual_state"]["color"])
        self.ent_icon_estado_act = self.window_config["gw"]["entrenamiento"]["actual_state"]["icono"]
        self.ent_null_icon = QtGui.QIcon()

        # ----------- Comienzo de seteo de la técnica --------------
        # Obtener la información asociada al ítem actual del combobox
        item_data = self.WMainWindow.cbQLTecnicas.itemData(self.WMainWindow.cbQLTecnicas.currentIndex())
        # Obtener el índice propio de la técnica a utilizar
        id_tecnica = item_data.toInt()[0]
        tecnica = self.tecnicas[id_tecnica]

        if id_tecnica == 0:
            # Greedy
            tecnica = Greedy
        elif id_tecnica == 1:
            # E-Greedy
            parametro = self.WMainWindow.sbQLEpsilon.value()
            tecnica = EGreedy
        elif id_tecnica == 2:
            # Softmax
            parametro = self.WMainWindow.sbQLTau.value()
            tecnica = Softmax
        elif id_tecnica == 3:
            # Aleatorio
            tecnica = Aleatorio
            parametro = None
        else:
            tecnica = None

        if self.WMainWindow.chkDecrementarParam.isChecked():
                paso_decremento = self.WMainWindow.sbDecrementoVal.value()
                intervalo_decremento = self.WMainWindow.sbCantEpisodiosDec.value()
        else:
            paso_decremento = 0
            intervalo_decremento = 0
        # ----------- Fin de seteo de la técnica --------------

        # Obtener parámetro Gamma
        gamma = self.WMainWindow.sbQLGamma.value()
        # Obtener cantidad de episodios a ejecutar
        cant_episodios = int(self.WMainWindow.sbCantidadEpisodios.value())

        # Establecer valor inicial a cargar en Matriz Q
        if self.WMainWindow.optMQInitEnCero.isChecked():
            init_value_fn = 0
        elif self.WMainWindow.optMQInitValOptimistas.isChecked():
            incremento = self.WMainWindow.sbValOptimoIncremento.value()
            max_recomp = self.window_config["tipos_estados"][TIPOESTADO.FINAL].recompensa
            init_value_fn = max_recomp + incremento
        else:
            init_value_fn = 0

        # Determina si utilizar el limitador de iteraciones o no
        limitar_nro_iteraciones = self.WMainWindow.chkLimitarCantIteraciones.isChecked()
        # Número máximo de iteraciones por episodio
        cant_max_iter = self.WMainWindow.sbCantMaxIteraciones.value()

        # Determinar si la diferencia de matrices se encuentra activa
        matdiff_status = self.WMainWindow.chkQLCalcularMatDiff.isChecked()

        # Diferencia mínima entre matrices para finalizar el entranamiento
        matriz_min_diff = self.WMainWindow.sbMatricesMinDiff.value()
        # Intervalo de episodios entre cálculos de diferencia entre matrices
        intervalo_diff_calc = self.WMainWindow.sbIntervaloDiffCalc.value()

        cant_max_iter_gral = 50000
        stop_action = self.window_config["gw"]["entrenamiento"]["maxitersreached"]["action"]

        # Crear una nueva instancia de Q-Learning
        self.qlearning = QLearning(self.gridworld,
                                   gamma,
                                   (tecnica, parametro, paso_decremento, intervalo_decremento),
                                   cant_episodios,
                                   (limitar_nro_iteraciones, cant_max_iter),
                                   init_value_fn,
                                   (matdiff_status, matriz_min_diff, intervalo_diff_calc),
                                   (cant_max_iter_gral, stop_action),
                                   None)

        # QLearningEntrenarWorker Management
        # Que empiece la magia
        self.ql_entrenar_out_q = multiprocessing.Queue()
        self.ql_entrenar_error_q = multiprocessing.Queue()

        self.qlearning_entrenar_worker = self.qlearning.entrenar(self.ql_entrenar_out_q,
                                                                 self.ql_entrenar_error_q)

        self._logger.debug("Nuevo Thread: {0}".format(self.qlearning_entrenar_worker))

        worker_error = get_item_from_queue(self.ql_entrenar_error_q)

        if worker_error is not None:
            self._logger.debug("Error {0}: ".format(worker_error))
            self.qlearning_entrenar_worker = None
            self.working_process = None
            self.ql_entrenar_out_q = None
            self.ql_entrenar_error_q = None

        if self.qlearning_entrenar_worker is not None:
            self.working_process = self.qlearning_entrenar_worker
            self.entrenar_is_running = True

            self._parametros = (gamma,
                                (id_tecnica, parametro, paso_decremento, intervalo_decremento),
                                cant_episodios,
                                (limitar_nro_iteraciones, cant_max_iter),
                                init_value_fn
                                )

            self.on_comienzo_proceso()

    def recorrer_gw(self):
        u"""
        Realiza el recorrido del agente en el GridWorld buscando los valores de
        Q mayores.
        """
        if self.estado_final is None:
            QtGui.QMessageBox.warning(self,
                                      tr('QLearning - Recorrido'),
                                      "Debe establecer un Estado Final antes de realizar el recorrido.")
            return None

        if self.estado_inicial is None:
            QtGui.QMessageBox.warning(self,
                                      _tr('QLearning - Recorrido'),
                                      "Debe establecer un Estado Inicial antes de realizar el recorrido.")
            return None

        # Ocultar camino óptimo antes de jugar
        self.ocultar_camino_optimo()
        self.camino_optimo = None

        # Parámetros para mostrar el estado actual en pantalla
        self.rec_show_estado_act = self.window_config["gw"]["recorrido"]["actual_state"]["show"]
        self.rec_color_estado_act = QtGui.QColor(self.window_config["gw"]["recorrido"]["actual_state"]["color"])
        self.rec_icon_estado_act = self.window_config["gw"]["recorrido"]["actual_state"]["icono"]
        self.rec_null_icon = QtGui.QIcon()

        # Crear colas para comunicarse con el proceso
        self.ql_recorrer_out_q = multiprocessing.Queue()
        self.ql_recorrer_error_q = multiprocessing.Queue()

        estado_inicial = (self.estado_inicial.fila,
                          self.estado_inicial.columna)

        self.qlearning_recorrer_worker = self.qlearning.recorrer(self.matriz_q,
                                                                 self.mat_est_acc,
                                                                 estado_inicial,
                                                                 self.ql_recorrer_out_q,
                                                                 self.ql_recorrer_error_q)

        self._logger.debug("Nuevo Thread: {0}".format(self.qlearning_recorrer_worker))

        worker_error = get_item_from_queue(self.ql_recorrer_error_q)
        if worker_error is not None:
            self._logger.debug("Error {0}: ".format(worker_error))
            self.qlearning_recorrer_worker = None
            self.working_process = None
            self.ql_recorrer_out_q = None
            self.ql_recorrer_error_q = None

        if self.qlearning_recorrer_worker is not None:
            self.recorrer_is_running = True
            self.working_process = self.qlearning_recorrer_worker

            self.on_comienzo_proceso()

    def terminar_proceso(self):
        u"""
        Ejecutar tareas al finalizar un thread.
        """
        if self.working_process is not None:
            self._logger.debug("Detener {0}".format(self.working_process))
            self.working_process.join(0.05)
            self._logger.debug(self.working_process)
            self.working_process = None

            if self.wnd_timer is not None:
                self.on_fin_proceso()

            self.worker_msg_out_q = None

    def switch_tipo_estado(self, fila, columna):
        """
        Rota a través de los distintos tipos de estados y los cambia acorde en
        la UI.

        :param fila: Fila del ítem.
        :param columna: Columna del ítem.
        """
        # TODO: Cambiar tipo de estado al ir haciendo clic sobre el estado
        tipos_estados = self.gridworld.tipos_estados.keys()

    def _on_window_timer(self):
        u"""
        Ejecuta diversas acciones a cada disparo del Timer principal.
        """
        # self._logger.debug("Timer Timeout")
        self.actualizar_window()
        self.comprobar_actividad_procesos()

    def on_comienzo_proceso(self):
        u"""
        Ejecutar tareas al ejecutar un thread.
        """
        self._logger.debug("Comienzo del proceso")
        # Crear Timer asociado a la ventana principal
        self.wnd_timer = QtCore.QTimer(self)
        # Conectar disparo de timer con método
        self.wnd_timer.timeout.connect(self._on_window_timer)
        self.wnd_timer.start(15)

        # Desactivar seguimiento del mouse antes de comenzar
        self.setMouseTracking(False)
        self.WMainWindow.tblGridWorld.setMouseTracking(False)

        # Mostrar cursor de ocupado indicando que se está procesando
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))

        if self.entrenar_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Entrenando agente..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.entrenar_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.entrenar_is_running)
            self.WMainWindow.actionAgenteEntrenar.setDisabled(self.entrenar_is_running)
            self.WMainWindow.actionAgenteRecorrer.setDisabled(self.entrenar_is_running)

            self.WMainWindow.lblEntEstadoActual.setText("-")
            self.WMainWindow.lblEntExecTimeEpisodios.setText("-")
            self.WMainWindow.lblEntExecTimeIteraciones.setText("-")
            self.WMainWindow.lblEntExecTimeTotal.setText("-")
            self.WMainWindow.lblEntNroEpisodio.setText("-")
            self.WMainWindow.lblEntNroIteracion.setText("-")
            self.WMainWindow.lblEntValParametro.setText("-")
            self.WMainWindow.lblEntDiffMatrices.setText("-")

            self.WMainWindow.lblRecEstadoActual.setText("-")
            self.WMainWindow.lblRecExecTimeRecorrido.setText("-")
            self.WMainWindow.lblRecExecTimeTotal.setText("-")

            self._ent_progress_bar.setVisible(True)
            cant_episodios = self.WMainWindow.sbCantidadEpisodios.value()
            self._ent_progress_bar.setMaximum(cant_episodios)
            self._ent_progress_bar.setValue(0)

        if self.recorrer_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Agente buscando camino óptimo..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.recorrer_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.recorrer_is_running)
            self.WMainWindow.actionAgenteEntrenar.setDisabled(self.recorrer_is_running)
            self.WMainWindow.actionAgenteRecorrer.setDisabled(self.recorrer_is_running)

            self.WMainWindow.lblRecEstadoActual.setText("-")
            self.WMainWindow.lblRecExecTimeRecorrido.setText("-")
            self.WMainWindow.lblRecExecTimeTotal.setText("-")

        self.WMainWindow.btnTerminarProceso.setEnabled(True)
        self.WMainWindow.gbGridWorld.setDisabled(True)
        self.WMainWindow.gbQLearning.setDisabled(True)
        self.WMainWindow.gbGeneral.setDisabled(True)
        self.WMainWindow.gbMatrices.setDisabled(True)
        self.WMainWindow.gbCOAcciones.setDisabled(True)
        self.WMainWindow.gbCOAnimacion.setDisabled(True)
        self.WMainWindow.menuConfiguracion.setDisabled(True)
        self.WMainWindow.menuPruebas.setDisabled(True)
        self.WMainWindow.menuEstadisticas.setDisabled(True)

        try:
            self.wnd_taskbar = taskbar.WindowsTaskBar()
            self.wnd_taskbar.HrInit()
            self.wnd_taskbar.SetProgressState(self.winId(),
                                              self.wnd_taskbar.TBPF_INDETERMINATE)
        except RuntimeError:
            pass

    def on_fin_proceso(self):
        u"""
        Ejecuta tareas al finalizar la ejecución de un thread/proceso.
        """
        # Detener Timer asociado a la ventana principal
        self.wnd_timer.stop()

        # Habilitar GridWorld
        self.window_config["item"]["menu_estado"]["enabled"] = True
        self.window_config["item"]["show_tooltip"] = True

        self._logger.debug("Procesos hijos activos: {0}\nFin de procesamiento"
            .format(multiprocessing.active_children()))

        self.WMainWindow.gbGridWorld.setEnabled(True)
        self.WMainWindow.gbQLearning.setEnabled(True)
        self.WMainWindow.gbGeneral.setEnabled(True)
        self.WMainWindow.gbMatrices.setEnabled(True)
        self.WMainWindow.menuConfiguracion.setEnabled(True)
        self.WMainWindow.menuPruebas.setEnabled(True)
        self.WMainWindow.menuEstadisticas.setEnabled(True)

        if self.entrenar_is_running:
            self.entrenar_is_running = False
            self.WMainWindow.btnEntrenar.setEnabled(True)
            self.WMainWindow.actionAgenteEntrenar.setEnabled(True)
            self.WMainWindow.statusBar.showMessage(_tr("Ha finalizado el entrenamiento."), 2000)

            test_matriz_q = self.matriz_q is not None
            self.WMainWindow.btnRecorrer.setEnabled(test_matriz_q)
            self.WMainWindow.actionAgenteRecorrer.setEnabled(test_matriz_q)
            self.WMainWindow.btnMostrarMatrizQ.setEnabled(test_matriz_q)

        if self.recorrer_is_running:
            self.recorrer_is_running = False
            self.WMainWindow.btnEntrenar.setEnabled(True)
            self.WMainWindow.actionAgenteEntrenar.setEnabled(True)
            self.WMainWindow.btnRecorrer.setEnabled(True)
            self.WMainWindow.actionAgenteRecorrer.setEnabled(True)
            self.WMainWindow.gbCOAcciones.setEnabled(True)
            self.WMainWindow.gbCOAnimacion.setEnabled(True)
            self.WMainWindow.statusBar.showMessage(_tr("Ha finalizado la búsqueda del camino óptimo."), 2000)

        self.WMainWindow.btnTerminarProceso.setEnabled(False)
        # self.WMainWindow.statusBar.clearMessage()
        self.WMainWindow.btnMostrarMatrizR.setEnabled(True)

        # Restaurar color original del estado final
        try:
            self.last_state_bkp.setBackground(QtGui.QBrush(self.last_state_bg))
            self.last_state_bkp.setText(self.last_state_text)
            self.last_state_bkp.setIcon(QtGui.QIcon())
            self.ent_color_estado_act = None
            self.ent_icon_estado_act = None
            self.ent_show_estado_act = None
            self.rec_color_estado_act = None
            self.rec_icon_estado_act = None
            self.rec_show_estado_act = None
        except AttributeError:
            pass
        except TypeError:
            pass

        self.last_state_bkp = None
        self.last_state_bg = None

        try:
            self.wnd_taskbar.SetProgressState(self.winId(),
                                              self.wnd_taskbar.TBPF_NOPROGRESS)
        except RuntimeError:
            pass

        # Mostrar camino óptimo
        if self.camino_optimo is not None:
            self.mostrar_camino_optimo_act()

        # Ocultar barra de progreso
        self._ent_progress_bar.setVisible(False)

        # Restaurar cursor normal
        QtGui.QApplication.restoreOverrideCursor()

        # Reactivar seguimiento del mouse en widgets
        self.setMouseTracking(True)
        self.WMainWindow.tblGridWorld.setMouseTracking(True)

        # FIXME: Eliminar
        # self._logger.debug("Matriz Recompensas Promedio: {0}".format(self.graph_recompensas_promedio))
        # self._logger.debug("Episodios Finalizados: {0}".format(self.graph_episodios_finalizados))
        # self._logger.debug("Iteraciones Por Episodio: {0}".format(self.graph_iters_por_episodio))
        # self._logger.debug("Diferencia entre matrices: {0}".format(self.graph_mat_diff))

    def _reintentar_detener_hilos(self):
        u"""
        Solicita la finalización de todos los threads utilizados en la
        aplicación. Este método debe ser llamado al desconectarse o al salir
        de la aplicación.
        """
        active_children = multiprocessing.active_children()

        for proceso in active_children:
            try:
                # Darle una oportunidad más al proceso de terminar
                proceso.join(0.05)
                # Esperar a que termine
                time.sleep(0.1)
                # Forzar terminación de proceso
                proceso.terminate()
                # Esperar antes de continuar
                time.sleep(0.1)
            except WindowsError:
                pass

    def inicializar_todo(self):
        u"""
        Reestablece los valores por defecto de varios controles de la UI
        e inicializa variables internas del programa.
        """
        # self.WMainWindow.cbGWDimension.currentIndexChanged.disconnect(self.set_gw_dimension_cb)
        self._init_vars()
        self.inicializar_ql_vals()
        self.inicializar_gw()

    def mostrar_dialogo_acerca(self):
        u"""
        Muestra el cuadro de diálogo Acerca de...
        """
        self.AboutD = AboutDialog(self)
        self.AboutD.show()

    def closeEvent(self, event):
        """
        Reimplementa el evento 'closeEvent' de la clase padre.

        :param event: Evento.
        """
        self._reintentar_detener_hilos()
        logging.shutdown()

    def exit(self):
        u"""
        Finaliza la ejecución de la aplicación.
        """
        self.close()

    def actualizar_window(self):
        u"""
        Actualiza la información mostrada en la ventana de acuerdo a los
        datos de entrada,
        """
        self.update_window_entrenar()
        self.update_window_recorrer()

    def update_window_entrenar(self):
        u"""
        Actualizar ventana con información del Entrenamiento
        """
        try:
            # Cachear acceso a métodos y atributos
            main_wnd = self.WMainWindow
            ent_progress_bar = self._ent_progress_bar
            ent_show_estado_act = self.ent_show_estado_act
            ent_warn_loop_alarm = self.ent_warn_loop_alarm
            # last_state_bkp = self.last_state_bkp
            # ent_null_icon = self.ent_null_icon
            # last_state_bg = self.last_state_bg
            # last_state_text = self.last_state_text
            # ent_icon_estado_act = self.ent_icon_estado_act
            # ent_color_estado_act = self.ent_color_estado_act

            data_entrenar = self.get_all_from_queue(self.ql_entrenar_out_q)

            for ql_ent_info in data_entrenar:
                estado_actual_ent = ql_ent_info.get('EstadoActual')
                nro_episodio = ql_ent_info.get('NroEpisodio')
                cant_iteraciones = ql_ent_info.get('NroIteracion')
                episode_exec_time = ql_ent_info.get('EpisodiosExecTime', 0.0)
                iter_exec_time = ql_ent_info.get('IteracionesExecTime', 0.0)
                worker_joined = ql_ent_info.get('ProcesoJoined')
                loop_alarm_pack = ql_ent_info.get('LoopAlarm', (False, -1))
                matriz_q = ql_ent_info.get('MatrizQ')
                valor_parametro = ql_ent_info.get('ValorParametro')
                running_exec_time_ent = ql_ent_info.get('RunningExecTime', 0.0)
                tmp_mat_diff = ql_ent_info.get('MatDiff')
                corte_iteracion = ql_ent_info.get('CorteIteracion')
                mat_est_acc = ql_ent_info.get('MatEstAcc')

                # Información estadística
                graph_recompensas_promedio = ql_ent_info.get('MatRecompProm')
                graph_episodios_finalizados = ql_ent_info.get('EpFinalizados')
                # graph_iters_por_episodio = ql_ent_info.get('ItersXEpisodio')
                graph_mat_diff = ql_ent_info.get('MatDiffStat')

                self.graph_episodios_finalizados = graph_episodios_finalizados
                self.graph_recompensas_promedio = graph_recompensas_promedio
                self.graph_mat_diff = graph_mat_diff
                # self.graph_iters_por_episodio = graph_iters_por_episodio
                self.matriz_q = matriz_q
                self.mat_est_acc = mat_est_acc

                ent_loop_alarm, ent_stop_action = loop_alarm_pack

                try:
                    # Descomponer coordenadas de estado actual
                    x_actual, y_actual = estado_actual_ent

                    # Mostrar información de entrenamiento en etiquetas
                    main_wnd.lblEntEstadoActual.setText("X:{0}  Y:{1}".format(x_actual,  # @IgnorePep8
                                                                              y_actual))  # @IgnorePep8
                    main_wnd.lblEntNroEpisodio.setText(str(nro_episodio))
                    main_wnd.lblEntNroIteracion.setText(str(cant_iteraciones))
                    main_wnd.lblEntValParametro.setText("{0:.2f}".format(valor_parametro))  # @IgnorePep8
                    main_wnd.lblEntExecTimeEpisodios.setText("{0:.3f} seg  ({1:.2f} ms)".format(episode_exec_time,  # @IgnorePep8
                                                                                                episode_exec_time * 1000))  # @IgnorePep8
                    main_wnd.lblEntExecTimeIteraciones.setText("{0:.3f} seg  ({1:.2f} ms)".format(iter_exec_time,  # @IgnorePep8
                                                                                                  iter_exec_time * 1000))  # @IgnorePep8
                    main_wnd.lblEntExecTimeTotal.setText("{0:.3f} seg  ({1:.2f} ms)".format(running_exec_time_ent,  # @IgnorePep8
                                                                                            running_exec_time_ent * 1000))  # @IgnorePep8
                    main_wnd.lblEntDiffMatrices.setText(str(tmp_mat_diff))

                    ent_progress_bar.setValue(nro_episodio)
                except TypeError:
                    pass
                except ValueError:
                    pass

                # Mostrar estado actual en grilla
                if ent_show_estado_act:
                    try:
                        item = main_wnd.tblGridWorld.item(x_actual - 1,
                                                          y_actual - 1)
                    except TypeError:
                        pass
                    except UnboundLocalError:
                        pass

                    try:
                        self.last_state_bkp.setIcon(self.ent_null_icon)
                        self.last_state_bkp.setBackground(self.last_state_bg)
                        self.last_state_bkp.setText(self.last_state_text)
                    except AttributeError:
                        pass
                    finally:
                        self.last_state_bkp = item
                        self.last_state_text = item.text()
                        self.last_state_bg = item.background()

                    try:
                        item.setText("")
                        item.setIcon(self.ent_icon_estado_act)
                    except TypeError:
                        try:
                            item.setBackground(self.ent_color_estado_act)
                        except TypeError:
                            pass

                if ent_loop_alarm:
                    if ent_warn_loop_alarm:
                        QtGui.QMessageBox.warning(self,
                                                  _tr('QLearning - Entrenamiento'),
                        u"Se ha detectado que el Estado Final se encuentra bloqueado por lo que se cancelará el entrenamiento.")

                    # self.working_process.join(0.05)
                    # self.qlearning_entrenar_worker = None
                    # self.working_process = None
                    # self.ql_entrenar_error_q = None
                    # self.ql_entrenar_out_q = None
                    # self.on_fin_proceso()
        except Queue.Empty:
            pass
        except AttributeError:
            pass

    def update_window_recorrer(self):
        u"""
        Actualizar ventana con información del Recorrido
        """
        try:
            # Cachear acceso al objeto WMainWindow
            main_wnd = self.WMainWindow
            rec_show_est_act = self.rec_show_estado_act

            data_recorrer = self.get_all_from_queue(self.ql_recorrer_out_q)

            for ql_rec_info in data_recorrer:
                estado_actual_rec = ql_rec_info.get('EstadoActual')
                camino_optimo = ql_rec_info.get('CaminoRecorrido')
                running_exec_time_rec = ql_rec_info.get('RunningExecTime', 0.0)
                worker_joined = ql_rec_info.get('ProcesoJoined')
                rec_exec_time = ql_rec_info.get('RecorridoExecTime', 0.0)
                nro_iteracion = ql_rec_info.get('NroIteracion')

                self.camino_optimo = camino_optimo

                try:
                    # Descomponer coordenadas de estado actual
                    x_actual, y_actual = estado_actual_rec
                    # self._logger.debug("Estado actual: {0}".format(estado_actual_rec))

                    main_wnd.lblRecEstadoActual.setText("X:{0}  Y:{1}".format(x_actual, y_actual))  # @IgnorePep8
                    main_wnd.lblRecExecTimeTotal.setText("{0:.3f} seg  ({1:.2f} ms)".format(running_exec_time_rec,  # @IgnorePep8
                                                                                            running_exec_time_rec * 1000))  # @IgnorePep8
                    main_wnd.lblRecExecTimeRecorrido.setText("{0:.3f} seg  ({1:.2f} ms)".format(rec_exec_time,  # @IgnorePep8
                                                                                                rec_exec_time * 1000))  # @IgnorePep8
                except TypeError:
                    pass
                except ValueError:
                    pass

                # Mostrar estado actual en grilla
                if rec_show_est_act:
                    try:
                        item = main_wnd.tblGridWorld.item(x_actual - 1,
                                                          y_actual - 1)
                    except TypeError:
                        pass

                    try:
                        self.last_state_bkp.setIcon(self.rec_null_icon)
                        self.last_state_bkp.setBackground(self.last_state_bg)
                        self.last_state_bkp.setText(self.last_state_text)
                    except AttributeError:
                        pass
                    finally:
                        self.last_state_bkp = item
                        self.last_state_text = item.text()
                        self.last_state_bg = item.background()

                    try:
                        item.setText("")
                        item.setIcon(self.rec_icon_estado_act)
                    except TypeError:
                        item.setBackground(self.rec_color_estado_act)
        except Queue.Empty:
            pass
        except AttributeError:
            pass

    def get_all_from_queue(self, cola):
        u"""Generator to yield one after the others all items
            currently in the queue Q, without any waiting.
            Grupo Nº 1 wants to thanks to Eli Bendersky for the idea.

            :param cola: Cola de entrada
        """
        try:
            while 1:
                yield cola.get_nowait()
        except Queue.Empty:
            raise StopIteration

    def comprobar_actividad_procesos(self):
        u"""
        Comprueba si hay threads activos (sin incluir el MainThread). Si no
        existen threads activos se detiene el Timer de la ventana.
        """
        # self._logger.debug("Comprobar actividad de procesos")

        active_children = multiprocessing.active_children()

        for proceso in active_children:
            if not proceso.is_alive():
                proceso.join(0.05)
            # self._logger.debug("Proceso hijo: {0}".format(proceso))

        if not active_children:
            self.on_fin_proceso()

    def mostrar_item_actual(self, item):
        u"""
        Muestra en la barra de estado las coordenadas del ítem sobre el
        cual el cursor se encuentra arriba.

        :param item: Item debajo del cursor.
        """
        self.lbl_item_actual.setText("Fila: {0} Columna: {1}"
                                    .format(item.row() + 1,
                                            item.column() + 1))

    def mouseMoveEvent(self, event):
        u"""
        Sobrecarga del evento mouseMoveEvent de Qt.

        :param event: Evento.
        """
        self.lbl_item_actual.setText("")

    def enterEvent(self, event):
        u"""
        Sobrecarga del evento enterEvent de Qt.

        :param event: Evento.
        """
        self.lbl_item_actual.setText("")

    def set_gw_dimension_menu(self, action):
        u"""
        Establece la dimensión del GridWorld en función del ítem seleccionado en el menú.

        :param action: Acción seleccionada.
        """
        dimension = action.data().toString()
        self._logger.debug("Dimensión: {0}".format(dimension))
        indice = self.WMainWindow.cbGWDimension.findData(dimension)
        self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
        self.set_gw_dimension(dimension)

    def set_gw_dimension_cb(self, indice):
        u"""
        Establece la dimensión del GridWorld en función del ítem seleccionado en el combobox.

        :param indice: Ítem seleccionado.
        """
        dimension = self.WMainWindow.cbGWDimension.itemData(indice).toString()
        self._logger.debug("Dimensión: {0}".format(dimension))
        self.set_gw_dimension(dimension)

    def parametros_segun_tecnica_menu(self, action):
        u"""
        Establecer técnica seleccionada de acuerdo al ítem seleccionado en el menú.

        :param action: Acción seleccionada.
        """
        indice = action.data().toInt()[0]
        self.WMainWindow.cbQLTecnicas.setCurrentIndex(indice)

    def generar_menu_dimensiones(self):
        u"""
        Crea el menú Dimensiones junto a sus submenúes y acciones.
        """
        self._logger.debug("Generar Menú Dimensiones")
        dim_idx = self.WMainWindow.cbGWDimension.currentIndex()
        dim_data = self.WMainWindow.cbGWDimension.itemData(dim_idx).toString()

        self.WMainWindow.menuGridWorld.clear()

        # Cargar dimensiones posibles del tblGridWorld en el menú
        submenu_dimension = QtGui.QMenu(_tr("Dimensiones"), self)
        dimension_group = QtGui.QActionGroup(self)
        for dimension in self.gw_dimensiones:
            action = QtGui.QAction(_tr(dimension), self)
            action.setData(dimension)
            action.setCheckable(True)
            action.setActionGroup(dimension_group)
            submenu_dimension.addAction(action)

            if dimension == dim_data:
                action.setChecked(True)

        self.WMainWindow.menuGridWorld.addMenu(submenu_dimension)

    def generar_menu_tecnicas(self):
        u"""
        Crea el menú Técnicas junto a sus acciones.
        """
        self._logger.debug("Generar Menú Técnicas")
        dim_idx = self.WMainWindow.cbQLTecnicas.currentIndex()
        dim_data = self.WMainWindow.cbQLTecnicas.itemData(dim_idx).toInt()[0]

        self.WMainWindow.menuQLearning.clear()

        # Cargar dimensiones posibles del tblGridWorld en el menú
        submenu_tecnica = QtGui.QMenu(_tr("Técnicas"), self)
        tecnica_group = QtGui.QActionGroup(self)
        for key, value in self.tecnicas.items():
            action = QtGui.QAction(_tr(value), self)
            action.setData(key)
            action.setCheckable(True)
            action.setActionGroup(tecnica_group)
            submenu_tecnica.addAction(action)

            if key == dim_data:
                action.setChecked(True)

        self.WMainWindow.menuQLearning.addMenu(submenu_tecnica)

    def mostrar_opciones_gw(self):
        u"""
        Despliega un cuadro de diálogo conteniendo opciones configurables del GridWorld.
        """
        # Inicializar cuadros de diálogo
        self.GWOpcionesD = GWOpcionesDialog(self, self.window_config)

        if self.GWOpcionesD.exec_():
            if self.GWOpcionesD.ent_show_state:
                if self.GWOpcionesD.ent_usar_color_fondo:
                    ent_bg_color = self.GWOpcionesD.ent_state_bg
                    self.window_config["gw"]["entrenamiento"]["actual_state"]["color"] = ent_bg_color
                    self.window_config["gw"]["entrenamiento"]["actual_state"]["icono"] = None
                elif self.GWOpcionesD.ent_usar_icono:
                    icono_agente = self.gridworld.tipos_estados[TIPOESTADO.AGENTE].icono
                    self.window_config["gw"]["entrenamiento"]["actual_state"]["icono"] = icono_agente
            self.window_config["gw"]["entrenamiento"]["actual_state"]["show"] = self.GWOpcionesD.ent_show_state

            if self.GWOpcionesD.rec_show_state:
                if self.GWOpcionesD.rec_usar_color_fondo:
                    rec_bg_color = self.GWOpcionesD.rec_state_bg
                    self.window_config["gw"]["recorrido"]["actual_state"]["color"] = rec_bg_color
                    self.window_config["gw"]["recorrido"]["actual_state"]["icono"] = None
                elif self.GWOpcionesD.rec_usar_icono:
                    icono_agente = self.gridworld.tipos_estados[TIPOESTADO.AGENTE].icono
                    self.window_config["gw"]["recorrido"]["actual_state"]["icono"] = icono_agente
            self.window_config["gw"]["recorrido"]["actual_state"]["show"] = self.GWOpcionesD.rec_show_state

            self.window_config["item"]["size"] = self.GWOpcionesD.estado_size

            # Actualizar tipos de estados
            self.gridworld.tipos_estados = self.GWOpcionesD.tipos_estados
            self.window_config["tipos_estados"] = self.GWOpcionesD.tipos_estados

            self.recargar_estados()

    def mostrar_gen_rnd_estados_dialog(self):
        u"""
        Despliega un cuadro de diálogo que permite seleccionar valores para generar estados aleatorios.

        TODO: NotYetImplemented
        """
        self.GWGenRndEstValsD = GWGenRndEstadosDialog(self)
        if self.GWGenRndEstValsD.exec_():
            pass

    def inicializar_gw(self):
        u"""
        Inicializa el GridWorld con tipos de estados por defecto y lo actualiza.
        """
        # Cargar dimensiones posibles del GridWorld
        try:
            self.WMainWindow.cbGWDimension.currentIndexChanged.disconnect()
        except Exception:
            pass

        self.WMainWindow.cbGWDimension.clear()

        # Cachear acceso a métodos y atributos
        gw_dimension_additem = self.WMainWindow.cbGWDimension.addItem

        for dimension in self.gw_dimensiones:
            gw_dimension_additem(_tr(dimension), dimension)

        self.WMainWindow.cbGWDimension.currentIndexChanged.connect(self.set_gw_dimension_cb)

        self.estado_final = None
        self.estado_inicial = None

        self.refresh_gw()

    def refresh_gw(self):
        u"""
        Actualizar estados del GridWorld.
        """
        indice = self.WMainWindow.cbGWDimension.currentIndex()
        self.set_gw_dimension(self.WMainWindow.cbGWDimension.itemData(indice).toString())
        self.WMainWindow.btnRecorrer.setDisabled(True)
        self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)

    def inicializar_ql_vals(self):
        u"""
        Inicializa los valores de Q-Learning a valores predeterminados
        """
        # Cargar técnicas posibles
        self.WMainWindow.cbQLTecnicas.clear()
        for key, value in self.tecnicas.items():
            self.WMainWindow.cbQLTecnicas.addItem(_tr(value), key)

        # self.WMainWindow.cbQLTecnicas.setCurrentIndex(1)
        self.WMainWindow.sbQLEpsilon.setMinimum(0.01)
        self.WMainWindow.sbQLTau.setMinimum(0.01)
        self.WMainWindow.lblTau.hide()
        self.WMainWindow.sbQLTau.hide()

        # Establecer cantidad de episodios por defecto
        self.WMainWindow.sbCantidadEpisodios.setValue(400)

        # Establecer por defecto un Epsilon = 0.01
        self.WMainWindow.sbQLEpsilon.setValue(0.01)

        # Establecer por defecto un Gamma = 0.9
        self.WMainWindow.sbQLGamma.setValue(0.9)

        self.WMainWindow.sbDecrementoVal.setValue(0.01)
        self.WMainWindow.sbCantEpisodiosDec.setValue(1)
        self.WMainWindow.sbCantEpisodiosDec.setSuffix(_tr(" episodios"))
        self.WMainWindow.chkDecrementarParam.setChecked(False)
        self.WMainWindow.sbDecrementoVal.setDisabled(True)
        self.WMainWindow.sbCantEpisodiosDec.setDisabled(True)
        self.WMainWindow.sbQLTau.setValue(10)
        self.WMainWindow.sbIntervaloDiffCalc.setSuffix(_tr(" episodios"))
        self.WMainWindow.sbCantMaxIteraciones.setValue(200)
        self.WMainWindow.sbIntervaloDiffCalc.setMinimum(2)
        self.WMainWindow.sbValOptimoIncremento.setValue(500)
        self.WMainWindow.sbMatricesMinDiff.setValue(0.000001)

        self.WMainWindow.optMQInitValOptimistas.setChecked(True)

        self.WMainWindow.sbCOAnimDelay.setSuffix(_tr(" seg"))
        self.WMainWindow.sbCOAnimDelay.setValue(1)

        enable_controls = self.WMainWindow.optMQInitValOptimistas.isChecked()
        self.WMainWindow.sbValOptimoIncremento.setEnabled(enable_controls)
        self.WMainWindow.lblMQFormula.setEnabled(enable_controls)
        self.set_minimo_incremento_opt()

    def show_matriz_dialog(self, matriz, titulo_corto, titulo_largo):
        u"""
        Muestra un cuadro de diálogo conteniendo una matriz dada.

        :param matriz: Matriz a representar en el cuadro de diálogo.
        :param titulo_corto: Texto a mostrar en el título del cuadro.
        :param titulo_largo: Texto a mostrar en el cuerpo del cuadro.
        """
        ShowMatrizD = ShowMatrizDialog(matriz,
                                       titulo_corto,
                                       titulo_largo,
                                       self)
        ShowMatrizD.exec_()

    def show_matriz_r(self):
        u"""
        Muestra un cuadro de diálogo conteniendo la Matriz de Recompensas R.
        """
        matriz_r = self.gridworld.get_matriz_r()
        self.show_matriz_dialog(matriz_r, "Matriz R", "Matriz de recompensas")

    def show_matriz_q(self):
        u"""
        Muestra un cuadro de diálogo conteniendo la Matriz Q.
        """
        if self.matriz_q is not None:
            self.show_matriz_dialog(self.matriz_q, "Matriz Q", "Matriz Q")

    def resize_gw_estados(self):
        u"""
        Redimensiona el tamaño de los estados en UI de acuerdo a lo configurado.
        """
        ancho_estado_px = self.window_config["item"]["size"]
        ancho_gw_px = ancho_estado_px * self.gridworld.ancho

        self.WMainWindow.tblGridWorld.horizontalHeader().setDefaultSectionSize(ancho_estado_px)
        self.WMainWindow.tblGridWorld.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.WMainWindow.tblGridWorld.verticalHeader().setDefaultSectionSize(ancho_estado_px)
        self.WMainWindow.tblGridWorld.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        ancho_contenedor = ancho_gw_px + self.WMainWindow.tblGridWorld.verticalHeader().width() + 1
        alto_contenedor = ancho_gw_px + self.WMainWindow.tblGridWorld.horizontalHeader().height() + 1
        self.WMainWindow.tblGridWorld.setFixedSize(ancho_contenedor, alto_contenedor)

    def set_minimo_incremento_opt(self):
        u"""
        Establecer mínimo de incremento por sobre la máxima recompensa en el
        control de entrada.
        """
        minimo = self.window_config["tipos_estados"][TIPOESTADO.FINAL].recompensa

        # El mínimo es la mitad de la máxima recompensa
        self.WMainWindow.sbValOptimoIncremento.setMinimum(minimo / 2.0)

    def mostrar_camino_optimo(self, caminoopt, delay=0, paintinicial=False,
                              paintfinal=False, show_icon=False):
        u"""
        Muestra el camino óptimo obtenido del Recorrido (Play) sobre el GridWorld.

        :param camino: Camino óptimo.
        :param delay: Retraso (en segundos) entre estados al mostrar en pantalla.
        :param paintinicial: Booleano que determina si se debe colorear el Estado Inicial.
        :param paintfinal: Booleano que determina si se debe colorear el Estado Final.
        :param show_icon: Booleano que determina si se debe mostrar el ícono del agente.
        """
        # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
        if caminoopt is not None:
            # Crear copia de la lista para no modificar la original
            camino = caminoopt[:]

            seen = set()
            seen_add = seen.add
            camino_optimo_sin_repetidos = [x for x in camino
                                           if x not in seen and not seen_add(x)]

            # FIXME
            self._logger.debug("Camino óptimo (con repetidos): {0}".format(camino))
            # FIXME
            self._logger.debug("Camino óptimo (sin repetidos): {0}".format(camino_optimo_sin_repetidos))

            # Determinar si se solicitó pintar el estado inicial
            if not paintinicial:
                del camino[0]

            # Determinar si se solicitó pintar el estado inicial
            if not paintfinal:
                del camino[-1]

            # Colorear items pertenecientes al camino optimo
            item_color = QtGui.QColor(self.window_config["opt_path"]["color"])

            # Cachear acceso a métodos y atributos
            gw_item = self.WMainWindow.tblGridWorld.item

            for x, y in camino:
                opt_item = gw_item(x - 1, y - 1)
                opt_item.setBackgroundColor(item_color)
                time.sleep(delay)

    def animar_camino_optimo(self):
        u"""
        Muestra el camino óptimo en el GridWorld introduciendo un retraso de tiempo
        entre los estados con el fin de visualizar el progreso.

        FIXME: Implementar utilizando threading.
        """
        self._logger.debug("Animar camino óptimo...")

        # Ocultar camino óptimo previamente a animar
        self.ocultar_camino_optimo()

        show_delay = self.WMainWindow.sbCOAnimDelay.value()
        paint_inicial = self.window_config["opt_path"]["pintar_inicial"]
        paint_final = self.window_config["opt_path"]["pintar_final"]

        self.mostrar_camino_optimo(self.camino_optimo,
                                   delay=show_delay,
                                   paintinicial=paint_inicial,
                                   paintfinal=paint_final)

    def ocultar_camino_optimo(self, paintinicial=False, paintfinal=False):
        u"""
        Acción que invoca al método para mostrar el camino óptimo. Utilizada desde
        un proceso o UI.
        """
        if self.camino_optimo is not None and self.camino_optimo_active:
            self.camino_optimo_active = False

            # Cachear acceso a métodos y atributos
            get_estado = self.gridworld.get_estado
            gw_item = self.WMainWindow.tblGridWorld.item

            camino_optimo = self.camino_optimo[:]

            if not paintinicial:
                del camino_optimo[0]

            if not paintfinal:
                del camino_optimo[-1]

            for x, y in camino_optimo:
                item = gw_item(x - 1, y - 1)
                estado = get_estado(x, y)
                item.setBackgroundColor(QtGui.QColor(estado.tipo.color))

    def mostrar_camino_optimo_act(self):
        u"""
        Acción que invoca al método para mostrar el camino óptimo. Utilizada desde
        un proceso o UI.
        """
        self._logger.debug("Mostrar camino óptimo")

        self.camino_optimo_active = True

        show_delay = self.window_config["opt_path"]["delay"]
        paint_inicial = self.window_config["opt_path"]["pintar_inicial"]
        paint_final = self.window_config["opt_path"]["pintar_final"]
        self.mostrar_camino_optimo(self.camino_optimo,
                                   delay=show_delay,
                                   paintinicial=paint_inicial,
                                   paintfinal=paint_final)

    def show_hide_camino_optimo(self):
        u"""
        Alterna la visualización del camino óptimo sobre el GridWorld.
        """
        if self.camino_optimo_active:
            self.WMainWindow.btnCOShowHide.setText(_tr("Mostrar"))
            self.ocultar_camino_optimo()
        else:
            self.WMainWindow.btnCOShowHide.setText(_tr("Ocultar"))
            self.mostrar_camino_optimo_act()

    def recargar_estados(self):
        u"""
        (Re)Dibuja los estados del GridWorld en la grilla de la UI.
        """
        # Cachear acceso a métodos y atributos
        show_tooltip = self.window_config["item"]["show_tooltip"]
        get_estado = self.gridworld.get_estado
        gw_setitem = self.WMainWindow.tblGridWorld.setItem
        item_flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        item_text_align = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter

        # Desactivar actualización de la tabla para optimizar la carga
        self.WMainWindow.tblGridWorld.setUpdatesEnabled(False)
        # Rellenar tabla con items
        for fila in xrange(0, self.gridworld.alto):
            for columna in xrange(0, self.gridworld.ancho):
                estado = get_estado(fila + 1, columna + 1)
                letra_estado = estado.tipo.letra
                # Cada item muestra la letra asignada al estado
                item = QtGui.QTableWidgetItem(str(letra_estado))
                item.setBackgroundColor(QtGui.QColor(estado.tipo.color))
                item.setFlags(item_flags)
                item.setTextAlignment(item_text_align)

                if show_tooltip:
                    item.setToolTip("Fila: {0} Columna: {1}\nTipo: {2}\nRecompensa: {3}"
                                    .format(fila + 1, columna + 1,
                                    estado.tipo.nombre,
                                    estado.tipo.recompensa))

                # Agregar item al GridWorld
                gw_setitem(fila, columna, item)
        # Reactivar la actualización de la tabla
        self.WMainWindow.tblGridWorld.setUpdatesEnabled(True)

    def refresh_gw_random(self, rnd_dim=False, incluir_final=False):
        u"""
        Actuliza la grilla en pantalla al crear estados aleatorios.

        :param rnd_dim: Booleano que establece si se genera aleatoriamente la dimensión o se utiliza la actual.
        :param incluir_final: Booleano que establece si se generar aleatorialmente el estado final y se lo incluye.
        """
        self.WMainWindow.btnRecorrer.setDisabled(True)
        self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)

        if rnd_dim:
            indice = random.randint(0, self.WMainWindow.cbGWDimension.count() - 1)
            self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
            self.set_gw_dimension(self.WMainWindow.cbGWDimension.itemData(indice).toString())

        self.estado_final = self.gridworld.generar_estados_aleatorios(incluir_final)
        self.recargar_estados()

    def calcular_recompensa_final(self):
        u"""
        Calcula de manera dinámica la recompensa del Estado Final.
        """
        if self.window_config["gw"]["entrenamiento"]["recompfinalauto"]:
            gamma = self.WMainWindow.sbQLGamma.value()
            estado_excelente = self.window_config["tipos_estados"][TIPOESTADO.EXCELENTE]
            recomp_excelente = estado_excelente.recompensa
            ancho = self.gridworld.ancho

            exponente = self.window_config["exponentes_final"].get(ancho, 1)

            try:
                calc_recomp_final = int(recomp_excelente / (gamma ** (exponente - 1)))

                estado_final_cfg = self.window_config["tipos_estados"][TIPOESTADO.FINAL]
                estado_final_cfg.recompensa = calc_recomp_final

                estado_final_gw = self.gridworld.tipos_estados[TIPOESTADO.FINAL]
                estado_final_gw.recompensa = calc_recomp_final
            except ZeroDivisionError:
                pass

    def generar_menu_estadisticas(self):
        u"""
        Crear el menú de Estadísticas junto a sus acciones.
        """
        self.WMainWindow.menuEstadisticas.clear()

        submenu1 = QtGui.QMenu(_tr("Recompensas promedio"), self)
        action = QtGui.QAction(_tr("Ver gráfico..."), self)
        action.setData(0)
        submenu1.addAction(action)
        action = QtGui.QAction(_tr("Exportar datos..."), self)
        action.setData(1)
        submenu1.addAction(action)

        submenu2 = QtGui.QMenu(_tr("Episodios finalizados"), self)
        action = QtGui.QAction(_tr("Ver gráfico..."), self)
        action.setData(2)
        submenu2.addAction(action)
        action = QtGui.QAction(_tr("Exportar datos..."), self)
        action.setData(3)
        submenu2.addAction(action)

        #=======================================================================
        # submenu3 = QtGui.QMenu(_tr("Iteraciones por episodio"), self)
        # action = QtGui.QAction(_tr("Ver gráfico..."), self)
        # action.setData(4)
        # submenu3.addAction(action)
        # action = QtGui.QAction(_tr("Exportar datos..."), self)
        # action.setData(5)
        # submenu3.addAction(action)
        #=======================================================================

        submenu4 = QtGui.QMenu(_tr("Diferencia entre matrices"), self)
        action = QtGui.QAction(_tr("Ver gráfico..."), self)
        action.setData(6)
        submenu4.addAction(action)
        action = QtGui.QAction(_tr("Exportar datos..."), self)
        action.setData(7)
        submenu4.addAction(action)

        self.WMainWindow.menuEstadisticas.addMenu(submenu1)
        self.WMainWindow.menuEstadisticas.addMenu(submenu2)
        # self.WMainWindow.menuEstadisticas.addMenu(submenu3)
        self.WMainWindow.menuEstadisticas.addMenu(submenu4)

        submenu1.setEnabled(self.graph_recompensas_promedio is not None)
        submenu2.setEnabled(self.graph_episodios_finalizados is not None)
        # submenu3.setEnabled(self.graph_iters_por_episodio is not None)
        submenu4.setEnabled(self.graph_mat_diff is not None)

    def show_estadisticas(self, action):
        u"""
        Muestra ventanas conteniendo el gráfico en función del valor de "action".

        :param action: Acción seleccionada.
        """
        data = action.data().toInt()[0]

        if data == 0:
            # Recompensas promedio
            # Mostrar gráfico
            avg_rwds_thread = QtCore.QThread(self)
            avg_rwds_worker = GraphRecompensasPromedioWorker((self._parametros,
                                                              self.graph_recompensas_promedio))
            avg_rwds_worker.mostrar_figura()
            avg_rwds_worker.moveToThread(avg_rwds_thread)
            avg_rwds_thread.finished.connect(lambda: avg_rwds_thread.wait(100))
            avg_rwds_thread.start()
        elif data == 1:
            # Recompensas promedio
            extfilter = "Datos estadísticos de gráfico (*.csv)"
            filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                         caption=_tr('Exportar datos'),
                                                         filter=_tr(extfilter))

            if filename:
                avg_rwds_worker = GraphRecompensasPromedioWorker((self._parametros,
                                                                  self.graph_recompensas_promedio))
                avg_rwds_worker.exportar_info(filename)
        elif data == 2:
            # Episodios finalizados
            # Mostrar gráfico
            suces_eps_thread = QtCore.QThread(self)
            suces_eps_worker = GraphSucessfulEpisodesWorker((self._parametros,
                                                               self.graph_episodios_finalizados))
            suces_eps_worker.mostrar_figura()
            suces_eps_worker.moveToThread(suces_eps_thread)
            suces_eps_thread.finished.connect(lambda: suces_eps_thread.wait(100))
            suces_eps_thread.start()
        elif data == 3:
            # Episodios finalizados
            extfilter = "Datos estadísticos de gráfico (*.csv)"
            filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                         caption=_tr('Exportar datos'),
                                                         filter=_tr(extfilter))

            if filename:
                suces_eps_worker = GraphSucessfulEpisodesWorker((self._parametros,
                                                                  self.graph_episodios_finalizados))
                suces_eps_worker.exportar_info(filename)
        elif data == 4:
            # Iteraciones por episodio
            # Mostrar gráfico
            #===================================================================
            # iters_por_ep_thread = QtCore.QThread(self)
            # iters_por_ep_worker = GraphIteracionesXEpisodioWorker((self._parametros,
            #                                                        self.graph_iters_por_episodio))
            # iters_por_ep_worker.mostrar_figura()
            # iters_por_ep_worker.moveToThread(iters_por_ep_thread)
            # iters_por_ep_thread.finished.connect(lambda: iters_por_ep_thread.wait(100))
            # iters_por_ep_thread.start()
            #===================================================================
            pass
        elif data == 5:
            #===============================================================================
            # extfilter = "Datos estadísticos de gráfico (*.csv)"
            # filename = QtGui.QFileDialog.getSaveFileName(parent=self,
            #                                              caption=_tr('Exportar datos'),
            #                                              filter=_tr(extfilter))
            #
            # if filename:
            #     iters_por_ep_worker = GraphIteracionesXEpisodioWorker((self._parametros,
            #                                                            self.graph_iters_por_episodio))
            #     iters_por_ep_worker.exportar_info(filename)
            #===============================================================================
            pass
        elif data == 6:
            # Diferencia entre matrices Q
            # Mostrar gráfico
            mat_diffs_thread = QtCore.QThread(self)
            mat_diffs_worker = GraphMatrizDiffsWorker((self._parametros,
                                                       self.graph_mat_diff))
            mat_diffs_worker.mostrar_figura()
            mat_diffs_worker.moveToThread(mat_diffs_thread)
            mat_diffs_thread.finished.connect(lambda: mat_diffs_thread.wait(100))
            mat_diffs_thread.start()
        elif data == 7:
            extfilter = "Datos estadísticos de gráfico (*.csv)"
            filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                         caption=_tr('Exportar datos'),
                                                         filter=_tr(extfilter))

            if filename:
                mat_diffs_worker = GraphMatrizDiffsWorker((self._parametros,
                                                           self.graph_mat_diff))
                mat_diffs_worker.exportar_info(filename)

    def generar_menu_edicion(self):
        u"""
        Crea el menú Edición junto a sus acciones.
        """
        action = QtGui.QAction("Copiar datos de pruebas al portapapeles", self)
        action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+C"))
        action.triggered.connect(self.copiar_prueba_toclipboard)
        self.WMainWindow.menuEdicion.addAction(action)

    def copiar_prueba_toclipboard(self):
        u"""
        Copiar datos de prueba al portapapeles.
        """
        if self.estado_final is None:
            QtGui.QMessageBox.warning(self,
                                      _tr('QLearning - Entrenamiento'),
                                      "Debe establecer un Estado Final antes de copiar la prueba.")
            return None

        linea_prueba_items = []
        linea_prueba_items.append(self.gridworld.get_matriz_tipos_estados())
        linea_prueba_items.append(self.WMainWindow.sbQLGamma.value())

        indice = self.WMainWindow.cbQLTecnicas.currentIndex()
        tecnica = self.WMainWindow.cbQLTecnicas.itemData(indice).toInt()[0]

        if tecnica == 0:
            parametro = 0
        elif tecnica == 1:
            parametro = self.WMainWindow.sbQLEpsilon.value()
        elif tecnica == 2:
            parametro = self.WMainWindow.sbQLTau.value()
        elif tecnica == 3:
            parametro = 1

        linea_prueba_items.append(tecnica)
        linea_prueba_items.append(parametro)
        linea_prueba_items.append(self.WMainWindow.sbCantidadEpisodios.value())
        linea_prueba_items.append(self.WMainWindow.sbDecrementoVal.value())
        linea_prueba_items.append(self.WMainWindow.sbCantEpisodiosDec.value())
        linea_prueba_items.append(self.WMainWindow.chkLimitarCantIteraciones.isChecked())
        linea_prueba_items.append(self.WMainWindow.sbCantMaxIteraciones.value())

        if self.WMainWindow.optMQInitEnCero.isChecked():
            valor_inicial = 0
        elif self.WMainWindow.optMQInitValOptimistas.isChecked():
            incremento = self.WMainWindow.sbValOptimoIncremento.value()
            valor_inicial = incremento

        linea_prueba_items.append(valor_inicial)
        linea_prueba_items.append(self.WMainWindow.chkQLCalcularMatDiff.isChecked())
        linea_prueba_items.append(self.WMainWindow.sbMatricesMinDiff.value())
        linea_prueba_items.append(self.WMainWindow.sbIntervaloDiffCalc.value())

        linea_prueba = ";".join([str(item) for item in linea_prueba_items])

        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(linea_prueba)

    def _join_graph_thread(self, threadp):
        u"""
        Hacer join del thread dedicado a gráficar.

        :param threadp: Hilo al cual se le hará join.
        """
        try:
            self._logger.debug("Join Thread: {0}".format(threadp))
            threadp.terminate()
            threadp.wait(500)
        except threading.ThreadError:
            pass

    def calcular_gamma_minimo(self):
        u"""
        Calcula el mínimo gamma permitido de acuerdo al máximo Emax admitido
        por el sistema.
        """
        estado_excelente = self.window_config["tipos_estados"][TIPOESTADO.EXCELENTE]
        recomp_excelente = estado_excelente.recompensa
        ancho = self.gridworld.ancho
        exponente = self.window_config["exponentes_final"].get(ancho, 1)

        tau = decimal.Decimal(self.WMainWindow.sbQLTau.value())
        gamma = 0.01
        incremento = 0.01

        c_decimal = decimal.Decimal
        while 1:
            try:
                calc_recomp_final = int(recomp_excelente / (gamma ** (exponente - 1)))
                expo = c_decimal(calc_recomp_final) / tau
                expo.exp()
                break
            except decimal.Overflow:
                gamma += incremento

        self.WMainWindow.sbQLGamma.setMinimum(gamma)

    def generar_menu_pruebas(self):
        u"""
        Crear submenúes y acciones para el menú Pruebas.
        """
        action = QtGui.QAction("Cargar prueba...", self)
        action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+L"))
        action.triggered.connect(self.cargar_prueba)
        self.WMainWindow.menuPruebas.addAction(action)

        action = QtGui.QAction("Guardar prueba...", self)
        action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+S"))
        action.triggered.connect(self.guardar_prueba)
        self.WMainWindow.menuPruebas.addAction(action)

        self.WMainWindow.menuPruebas.addSeparator()

        action = QtGui.QAction("Copiar datos de prueba al portapapeles", self)
        action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+C"))
        action.triggered.connect(self.copiar_prueba_toclipboard)
        self.WMainWindow.menuPruebas.addAction(action)

    def cargar_prueba(self):
        u"""
        Cargar escenario de prueba desde archivo.
        """
        extfilter = "Prueba de Q-Learning (*.csv)"
        filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                     caption=_tr('Cargar prueba'),
                                                     filter=_tr(extfilter)
                                                     )

        if filename:
            with open(filename, 'rb') as csvf:
                prueba_reader = csv.reader(csvf, dialect='excel', delimiter=';')

                prueba = prueba_reader.next()
                while prueba == '':
                    try:
                        prueba = prueba_reader.next()
                    except StopIteration:
                        break

                if len(prueba) == 13:
                    estados_num = eval(prueba[0])
                    gamma = float(prueba[1].replace(',', '.'))
                    tecnica_idx = int(prueba[2])
                    parametro = float(prueba[3].replace(',', '.'))
                    cant_episodios = int(prueba[4])
                    decremento = float(prueba[5].replace(',', '.'))
                    interv_dec = int(prueba[6])
                    limitar_iter = prueba[7].strip().lower()
                    cant_max_iter = int(prueba[8])
                    valor_inicial = float(prueba[9].replace(',', '.'))
                    calcular_mat_diff = prueba[10].strip().lower()
                    mat_diff_min = float(prueba[11].replace(',', '.'))
                    interv_calc_diff = int(prueba[12])

                    indice = self.WMainWindow.cbQLTecnicas.findData(tecnica_idx)
                    self.WMainWindow.cbQLTecnicas.setCurrentIndex(indice)

                    self.WMainWindow.sbQLGamma.setValue(gamma)

                    if tecnica_idx == 0:
                        self.WMainWindow.sbQLEpsilon.setValue(0)
                    elif tecnica_idx == 1:
                        self.WMainWindow.sbQLEpsilon.setValue(parametro)
                    elif tecnica_idx == 2:
                        self.WMainWindow.sbQLTau.setValue(parametro)
                    elif tecnica_idx == 3:
                        self.WMainWindow.sbQLEpsilon.setValue(parametro)

                    self.WMainWindow.sbCantidadEpisodios.setValue(cant_episodios)
                    self.WMainWindow.sbDecrementoVal.setValue(decremento)
                    self.WMainWindow.sbCantMaxIteraciones.setValue(cant_max_iter)
                    self.WMainWindow.sbMatricesMinDiff.setValue(mat_diff_min)
                    self.WMainWindow.sbIntervaloDiffCalc.setValue(interv_calc_diff)
                    self.WMainWindow.sbCantEpisodiosDec.setValue(interv_dec)

                    if valor_inicial == 0:
                        self.WMainWindow.optMQInitEnCero.setChecked(True)
                    elif valor_inicial > 0:
                        self.WMainWindow.optMQInitValOptimistas.setChecked(True)
                        self.WMainWindow.sbValOptimoIncremento.setValue(valor_inicial)

                    if limitar_iter == 'true':
                        self.WMainWindow.chkLimitarCantIteraciones.setChecked(True)
                    elif limitar_iter == 'false':
                        self.WMainWindow.chkLimitarCantIteraciones.setChecked(False)

                    if calcular_mat_diff == 'true':
                        self.WMainWindow.chkQLCalcularMatDiff.setChecked(True)
                    elif calcular_mat_diff == 'false':
                        self.WMainWindow.chkQLCalcularMatDiff.setChecked(False)

                    self.WMainWindow.cbGWDimension.currentIndexChanged.disconnect()

                    ancho, alto = len(estados_num), len(estados_num[0])
                    dimension = "{0} x {1}".format(ancho, alto)
                    indice = self.WMainWindow.cbGWDimension.findData(dimension)
                    self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
                    self.WMainWindow.cbGWDimension.currentIndexChanged.connect(self.set_gw_dimension_cb)

                    self.set_gw_dimension(dimension)
                    self.estado_final = self.gridworld.from_matriz_tipos_estados(estados_num)
                    self.recargar_estados()

    def guardar_prueba(self):
        u"""
        Guardar datos de prueba a archivo.
        """
        if self.estado_final is None:
            QtGui.QMessageBox.warning(self,
                                      _tr('QLearning - Entrenamiento'),
                                      "Debe establecer un Estado Final antes guardar la prueba.")
            return None

        extfilter = "Prueba de Q-Learning (*.csv)"
        filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                     caption=_tr('Guardar prueba'),
                                                     filter=_tr(extfilter))

        if filename:
            with open(filename, 'wb') as csvf:
                csv_writer = csv.writer(csvf, dialect='excel', delimiter=';')

                indice = self.WMainWindow.cbQLTecnicas.currentIndex()
                tecnica = self.WMainWindow.cbQLTecnicas.itemData(indice).toInt()[0]

                if tecnica == 0:
                    parametro = 0
                elif tecnica == 1:
                    parametro = self.WMainWindow.sbQLEpsilon.value()
                elif tecnica == 2:
                    parametro = self.WMainWindow.sbQLTau.value()
                elif tecnica == 3:
                    parametro = 1

                if self.WMainWindow.optMQInitEnCero.isChecked():
                    valor_inicial = 0
                elif self.WMainWindow.optMQInitValOptimistas.isChecked():
                    valor_inicial = self.WMainWindow.sbValOptimoIncremento.value()

                csv_writer.writerow([self.gridworld.get_matriz_tipos_estados(),
                                    self.WMainWindow.sbQLGamma.value(),
                                    tecnica,
                                    parametro,
                                    self.WMainWindow.sbCantidadEpisodios.value(),
                                    self.WMainWindow.sbDecrementoVal.value(),
                                    self.WMainWindow.sbCantEpisodiosDec.value(),
                                    self.WMainWindow.chkLimitarCantIteraciones.isChecked(),
                                    self.WMainWindow.sbCantMaxIteraciones.value(),
                                    valor_inicial,
                                    self.WMainWindow.chkQLCalcularMatDiff.isChecked(),
                                    self.WMainWindow.sbMatricesMinDiff.value(),
                                    self.WMainWindow.sbIntervaloDiffCalc.value()])
