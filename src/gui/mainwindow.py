#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import multiprocessing
import Queue
import random
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
                                     "enabled": True},
                               "size": 40},
                              "gw":
                               {"entrenamiento": {"actual_state": {"show": True, "color": "#000000", "icono": None}},
                                "recorrido": {"actual_state": {"show": True, "color": "#000000", "icono": None}}
                               },
                              "tipos_estados":
                               {0: TipoEstado(0, None, _tr("Inicial"), _tr("I"), "#FF5500", None),
                                1: TipoEstado(1, 1000, _tr("Final"), _tr("F"), "#0071A6", None),
                                2: TipoEstado(2, None, _tr("Agente"), _tr("A"), "#474747",
                                              QtGui.QIcon(QtGui.QPixmap(":/iconos/Agente_1.png"))),
                                3: TipoEstado(3, 0, _tr("Neutro"), _tr("N"), "#FFFFFF", None),
                                4: TipoEstado(4, 100, _tr("Excelente"), _tr("E"), "#BB0011", None),
                                5: TipoEstado(5, 50, _tr("Bueno"), _tr("B"), "#4F0ACC", None),
                                6: TipoEstado(6, -10, _tr("Malo"), _tr("M"), "#EB00A1", None),
                                7: TipoEstado(7, None, _tr("Pared"), _tr("P"), "#000000", None),
                                },
                              "opt_path":
                                {"color": "#70DC4C",
                                 "pintar_inicial": False,
                                 "pintar_final": False,
                                 "delay": 0,
                                 "show_icon": False}
                             }

    def _initialize_window(self):
        # Aspectos de la ventana principal
        screen_geometry = QtGui.QApplication.desktop().screenGeometry()
        y_wnd = (screen_geometry.height() - self.height()) / 2.0
        x_wnd = (screen_geometry.width() - self.width()) / 2.0
        # Centrar la ventana en la pantalla
        self.move(x_wnd, y_wnd)

        self.setWindowFlags(QtCore.Qt.WindowSoftkeysVisibleHint)

        self.lbl_item_actual = QtGui.QLabel()
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

        # Asignar shorcuts
        entrenar_shortcut = "F5"
        recorrer_shortcut = "F6"
        cancelar_shortcut = "Shift+X"
        self.WMainWindow.btnEntrenar.setShortcut(QtGui.QKeySequence(entrenar_shortcut))
        self.WMainWindow.btnRecorrer.setShortcut(QtGui.QKeySequence(recorrer_shortcut))
        self.WMainWindow.btnTerminarProceso.setShortcut(QtGui.QKeySequence(cancelar_shortcut))

        self.WMainWindow.btnEntrenar.setToolTip("<html><head/><body><p>\
                                                Entrenar agente \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(entrenar_shortcut))
        self.WMainWindow.btnRecorrer.setToolTip("<html><head/><body><p>\
                                                Recorrer GridWorld \
                                                <span style='font-size:7pt;'>\
                                                {0}</span></p></body></html>"
                                                .format(recorrer_shortcut))
        self.WMainWindow.btnTerminarProceso.setToolTip("<html><head/><body><p>\
                                                    Cancelar proceso \
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
                                   [TIPOESTADO.PARED])

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
        elif key == 2:
            # Softmax
            self.WMainWindow.lblEpsilon.hide()
            self.WMainWindow.sbQLEpsilon.hide()
            self.WMainWindow.lblTau.show()
            self.WMainWindow.sbQLTau.show()
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
            self.WMainWindow.sbCantEpisodiosDec.setEnabled(True)
            self.WMainWindow.sbDecrementoVal.setEnabled(True)
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
            for item in selected_items:
                # Obtener el tipo de estado asociado al texto clickeado
                tipo_num = action.data().toInt()[0]
                # Actualizar texto del item de la tabla en función del tipo de estado
                item.setText(tipos_estados[tipo_num].letra)
                # Establecer color de fondo de acuerdo al tipo de estado
                item.setBackgroundColor(QtGui.QColor(tipos_estados[tipo_num].color))
                item.setSelected(False)

                estado_actual = self.gridworld.get_estado(item.row() + 1,
                                                      item.column() + 1)

                if tipo_num == TIPOESTADO.INICIAL:
                    self.estado_inicial = estado_actual
                elif tipo_num == TIPOESTADO.FINAL:
                    self.estado_final = estado_actual

                if estado_actual.tipo.ide == TIPOESTADO.INICIAL:
                    self.estado_inicial = None
                elif estado_actual.tipo.ide == TIPOESTADO.FINAL:
                    self.estado_final = None
                    self.WMainWindow.btnRecorrer.setDisabled(True)
                    self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)

                # Establecer tipo de estado seleccionado al estado en la matriz de
                # Estados
                estado_actual.tipo = tipos_estados[tipo_num]

                if self.window_config["item"]["show_tooltip"]:
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

        # Parámetros para mostrar el estado actual en pantalla
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

        # Crear una nueva instancia de Q-Learning
        self.qlearning = QLearning(self.gridworld,
                                   gamma,
                                   (tecnica, parametro, paso_decremento, intervalo_decremento),
                                   cant_episodios,
                                   (limitar_nro_iteraciones, cant_max_iter),
                                   init_value_fn,
                                   (matdiff_status, matriz_min_diff, intervalo_diff_calc),
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

        # Mostrar cursor de ocupado indicando que se está procesando
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))

        if self.entrenar_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Entrenando agente..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.entrenar_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.entrenar_is_running)

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

        if self.recorrer_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Agente buscando camino óptimo..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.recorrer_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.recorrer_is_running)

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
        self.window_config["item"]["show_tooltip"] = self.window_config["item"]["show_tooltip"] and True

        self._logger.debug("Procesos hijos activos: {0}\nFin de procesamiento"
            .format(multiprocessing.active_children()))

        self.WMainWindow.gbGridWorld.setEnabled(True)
        self.WMainWindow.gbQLearning.setEnabled(True)
        self.WMainWindow.gbGeneral.setEnabled(True)
        self.WMainWindow.gbMatrices.setEnabled(True)

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

        # Restaurar cursor normal
        QtGui.QApplication.restoreOverrideCursor()

    def _reintentar_detener_hilos(self):
        u"""
        Solicita la finalización de todos los threads utilizados en la
        aplicación. Este método debe ser llamado al desconectarse o al salir
        de la aplicación.
        """
        for proceso in multiprocessing.active_children():
            try:
                # Darle una oportunidad más al proceso de terminar
                proceso.join(0.01)
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
        self.inicializar_gw()
        self.inicializar_ql_vals()

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
        # Cachear acceso al objeto WMainWindow
        main_wnd = self.WMainWindow

        try:
            data_entrenar = self.get_all_from_queue(self.ql_entrenar_out_q)

            for ql_ent_info in data_entrenar:
                estado_actual_ent = ql_ent_info.get('EstadoActual', None)
                nro_episodio = ql_ent_info.get('NroEpisodio', None)
                cant_iteraciones = ql_ent_info.get('NroIteracion', None)
                episode_exec_time = ql_ent_info.get('EpisodiosExecTime', 0.0)
                iter_exec_time = ql_ent_info.get('IteracionesExecTime', 0.0)
                worker_joined = ql_ent_info.get('ProcesoJoined', None)
                loop_alarm = ql_ent_info.get('LoopAlarm', False)
                matriz_q = ql_ent_info.get('MatrizQ', None)
                valor_parametro = ql_ent_info.get('ValorParametro', None)
                running_exec_time_ent = ql_ent_info.get('RunningExecTime', 0.0)
                tmp_mat_diff = ql_ent_info.get('MatDiff', None)
                corte_iteracion = ql_ent_info.get('CorteIteracion', None)

                self.matriz_q = matriz_q

                if loop_alarm:
                    QtGui.QMessageBox.warning(self,
                                              _tr('QLearning - Entrenamiento'),
                    u"Se ha detectado que el Estado Final se encuentra bloqueado por lo que se cancelará el entrenamiento.")
                    self.working_process.join(0.05)
                    self.qlearning_entrenar_worker = None
                    self.working_process = None
                    self.ql_entrenar_error_q = None
                    self.ql_entrenar_out_q = None

                try:
                    # Descomponen coordenadas de estado actual
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
                except TypeError:
                    pass
                except ValueError:
                    pass

                # Mostrar estado actual en grilla
                if self.ent_show_estado_act:
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
                        item.setBackground(self.ent_color_estado_act)
        except Queue.Empty:
            pass
        except AttributeError:
            pass

    def update_window_recorrer(self):
        u"""
        Actualizar ventana con información del Recorrido
        """
        # Cachear acceso al objeto WMainWindow
        main_wnd = self.WMainWindow

        try:
            data_recorrer = self.get_all_from_queue(self.ql_recorrer_out_q)

            for ql_rec_info in data_recorrer:
                estado_actual_rec = ql_rec_info.get('EstadoActual', None)
                camino_optimo = ql_rec_info.get('CaminoRecorrido', None)
                running_exec_time_rec = ql_rec_info.get('RunningExecTime', 0.0)
                worker_joined = ql_rec_info.get('ProcesoJoined', None)
                rec_exec_time = ql_rec_info.get('RecorridoExecTime', 0.0)
                nro_iteracion = ql_rec_info.get('NroIteracion', None)

                self.camino_optimo = camino_optimo

                try:
                    # Descomponer coordenadas de estado actual
                    x_actual, y_actual = estado_actual_rec
                    self._logger.debug("Estado actual: {0}".format(estado_actual_rec))

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
                if self.rec_show_estado_act:
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
                proceso.join(0.01)
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
        self.lbl_item_actual.setText("")

    def enterEvent(self, event):
        self.lbl_item_actual.setText("")

    def set_gw_dimension_menu(self, action):
        dimension = action.data().toString()
        self._logger.debug("Dimensión: {0}".format(dimension))
        indice = self.WMainWindow.cbGWDimension.findData(dimension)
        self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
        self.set_gw_dimension(dimension)

    def set_gw_dimension_cb(self, indice):
        dimension = self.WMainWindow.cbGWDimension.itemData(indice).toString()
        self._logger.debug("Dimensión: {0}".format(dimension))
        self.set_gw_dimension(dimension)

    def parametros_segun_tecnica_menu(self, action):
        indice = action.data().toInt()[0]
        self.WMainWindow.cbQLTecnicas.setCurrentIndex(indice)

    def generar_menu_dimensiones(self):
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
        # Inicializar cuadros de diálogo
        self.GWOpcionesD = GWOpcionesDialog(self)

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

            new_tipos_estados = self.GWOpcionesD.tipos_estados

            self.window_config["tipos_estados"] = new_tipos_estados
            self.refresh_gw()

    def mostrar_gen_rnd_estados_dialog(self):
        self.GWGenRndEstValsD = GWGenRndEstadosDialog(self)
        if self.GWGenRndEstValsD.exec_():
            pass

    def inicializar_gw(self):
        # Cargar dimensiones posibles del GridWorld
        try:
            self.WMainWindow.cbGWDimension.currentIndexChanged.disconnect()
        except Exception:
            pass

        self.WMainWindow.cbGWDimension.clear()
        for dimension in self.gw_dimensiones:
            self.WMainWindow.cbGWDimension.addItem(_tr(dimension), dimension)

        self.WMainWindow.cbGWDimension.currentIndexChanged.connect(self.set_gw_dimension_cb)

        self.estado_final = None
        self.estado_inicial = None

        self.refresh_gw()

    def refresh_gw(self):
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

        # Establecer por defecto 1 episodio
        self.WMainWindow.sbCantidadEpisodios.setValue(1)

        # Establecer por defecto un Epsilon = 0.5
        self.WMainWindow.sbQLEpsilon.setValue(0.5)

        # Establecer por defecto un Gamma = 0.8
        self.WMainWindow.sbQLGamma.setValue(0.8)

        self.WMainWindow.sbDecrementoVal.setValue(0.01)
        self.WMainWindow.sbCantEpisodiosDec.setValue(1)
        self.WMainWindow.sbCantEpisodiosDec.setSuffix(_tr(" episodios"))
        self.WMainWindow.chkDecrementarParam.setChecked(True)
        self.WMainWindow.sbQLTau.setValue(10)
        self.WMainWindow.sbIntervaloDiffCalc.setSuffix(_tr(" episodios"))
        self.WMainWindow.sbCantMaxIteraciones.setValue(200)
        self.WMainWindow.sbIntervaloDiffCalc.setMinimum(2)
        self.WMainWindow.sbCantidadEpisodios.setValue(50)
        self.WMainWindow.sbValOptimoIncremento.setValue(500)
        self.WMainWindow.optMQInitEnCero.setChecked(True)

        self.WMainWindow.sbCOAnimDelay.setSuffix(_tr(" seg"))
        self.WMainWindow.sbCOAnimDelay.setValue(1)

        enable_controls = not self.WMainWindow.optMQInitValOptimistas.isEnabled()
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

    def mostrar_camino_optimo(self, caminoopt, delay=0, paintinicial=False, paintfinal=False, show_icon=False):
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

            for x, y in camino:
                opt_item = self.WMainWindow.tblGridWorld.item(x - 1, y - 1)
                opt_item.setBackgroundColor(item_color)
                time.sleep(delay)

    def animar_camino_optimo(self):
        u"""
        Muestra el camino óptimo en el GridWorld introduciendo un retraso de tiempo
        entre los estados con el fin de visualizar el progreso.
        """
        logging.debug("Animar camino óptimo")

        # Ocultar camino óptimo previamente a animar
        self.ocultar_camino_optimo()

        show_delay = self.WMainWindow.sbCOAnimDelay.value()
        paint_inicial = self.window_config["opt_path"]["pintar_inicial"]
        paint_final = self.window_config["opt_path"]["pintar_final"]

        self.mostrar_camino_optimo(self.camino_optimo,
                                   delay=show_delay,
                                   paintinicial=paint_inicial,
                                   paintfinal=paint_final)

    def ocultar_camino_optimo(self):
        u"""
        Acción que invoca al método para mostrar el camino óptimo. Utilizada desde
        un proceso o UI.
        """
        logging.debug("Ocultar camino óptimo")

        if self.camino_optimo is not None and self.camino_optimo_active:
            self.camino_optimo_active = False

            for x, y in self.camino_optimo:
                item = self.WMainWindow.tblGridWorld.item(x - 1, y - 1)
                estado = self.gridworld.get_estado(x, y)
                item.setBackgroundColor(QtGui.QColor(estado.tipo.color))

    def mostrar_camino_optimo_act(self):
        u"""
        Acción que invoca al método para mostrar el camino óptimo. Utilizada desde
        un proceso o UI.
        """
        logging.debug("Mostrar camino óptimo")

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
        # Desactivar actualización de la tabla para optimizar la carga
        self.WMainWindow.tblGridWorld.setUpdatesEnabled(False)
        # Rellenar tabla con items
        for fila in xrange(0, self.gridworld.alto):
            for columna in xrange(0, self.gridworld.ancho):
                estado = self.gridworld.get_estado(fila + 1, columna + 1)
                letra_estado = estado.tipo.letra
                # Cada item muestra la letra asignada al estado
                item = QtGui.QTableWidgetItem(str(letra_estado))
                item.setBackgroundColor(QtGui.QColor(estado.tipo.color))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)

                if self.window_config["item"]["show_tooltip"]:
                    item.setToolTip("Fila: {0} Columna: {1}\nTipo: {2}\nRecompensa: {3}"
                                    .format(fila + 1, columna + 1,
                                    estado.tipo.nombre,
                                    estado.tipo.recompensa))

                self.WMainWindow.tblGridWorld.setItem(fila, columna, item)
        # Reactivar la actualización de la tabla
        self.WMainWindow.tblGridWorld.setUpdatesEnabled(True)

    def refresh_gw_random(self, rnd_dim=False, incluir_final=False):
        self.WMainWindow.btnRecorrer.setDisabled(True)
        self.WMainWindow.btnMostrarMatrizQ.setDisabled(True)

        if rnd_dim:
            indice = random.randint(0, self.WMainWindow.cbGWDimension.count() - 1)
            self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
            self.set_gw_dimension(self.WMainWindow.cbGWDimension.itemData(indice).toString())

        self.estado_final = self.gridworld.generar_estados_aleatorios(incluir_final)
        self.recargar_estados()
