#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import Queue
import threading

from PyQt4 import QtCore, QtGui

from gui.genrndvalsdialog import GenRndValsDialog
from gui.qtgen.mainwindow import Ui_MainWindow

from core.estado.estado import TIPOESTADO
from core.gridworld.gridworld import GridWorld
from core.qlearning.qlearning import QLearning
from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax
from core.tecnicas.aleatorio import Aleatorio

from tools.livedatafeed import LiveDataFeed
from tools.queue import get_all_from_queue, get_item_from_queue
from tools.listacircular import ListaCircular


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
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")

        self.WMainWindow = Ui_MainWindow()
        self.WMainWindow.setupUi(self)

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
        self.wnd_timer = None
        self.ql_entrenar_error_q = None
        self.ql_entrenar_out_q = None
        self.ql_recorrer_error_q = None
        self.ql_recorrer_out_q = None
        self.tecnicas = {0: "Greedy",
                         1: "ε-Greedy",
                         2: "Softmax",
                         3: "Aleatorio"}
        self.gw_dimensiones = ["2 x 2", "3 x 3", "4 x 4", "5 x 5", "6 x 6",
                               "7 x 7", "8 x 8", "9 x 9", "10 x 10"]
        self.window_config = {"item":
                              {"show_tooltip": True,
                               "menu_estado":
                                    {"ocultar_tipos":
                                     [TIPOESTADO.AGENTE],
                                     "enabled": True}}}

    def _initialize_window(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        # Aspectos de la ventana principal
        self.setWindowIcon(QtGui.QIcon('img/96x96.png'))

        # Cargar técnicas posibles
        self.WMainWindow.cbQLTecnicas.clear()
        for key, value in self.tecnicas.items():
            self.WMainWindow.cbQLTecnicas.addItem(_tr(value), key)

        self.WMainWindow.cbQLTecnicas.setCurrentIndex(1)
        self.WMainWindow.sbQLEpsilon.setMinimum(0.01)
        self.WMainWindow.sbQLTau.setMinimum(0.01)
        self.WMainWindow.lblTau.hide()
        self.WMainWindow.sbQLTau.hide()

        # Cargar dimensiones posibles del tblGridWorld
        self.WMainWindow.cbGWDimension.clear()
        for dimension in self.gw_dimensiones:
            self.WMainWindow.cbGWDimension.addItem(_tr(dimension), dimension)

        # Establece la dimensión por defecto del tblGridWorld en 6x6
        self.set_gw_dimension_cb(self.WMainWindow.cbGWDimension.currentIndex())

        # Establecer por defecto 1 episodio
        self.WMainWindow.sbCantidadEpisodios.setValue(1)

        # Establecer por defecto un Epsilon = 0.5
        self.WMainWindow.sbQLEpsilon.setValue(0.5)

        # Establecer por defecto un Gamma = 0.5
        self.WMainWindow.sbQLGamma.setValue(0.5)

        self.lbl_item_actual = QtGui.QLabel()
        self.WMainWindow.statusBar.addPermanentWidget(self.lbl_item_actual)

        self.WMainWindow.tblGridWorld.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.WMainWindow.tblGridWorld.setSortingEnabled(False)
        self.WMainWindow.tblGridWorld.setMouseTracking(True)
        self.setMouseTracking(True)

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
        # Obtener ancho y alto del GridWorld
        logging.debug(dimension)
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

        # Desactivar actualización de la tabla para optimizar la carga
        self.WMainWindow.tblGridWorld.setUpdatesEnabled(False)
        # Rellenar tabla con items
        for fila in range(0, self.gridworld.alto):
            for columna in range(0, self.gridworld.ancho):
                estado = self.gridworld.get_estado(fila + 1, columna + 1)
                letra_estado = estado.tipo.letra
                # Cada item muestra la letra asignada al estado
                item = QtGui.QTableWidgetItem(str(letra_estado))
                item.setBackgroundColor(QtGui.QColor(estado.tipo.color))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
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
        # Solicita la generación de valores aleatorio
        self.WMainWindow.btnGenValAleatorios.clicked.connect(self.mostrar_dialogo_gen_rnd_vals)
        self.WMainWindow.btnInicializar.clicked.connect(self.inicializar_todo)
        self.WMainWindow.btnRecorrer.clicked.connect(self.recorrer_gw)
        # Emite cuando se coloca el cursor del mouse sobre un ítem
        self.WMainWindow.tblGridWorld.itemEntered.connect(self.mostrar_item_actual)
        self.WMainWindow.menuGridWorld.aboutToShow.connect(self.generar_menu_dimensiones)
        self.WMainWindow.menuQLearning.aboutToShow.connect(self.generar_menu_tecnicas)
        self.WMainWindow.menuGridWorld.triggered.connect(self.set_gw_dimension_menu)
        self.WMainWindow.menuQLearning.triggered.connect(self.parametros_segun_tecnica_menu)

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
                    if self.estado_final is not None:
                        action.setEnabled(False)
                    else:
                        action.setEnabled(True)
                elif tipo.ide == TIPOESTADO.INICIAL:
                    if self.estado_inicial is not None:
                        action.setEnabled(False)
                    else:
                        action.setEnabled(True)

        # Mostrar el menú y obtener el item de menu clickeado
        action = self.menu_item.exec_(self.WMainWindow.tblGridWorld.mapToGlobal(posicion))

        if action is not None:
            # Obtener el tipo de estado asociado al texto clickeado
            tipo_num = action.data().toInt()[0]
            # Averiguar en cual item de la tabla se hizo clic
            item = self.WMainWindow.tblGridWorld.itemAt(posicion)
            # Actualizar texto del item de la tabla en función del tipo de estado
            item.setText(tipos_estados[tipo_num].letra)
            # Establecer color de fondo de acuerdo al tipo de estado
            item.setBackgroundColor(QtGui.QColor(tipos_estados[tipo_num].color))
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
                intervalo_decremento = self.WMainWindow.sbCantIteracionesDec.value()
                tecnica.paso_decremento = paso_decremento
                tecnica.intervalo_decremento = intervalo_decremento
        # ----------- Fin de seteo de la técnica --------------

        gamma = self.WMainWindow.sbQLGamma.value()
        cant_episodios = int(self.WMainWindow.sbCantidadEpisodios.value())
        valor_inicial = 0

        # Crear nueva instancia de Q-Learning
        self.qlearning = QLearning(self.gridworld,
                                   gamma,
                                   tecnica,
                                   cant_episodios,
                                   valor_inicial)

        logging.debug("Matriz Q Inicial: {0}".format(self.qlearning.matriz_q))

        # QLearningEntrenarWorker Management
        # Que empiece la magia
        # FIXME: Ejecución concurrente Entrenamiento
        self.ql_entrenar_out_q = Queue.Queue()
        self.ql_entrenar_error_q = Queue.Queue()
        self.qlearning_entrenar_worker = self.qlearning.entrenar(self.ql_entrenar_out_q,
                                                                 self.ql_entrenar_error_q)

        logging.debug("Nuevo Thread: {0}".format(self.qlearning_entrenar_worker))

        worker_error = get_item_from_queue(self.ql_entrenar_error_q)
        if worker_error is not None:
            logging.debug("Error {0}: ".format(worker_error))
            self.qlearning_entrenar_worker = None

        if self.qlearning_entrenar_worker is not None:
            self.WMainWindow.statusBar.showMessage(_tr("Entrenando agente..."))
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

        self.ql_recorrer_out_q = Queue.Queue()
        self.ql_recorrer_error_q = Queue.Queue()
        self.qlearning_recorrer_worker = self.qlearning.recorrer(self.estado_inicial,
                                                                 self.ql_recorrer_out_q,
                                                                 self.ql_recorrer_error_q)

        logging.debug("Nuevo Thread: {0}".format(self.qlearning_recorrer_worker))

        worker_error = get_item_from_queue(self.ql_recorrer_error_q)
        if worker_error is not None:
            logging.debug("Error {0}: ".format(worker_error))
            self.qlearning_recorrer_worker = None

        if self.qlearning_recorrer_worker is not None:
            self.WMainWindow.statusBar.showMessage(_tr("Agente buscando camino óptimo..."))
            self.on_comienzo_proceso()

    def terminar_proceso(self):
        u"""
        Ejecutar tareas al finalizar un thread.
        """
        logging.debug("Detener {0}: ".format(self.qlearning_entrenar_worker))
        self.qlearning_entrenar_worker.join(0.05)
        logging.debug(self.qlearning_entrenar_worker)
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
        logging.debug("Timeout")
        self.comprobar_colas()
        self.actualizar_window()
        self.comprobar_actividad_threads()

    def on_comienzo_proceso(self):
        u"""
        Ejecutar tareas al ejecutar un thread.
        """
        logging.debug("Comienzo del proceso")
        # Crear Timer asociado a la ventana principal
        self.wnd_timer = QtCore.QTimer()
        # Conectar disparo de timer con método
        self.wnd_timer.timeout.connect(self._on_window_timer)
        self.wnd_timer.start(100)

    def on_fin_proceso(self):
        u"""
        Ejecuta tareas al finalizar la ejecución de un thread/proceso.
        """
        # Detener Timer asociado a la ventana principal
        self.wnd_timer.stop()

        # Habilitar GridWorld
        self.window_config["item"]["menu_estado"]["enabled"] = True
        self.window_config["item"]["show_tooltip"] = True

        self.WMainWindow.statusBar.clearMessage()

        logging.debug("Estos son los valores de la matriz Q")
        print self.qlearning.matriz_q

    def _reintentar_detener_hilos(self):
        u"""
        Solicita la finalización de todos los threads utilizados en la
        aplicación. Este método debe ser llamado al desconectarse o al salir
        de la aplicación.

        Fuente: http://pymotw.com/2/threading/
        """
        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is not main_thread and t.is_alive():
                t.join(0.01)

    def mostrar_dialogo_gen_rnd_vals(self):
        u"""
        Instancia y muestra el diálogo para generar valores aleatorios.
        """
        self.GenRndValsD = GenRndValsDialog(self)
        if self.GenRndValsD.exec_():
            pass

    def inicializar_todo(self):
        u"""
        Reestablece los valores por defecto de varios controles de la UI
        e inicializa variables internas del programa.
        """
        self.WMainWindow.cbGWDimension.currentIndexChanged[str].disconnect(self.set_gw_dimension)
        self._init_vars()
        self._initialize_window()

    def mostrar_dialogo_acerca(self):
        u"""
        Muestra el cuadro de diálogo Acerca de...
        """
        # TODO: Implementar AboutDialog
        self.AboutD = AboutDialog(self)
        self.AboutD.show()

    def closeEvent(self, event):
        """
        Reimplementa el evento 'closeEvent' de la clase padre.

        :param event: Evento.
        """
        self._reintentar_detener_hilos()

    def exit(self):
        u"""
        Finaliza la ejecución de la aplicación.
        """
        self.close()

    def leer_ql_input(self, cola):
        u"""
        Lee los datos del worker desde la cola de salida del mismo.

        :param cola: Cola de salida del worker.
        """
        ql_datos_in = list(get_all_from_queue(cola))
        logging.debug("Leer QL Input: {0}".format(ql_datos_in))
        if len(ql_datos_in) > 0:
            self.ql_datos_entrenar_in_feed.add_data(ql_datos_in)
            logging.debug("Datos IN: {0}".format(ql_datos_in))

    def actualizar_window(self):
        u"""
        Actualiza la información mostrada en la ventana de acuerdo a los
        datos de entrada,
        """
        logging.debug("Actualizar ventana")
        if self.ql_datos_entrenar_in_feed.has_new_data:
            data_entrenar = self.ql_datos_entrenar_in_feed.read_data()
            logging.debug("Actualizar ventana con: {0}".format(data_entrenar))

        if self.ql_datos_recorrer_in_feed.has_new_data:
            data_recorrer = self.ql_datos_recorrer_in_feed.read_data()
            logging.debug("Actualizar ventana con: {0}".format(data_recorrer))


            ultima_info = data_recorrer[-1]
            camino_optimo = [(i.fila, i.columna) for i in ultima_info[1]]

            # http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
            seen = set()
            seen_add = seen.add
            camino_optimo_sin_repetidos = [ x for x in camino_optimo
                                           if x not in seen and not seen_add(x)]

            logging.debug("Camino óptimo (con repetidos): {0}"
                          .format(camino_optimo))
            logging.debug("Camino óptimo (sin repetidos): {0}".
                          format(camino_optimo_sin_repetidos))

    def comprobar_colas(self):
        u"""
        Comprueba si hay datos en las colas de entrada y salida y actúa acorde.
        """
        logging.debug("Comprobar colas")
        if self.ql_entrenar_out_q is not None:
            logging.debug("Comprobar cola QLearning Entrenar: {0}"
                          .format(self.ql_entrenar_out_q))
            self.leer_ql_input(self.ql_entrenar_out_q)

        if self.ql_recorrer_out_q is not None:
            logging.debug("Comprobar cola QLearning Recorrer: {0}"
                          .format(self.ql_recorrer_out_q))
            self._procesar_info_ql_recorrido(self.ql_recorrer_out_q)

    def comprobar_actividad_threads(self):
        u"""
        Comprueba si hay threads activos (sin incluir el MainThread). Si no
        existen threads activos se detiene el Timer de la ventana.
        """
        logging.debug("Comprobar actividad threads")
        main_thread = threading.current_thread()
        active_threads = threading.enumerate()

        cant_active_threads = 0
        for t in active_threads:
            if t is not main_thread:
                cant_active_threads += 1

        if cant_active_threads == 0:
            logging.debug("No hay threads activos. Detener Window Timer.")
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
        logging.debug(dimension)
        indice = self.WMainWindow.cbGWDimension.findData(dimension)
        self.WMainWindow.cbGWDimension.setCurrentIndex(indice)
        self.set_gw_dimension(dimension)

    def set_gw_dimension_cb(self, indice):
        dimension = self.WMainWindow.cbGWDimension.itemData(indice).toString()
        logging.debug(dimension)
        self.set_gw_dimension(dimension)

    def parametros_segun_tecnica_menu(self, action):
        indice = action.data().toInt()[0]
        self.WMainWindow.cbQLTecnicas.setCurrentIndex(indice)

    def generar_menu_dimensiones(self):
        logging.debug("Generar Menú Dimensiones")
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
        logging.debug("Generar Menú Técnicas")
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

    def _procesar_info_ql_recorrido(self, cola):
        ql_datos_in = list(get_all_from_queue(cola))
        logging.debug("Leer QL Input: {0}".format(ql_datos_in))
        if len(ql_datos_in) > 0:
            self.ql_datos_recorrer_in_feed.add_data(ql_datos_in)
            logging.debug("Datos IN: {0}".format(ql_datos_in))
