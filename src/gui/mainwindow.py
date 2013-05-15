#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import multiprocessing
import Queue

from PyQt4 import QtCore, QtGui

from info import app_info

from gui.aboutdialog import AboutDialog
from gui.qtgen.mainwindow import Ui_MainWindow
from gui.gwgenrndestadosdialog import GWGenRndEstadosDialog
from gui.gwopcionesdialog import GWOpcionesDialog
from gui.matrizdialog import ShowMatrizDialog

from core.estado.estado import TIPOESTADO
from core.gridworld.gridworld import GridWorld
from core.qlearning.qlearning import QLearning
from core.qlearning.matrixinits import QLMatrixInitEnCero
from core.qlearning.matrixinits import QLMatrixInitEnRecompensa
from core.qlearning.matrixinits import QLMatrixInitRandom
from core.tecnicas.aleatorio import Aleatorio
from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax

from tools.livedatafeed import LiveDataFeed
from tools.listacircular import ListaCircular
from tools.queue import get_all_from_queue, get_item_from_queue
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
        self.ql_datos_entrenar_in_feed = LiveDataFeed()
        self.ql_datos_recorrer_in_feed = LiveDataFeed()
        self.estado_inicial = None
        self.estado_final = None
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

        self.tecnicas = {0: "Greedy",
                         1: "ε-Greedy",
                         2: "Softmax",
                         3: "Aleatorio"}
        self.gw_dimensiones = ["3 x 3", "4 x 4", "5 x 5",
                               "6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"]
        self.window_config = {"item":
                              {"show_tooltip": False,
                               "menu_estado":
                                    {"ocultar_tipos":
                                     [TIPOESTADO.AGENTE],
                                     "enabled": True},
                               "size": 40}}

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

        # Obtener ancho y alto del GridWorld
        self._logger.debug("Dimensión: {0}".format(dimension))
        ancho_gw, alto_gw = self.convert_dimension(dimension)
        # Crear un nuevo GridWorld dados el ancho y el alto del mismo
        self.gridworld = GridWorld(ancho_gw,
                                   alto_gw,
                                   excluir_tipos_vecinos=[TIPOESTADO.PARED])

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

        self.estado_inicial = None
        self.estado_final = None

        # Activar la visualización de la Matriz R
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
            self.WMainWindow.chkDecrementarParam.setEnabled(False)
        elif key == 1:
            # E-Greedy
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setMinimum(0.01)
            self.WMainWindow.sbQLEpsilon.setEnabled(True)
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
        elif key == 2:
            # Softmax
            self.WMainWindow.lblEpsilon.hide()
            self.WMainWindow.sbQLEpsilon.hide()
            self.WMainWindow.lblTau.show()
            self.WMainWindow.sbQLTau.show()
            self.WMainWindow.chkDecrementarParam.setEnabled(True)
        elif key == 3:
            # Aleatorio
            self.WMainWindow.lblTau.hide()
            self.WMainWindow.sbQLTau.hide()
            self.WMainWindow.lblEpsilon.show()
            self.WMainWindow.sbQLEpsilon.show()
            self.WMainWindow.sbQLEpsilon.setMinimum(1.00)
            self.WMainWindow.sbQLEpsilon.setValue(1.00)
            self.WMainWindow.sbQLEpsilon.setEnabled(False)
            self.WMainWindow.chkDecrementarParam.setEnabled(False)

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
                estado_actual = self.gridworld.get_estado(item.row() + 1, item.column() + 1)

                if tipo_num == TIPOESTADO.INICIAL:
                    self.estado_inicial = estado_actual
                elif tipo_num == TIPOESTADO.FINAL:
                    self.estado_final = estado_actual

                if estado_actual.tipo.ide == TIPOESTADO.INICIAL:
                    self.estado_inicial = None
                elif estado_actual.tipo.ide == TIPOESTADO.FINAL:
                    self.estado_final = None

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
                                          "Debe establecer un Estado Final antes de realizar el recorrido.")
            return None

        # Bloquear GridWorld
        self.window_config["item"]["menu_estado"]["enabled"] = False
        self.window_config["item"]["show_tooltip"] = False

        # ----------- Comienzo de seteo de la técnica --------------
        # Obtener la información asociada al ítem actual del combobox
        item_data = self.WMainWindow.cbQLTecnicas.itemData(self.WMainWindow.cbQLTecnicas.currentIndex())
        # Obtener el índice propio de la técnica a utilizar
        id_tecnica = item_data.toInt()[0]
        tecnica = self.tecnicas[id_tecnica]

        if id_tecnica == 0:
            # Greedy
            tecnica = Greedy()
        elif id_tecnica == 1:
            # E-Greedy
            epsilon = self.WMainWindow.sbQLEpsilon.value()
            tecnica = EGreedy(epsilon)
        elif id_tecnica == 2:
            # Softmax
            tau = self.WMainWindow.sbQLTau.value()
            tecnica = Softmax(tau)
        elif id_tecnica == 3:
            # Aleatorio
            tecnica = Aleatorio()
        else:
            tecnica = None

        if self.WMainWindow.chkDecrementarParam.isChecked():
                paso_decremento = self.WMainWindow.sbDecrementoVal.value()
                intervalo_decremento = self.WMainWindow.sbCantEpisodiosDec.value()
                tecnica.paso_decremento = paso_decremento
                tecnica.intervalo_decremento = intervalo_decremento
        # ----------- Fin de seteo de la técnica --------------

        gamma = self.WMainWindow.sbQLGamma.value()
        cant_episodios = int(self.WMainWindow.sbCantidadEpisodios.value())
        # TODO: Se puede cambiar la función para inicializar la Matriz Q
        init_value_fn = QLMatrixInitEnCero()

        # Crear nueva instancia de Q-Learning
        self.qlearning = QLearning(self.gridworld,
                                   gamma,
                                   tecnica,
                                   cant_episodios,
                                   init_value_fn,
                                   None)

        # QLearningEntrenarWorker Management
        # Que empiece la magia
        self.ql_entrenar_out_q = multiprocessing.Queue()
        self.ql_entrenar_error_q = multiprocessing.Queue()
        self.ql_datos_entrenar_in_feed = LiveDataFeed()

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
                                          _tr('QLearning - Recorrido'),
                                          "Debe establecer un Estado Final antes de realizar el recorrido.")
            return None

        if self.estado_inicial is None:
            QtGui.QMessageBox.warning(self,
                                          _tr('QLearning - Recorrido'),
                                          "Debe establecer un Estado Inicial antes de realizar el recorrido.")
            return None

        self.ql_recorrer_out_q = multiprocessing.Queue()
        self.ql_recorrer_error_q = multiprocessing.Queue()
        self.ql_datos_recorrer_in_feed = LiveDataFeed()
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
        self._logger.debug("Timer Timeout")
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
        self.wnd_timer.start(20)

        if self.entrenar_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Entrenando agente..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.entrenar_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.entrenar_is_running)

        if self.recorrer_is_running:
            self.WMainWindow.statusBar.showMessage(_tr("Agente buscando camino óptimo..."))
            self.WMainWindow.btnEntrenar.setDisabled(self.recorrer_is_running)
            self.WMainWindow.btnRecorrer.setDisabled(self.recorrer_is_running)

        self.WMainWindow.btnTerminarProceso.setEnabled(True)
        self.WMainWindow.gbGridWorld.setDisabled(True)
        self.WMainWindow.gbQLearning.setDisabled(True)
        self.WMainWindow.gbGeneral.setDisabled(True)
        self.WMainWindow.gbMatrices.setDisabled(True)

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

        self._logger.debug("Procesos hijos activos: {0}"
                      .format(multiprocessing.active_children()))
        self._logger.debug("Fin de procesamiento")

        self.WMainWindow.gbGridWorld.setEnabled(True)
        self.WMainWindow.gbQLearning.setEnabled(True)
        self.WMainWindow.gbGeneral.setEnabled(True)
        self.WMainWindow.gbMatrices.setEnabled(True)

        if self.entrenar_is_running:
            self.entrenar_is_running = False
            self.WMainWindow.btnEntrenar.setEnabled(True)
            self.WMainWindow.actionAgenteEntrenar.setEnabled(True)

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

        self.WMainWindow.btnTerminarProceso.setEnabled(False)
        self.WMainWindow.statusBar.clearMessage()
        self.WMainWindow.btnMostrarMatrizR.setEnabled(True)

        try:
            self.wnd_taskbar.SetProgressState(self.winId(),
                                              self.wnd_taskbar.TBPF_NOPROGRESS)
        except RuntimeError:
            pass

    def _reintentar_detener_hilos(self):
        u"""
        Solicita la finalización de todos los threads utilizados en la
        aplicación. Este método debe ser llamado al desconectarse o al salir
        de la aplicación.
        """
        for proc in multiprocessing.active_children():
            proc.terminate()

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
        self._logger.debug("Actualizar ventana")

        try:
            data_entrenar = self.get_all_from_queue(self.ql_entrenar_out_q)
            # self._logger.debug("[Entrenar] Actualizar ventana con: {0}".format(data_entrenar)) @IgnorePep8

            for ql_ent_info in data_entrenar:
                estado_actual = ql_ent_info.get('EstadoActual', None)
                nro_episodio = ql_ent_info.get('NroEpisodio', None)
                cant_iteraciones = ql_ent_info.get('NroIteracion', None)
                episode_exec_time = ql_ent_info.get('EpisodiosExecTime', 0.0)
                iter_exec_time = ql_ent_info.get('IteracionesExecTime', 0.0)
                worker_joined = ql_ent_info.get('ProcesoJoined', None)
                loop_alarm = ql_ent_info.get('LoopAlarm', None)
                matriz_q = ql_ent_info.get('MatrizQ', None)
                running_exec_time = ql_ent_info.get('RunningExecTime', 0.0)

                self._logger.debug("[Entrenar] Estado actual: {0}".format(estado_actual))
                self._logger.debug("[Entrenar] Episodio: {0}".format(nro_episodio))
                self._logger.debug("[Entrenar] Iteraciones: {0}".format(cant_iteraciones))
                self._logger.debug("[Entrenar] Tiempo ejecución episodio: {0}".format(episode_exec_time))
                self._logger.debug("[Entrenar] Tiempo ejecución iteración: {0}".format(iter_exec_time))
                self._logger.debug("[Entrenar] Tiempo ejecución total: {0}".format(running_exec_time))
                self._logger.debug("[Entrenar] Worker joined : {0}".format(worker_joined))
                # self._logger.debug("[Entrenar] Matriz Q: {0}".format(self.matriz_q))
                self._logger.debug("[Entrenar] Loop Alarm: {0}".format(loop_alarm))

                if matriz_q is not None:
                    self.matriz_q = matriz_q

                if loop_alarm is not None:
                    if loop_alarm:
                        QtGui.QMessageBox.warning(self,
                                                  _tr('QLearning - Entrenamiento'),
                        u"Se ha detectado que el Estado Final se encuentra bloqueado por lo que se cancelará el entrenamiento.")
                        self.working_process.join(0.05)
                        self.qlearning_entrenar_worker = None
                        self.working_process = None
                        self.ql_entrenar_error_q = None
                        self.ql_entrenar_out_q = None

                self.WMainWindow.lblEstadoActual.setText("X:{0}  Y:{1}"
                                                         .format(estado_actual[0],
                                                                 estado_actual[1]
                                                                 ))
                self.WMainWindow.lblNroEpisodio.setText(str(nro_episodio))
                self.WMainWindow.lblNroIteracion.setText(str(cant_iteraciones))
                self.WMainWindow.lblExecTimeEpisodios.setText("{0:.3f} seg  ({1:.2f} ms)"
                                                              .format(episode_exec_time,
                                                                      episode_exec_time * 1000))
                self.WMainWindow.lblExecTimeIteraciones.setText("{0:.3f} seg  ({1:.2f} ms)"
                                                                .format(iter_exec_time,
                                                                        iter_exec_time * 1000))
                self.WMainWindow.lblExecTimeTotal.setText("{0:.3f} seg  ({1:.2f} ms)"
                                                          .format(running_exec_time,
                                                                  running_exec_time * 1000))
        except Queue.Empty:
            pass
        except AttributeError:
            pass

        try:
            data_recorrer = self.get_all_from_queue(self.ql_recorrer_out_q)
            # self._logger.debug("[Recorrer] Actualizar ventana con: {0}".format(data_recorrer)) @IgnorePep8

            for ql_rec_info in data_recorrer:
                estado_actual = ql_rec_info.get('EstadoActual', None)
                camino_optimo = ql_rec_info.get('CaminoRecorrido', None)
                rec_exec_time = ql_rec_info.get('RunningExecTime', None)
                worker_joined = ql_rec_info.get('ProcesoJoined', None)

                self._logger.debug("[Recorrer] Estado actual: {0}".format(estado_actual))
                self._logger.debug("[Recorrer] Camino óptimo: {0}".format(camino_optimo))
                self._logger.debug("[Recorrer] Tiempo ejecución recorrido: {0}".format(rec_exec_time))
                self._logger.debug("[Recorrer] Worker joined: {0}".format(worker_joined))

                # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
                if camino_optimo is not None:
                    seen = set()
                    seen_add = seen.add
                    camino_optimo_sin_repetidos = [x for x in camino_optimo
                                                   if x not in seen and not seen_add(x)]

                    self._logger.debug("Camino óptimo (con repetidos): {0}"
                                  .format(camino_optimo))
                    self._logger.debug("Camino óptimo (sin repetidos): {0}".
                                  format(camino_optimo_sin_repetidos))
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
            while True:
                yield cola.get_nowait()
        except Queue.Empty:
            raise StopIteration

    def comprobar_actividad_procesos(self):
        u"""
        Comprueba si hay threads activos (sin incluir el MainThread). Si no
        existen threads activos se detiene el Timer de la ventana.
        """
        self._logger.debug("Comprobar actividad de procesos")

        for proc in multiprocessing.active_children():
            if not proc.is_alive():
                proc.join(0.05)
            self._logger.debug("Proceso hijo: {0}".format(proc))

        if len(multiprocessing.active_children()) == 0:
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
            self.window_config["item"]["size"] = self.GWOpcionesD.estado_size

            self.refresh_gw()

    def mostrar_gen_rnd_estados_dialog(self):
        self.GWGenRndEstValsD = GWGenRndEstadosDialog(self)
        if self.GWGenRndEstValsD.exec_():
            pass

    def inicializar_gw(self):
        # Cargar dimensiones posibles del tblGridWorld
        try:
            self.WMainWindow.cbGWDimension.currentIndexChanged.disconnect()
        except Exception:
            pass

        self.WMainWindow.cbGWDimension.clear()
        for dimension in self.gw_dimensiones:
            self.WMainWindow.cbGWDimension.addItem(_tr(dimension), dimension)

        self.WMainWindow.cbGWDimension.currentIndexChanged.connect(self.set_gw_dimension_cb)

        self.refresh_gw()

    def refresh_gw(self):
        # Establece la dimensión por defecto del tblGridWorld en 6x6
        self.set_gw_dimension(self.WMainWindow.cbGWDimension.itemData(0).toString())

    def inicializar_ql_vals(self):
        # Cargar técnicas posibles
        self.WMainWindow.cbQLTecnicas.clear()
        for key, value in self.tecnicas.items():
            self.WMainWindow.cbQLTecnicas.addItem(_tr(value), key)

        self.WMainWindow.cbQLTecnicas.setCurrentIndex(1)
        self.WMainWindow.sbQLEpsilon.setMinimum(0.01)
        self.WMainWindow.sbQLTau.setMinimum(0.01)
        self.WMainWindow.lblTau.hide()
        self.WMainWindow.sbQLTau.hide()

        # Establecer por defecto 1 episodio
        self.WMainWindow.sbCantidadEpisodios.setValue(1)

        # Establecer por defecto un Epsilon = 0.5
        self.WMainWindow.sbQLEpsilon.setValue(0.5)

        # Establecer por defecto un Gamma = 0.5
        self.WMainWindow.sbQLGamma.setValue(0.5)

        self.WMainWindow.sbDecrementoVal.setValue(0.01)
        self.WMainWindow.sbCantEpisodiosDec.setValue(1)
        self.WMainWindow.sbCantEpisodiosDec.setSuffix(_tr(" episodios"))
        self.WMainWindow.chkDecrementarParam.setChecked(True)
        self.WMainWindow.sbQLTau.setValue(0.5)

    def show_matriz_dialog(self, matriz, titulo_corto, titulo_largo):
        ShowMatrizD = ShowMatrizDialog(matriz,
                                       titulo_corto,
                                       titulo_largo,
                                       self)
        ShowMatrizD.exec_()

    def show_matriz_r(self):
        matriz_r = self.gridworld.get_matriz_r()
        print matriz_r
        self.show_matriz_dialog(matriz_r, "Matriz R", "Matriz de recompensas")

    def show_matriz_q(self):
        if self.matriz_q is not None:
            self.show_matriz_dialog(self.matriz_q, "Matriz Q", "Matriz Q")
