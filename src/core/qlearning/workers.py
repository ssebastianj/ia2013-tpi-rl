#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import Queue
import logging
import multiprocessing
import numpy
import time
import sys
import random
from core.estado.estado import TIPOESTADO


class QLearningEntrenarWorker(multiprocessing.Process):
    u"""
    Worker encargado de realizar el aprendizaje de Q-Learning.
    """
    def __init__(self, inp_queue, out_queue, error_q):
        """
        Inicializador del worker.

        :param inp_queue: Cola de entrada.
        :param out_queue: Cola de salida de datos.
        :param error_q: Cola de salida de errores.
        """
        super(QLearningEntrenarWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_q
        self._stoprequest = multiprocessing.Event()
        self.name = "QLearningEntrenarWorker"
        self.input_data = None
        self._visitados_1 = None
        self._visitados_2 = None
        self._contador_ref = None
        self.matriz_r = None
        self.matriz_q = None
        self.estados = None
        self.excluir_tipos_vecinos = None

        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG,
                            format="[%(levelname)s] – %(threadName)-10s : %(message)s")

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        logging.debug("En ejecución.")

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        logging.debug("Terminando.")
        self._inp_queue.close()
        self._error_queue.close()
        self._out_queue.close()

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        aprendizaje de Q-Learning.
        """
        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener matriz R y matriz Q
        try:
            self.input_data = self._inp_queue.get()
        except Queue.Empty:
            logging.debug("Cola de entrada vacía")
            return None

        self.estados = self.input_data[0]
        self.coordenadas = self.input_data[1]
        self.gamma = self.input_data[2]
        self.cant_episodios = self.input_data[3]
        self.tecnica = self.input_data[4]
        self.ancho, self.alto = self.input_data[5]
        self.detector_bloqueo = self.input_data[6]
        self.tipos_vec_excluidos = self.input_data[7]
        self.q_init_value_fn = self.input_data[8]

        self.matriz_r = self.get_matriz_r()
        self.matriz_q = self.get_matriz_q(self.matriz_r)

        logging.debug("Estados: {0}".format(self.estados))
        logging.debug("Coordenadas: {0}".format(self.coordenadas))
        logging.debug("Gamma: {0}".format(self.gamma))
        logging.debug("Episodios: {0}".format(self.cant_episodios))
        logging.debug("Técnica: {0}".format(self.tecnica))
        logging.debug("Ancho: {0} - Alto: [1]".format(self.ancho, self.alto))
        logging.debug("Usar detector bloqueo: {0}".format(self.detector_bloqueo))
        logging.debug("Tipos vecinos excluidos: {0}".format(self.tipos_vec_excluidos))

        if self.detector_bloqueo:
            self._contador_ref = self._crear_cont_ref(self.tipos_vec_excluidos)
            self._cant_estados_libres = len(self._contador_ref)
            self._visitados_1 = []
            self._visitados_2 = []

        if sys.platform == 'win32':
            _timer = time.clock
        else:
            _timer = time.time

        decrementar_step = 0
        # Ejecutar una cantidad dada de Episodios
        for epnum in xrange(1, self.cant_episodios + 1):
            # Registrar tiempo de comienzo del episodio
            ep_start_time = _timer()

            logging.debug("Numero de episodio: {0}".format(epnum))  # FIXME: Logging @IgnorePep8

            # Obtener coordenadas aleatorias y obtener Estado asociado
            x_act, y_act = self.generar_estado_aleatorio()

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las de un tipo excluido
            estado_actual = self.matriz_r[x_act - 1][y_act - 1]
            tipo_ide = estado_actual[0]
            while tipo_ide in self.tipos_vec_excluidos:
                x_act, y_act = self.generar_estado_aleatorio()
                estado_actual = self.matriz_r[x_act - 1][y_act - 1]
                tipo_ide = estado_actual[0]
                logging.debug("Estado inicial generado no válido: {0}"
                              .format((x_act, y_act)))
            logging.debug("Estado Inicial Generado: {0}".format(estado_actual))

            # Forzar restauración del valor de parámetro de la técnica
            # utilizada antes de comenzar un nuevo Episodio
            self.tecnica.restaurar_val_parametro()

            # Realizar 1 Episodio mientras no estemos en el Estado Final
            cant_iteraciones = 0
            while (not self._stoprequest.is_set()) and (not estado_actual[0] == TIPOESTADO.FINAL):
                # Registrar tiempo de comienzo de las iteraciones
                iter_start_time = _timer()

                if self.detector_bloqueo:
                    self._contar_ref((x_act, y_act))

                # Obtener vecinos del estado actual
                vecinos = estado_actual[1]
                logging.debug("Vecinos Estado Actual: {0}".format(vecinos))
                # Invocar a la técnica para que seleccione uno de los vecinos
                estado_elegido = self.tecnica.obtener_accion(vecinos)
                logging.debug("Estado Elegido: {0}".format(estado_elegido))
                x_eleg, y_eleg = estado_elegido

                recompensa_estado = vecinos[(x_eleg, y_eleg)]

                # Obtener vecinos del estado elegido por la acción
                vecinos_est_elegido = self.matriz_q[x_eleg - 1][y_eleg - 1][1]
                logging.debug("Vecinos Elegidos del Elegido: {0}"
                              .format(vecinos_est_elegido))

                max_q = max([q_val for q_val in vecinos_est_elegido.values()])

                # Fórmula principal de Q-Learning
                # -------------------------------
                if recompensa_estado is not None:
                    logging.debug("Gamma: {0}".format(self.gamma))
                    nuevo_q = recompensa_estado + (self.gamma * max_q)
                    # Actualizar valor de Q en matriz Q
                    self.matriz_q[x_act - 1][y_act - 1][1][(x_eleg, y_eleg)] = nuevo_q

                cant_iteraciones += 1

                logging.debug("Valor parámetro: {0}"
                              .format(self.tecnica._val_param_parcial))  # FIXME: Logging @IgnorePep8
                logging.debug("Iteraciones {0}".format(cant_iteraciones))  # FIXME: Logging @IgnorePep8
                logging.debug("Matriz Q: {0}".format(self.matriz_q))  # FIXME: Logging @IgnorePep8

                try:
                    self._out_queue.put({'EstAct': (x_act, y_act),
                                         'NoEp': epnum,
                                         'CantIter': cant_iteraciones,
                                         'Joined': False})
                except Queue.Full:
                    logging.debug("Cola llena")
                    pass

                # Actualizar estado actual
                (x_act, y_act) = (x_eleg, y_eleg)
                estado_actual = self.matriz_r[x_act - 1][y_act - 1]

            decrementar_step += 1
            # Comprobar si es necesario decrementar el valor del parámetro
            if self.tecnica.intervalo_decremento == decrementar_step:
                # Decrementar valor del parámetro en 1 paso
                self.tecnica.decrementar_parametro()
                decrementar_step = 0

            iter_end_time = _timer()
            ep_end_time = _timer()

            # Calcular tiempo de ejecución del episodio
            ep_exec_time = ep_end_time - ep_start_time
            # Calcular tiempo de ejecución de las iteraciones
            iter_exec_time = iter_end_time - iter_start_time

            # Poner en la cola de salida los resultados
            try:
                self._out_queue.put({'EstAct': (x_act, y_act),
                                     'NoEp': epnum,
                                     'CantIter': cant_iteraciones,
                                     'MatQ': self.matriz_q,
                                     'EpExecT': ep_exec_time,
                                     'IterExecT': iter_exec_time,
                                     'Joined': False})
            except Queue.Full:
                logging.debug("Cola llena")
                pass

            # Verificar si se solicitó externamente finalizar el thread
            if self._stoprequest.is_set():
                break

        # Poner en cola un valor booleano para indicar que se finalizó el trabajo
        # self._out_queue.put(True)
        # Realizar tareas al finalizar
        self._on_end()

    def generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        alto, ancho = self.input_data[5]
        return (random.randint(1, ancho), random.randint(1, alto))

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        logging.debug("Join")
        self._stoprequest.set()
        self._out_queue.put({'Joined': True})
        super(QLearningEntrenarWorker, self).join(timeout)

    def _crear_cont_ref(self, tipos_vec_exc):
        matriz_q = self.input_data[1]
        tipos_vec_exc.append(TIPOESTADO.FINAL)

        contador_ref = {}
        for i, fila in enumerate(matriz_q):
            for j, columna in enumerate(fila):
                if columna[0] not in tipos_vec_exc:
                    contador_ref[(i + 1, j + 1)] = 0

        logging.debug("Contador de referencias: {0}".format(contador_ref))
        return contador_ref

    def _contar_ref(self, estado):
        umbral_1 = 1
        umbral_2 = 2

        self._contador_ref[estado] += 1
        cont = self._contador_ref[estado]

        if cont == umbral_1:
            self._visitados_1.append(estado)
        elif cont == umbral_2:
            self._visitados_2.append(estado)

        logging.debug("Contador de referencias actualizado: {0}"
                          .format(self._contador_ref))
        logging.debug("Visitados 1: {0}".format(self._visitados_1))
        logging.debug("Visitados 2: {0}".format(self._visitados_2))

        self._comprobar_visitados()

    def _comprobar_visitados(self):
        test_1 = len(self._visitados_1) == self._cant_estados_libres
        test_2 = len(self._visitados_1) == len(self._visitados_2)

        if test_1 or test_2:
            self._out_queue.put({'LoopAlarm': True})

    def get_matriz_r(self):
        u"""
        Crea y devuelve la matriz R de recompensa en en función de la ubicación de los estados
        y sus vecinos. Representa las transiciones posibles.
        """
        # Verificar si hay tipos de vecinos a excluir de la matriz R
        if self.excluir_tipos_vecinos is None:
            self.excluir_tipos_vecinos = []

        matriz_r = numpy.empty((self.alto, self.ancho), object)
        # Crear una lista de listas
        for i in xrange(1, self.alto + 1):
            fila = []
            for j in xrange(1, self.ancho + 1):
                # Obtener estado actual y su ID de tipo
                estado = self.get_estado(i, j)
                estado_ide = estado.tipo.ide
                # Obtener los estados vecinos del estado actual (i, j)
                vecinos = self.get_vecinos_estado(i, j)
                # Agregar vecinos y su recompensa al estado
                # excluyendo los prohibidos
                recomp_and_vec = {}

                for vecino in vecinos:
                    if vecino.tipo.ide not in self.excluir_tipos_vecinos:
                        recomp_and_vec[(vecino.fila, vecino.columna)] = vecino.tipo.recompensa

                fila.append((estado_ide, recomp_and_vec))
            matriz_r[i - 1] = fila
        return matriz_r

    def get_matriz_q(self, matriz_r):
        u"""
        Crea la matriz Q con un valor inicial.

        :param default: Valor con que se inicializa cada estado de la matriz.
        """
        matriz_q = numpy.empty((self.ancho, self.alto), object)

        for i in xrange(0, self.alto):
            for j in xrange(0, self.ancho):
                tipo_estado = matriz_r[i][j][0]
                vecinos = matriz_r[i][j][1]
                vecinos = dict([(key, self.q_init_value_fn.procesar_valor(value))
                                for key, value in vecinos.iteritems()])
                matriz_q[i][j] = (tipo_estado, vecinos)
        return matriz_q

    def get_vecinos_estado(self, x, y):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila del estado
        :param y: Columna del estado
        """
        vecinos = []
        for fila, columna in ((x + i, y + j)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if i != 0 or j != 0):
            if (fila, columna) in self.coordenadas:
                vecinos.append(self.get_estado(fila, columna))
        return numpy.array(vecinos, object)

    def get_estado(self, x, y):
        u"""
        Devuelve un estado dadas sus coordenadas.

        :param x: Fila del estado
        :param y: Columna del estado
        """
        return self.estados[x - 1][y - 1]


class QLearningRecorrerWorker(multiprocessing.Process):
    u"""
    Worker encargado de recorrer el GridWorld utilizando la matriz Q para seguir
    el mejor camino hasta el Estado Final.
    """
    def __init__(self, inp_queue, out_queue, error_queue):
        u"""
        Inicializador de QLearningRecorrerWorker.

        :param inp_queue: Cola de entrada.
        :param out_queue: Cola de salida de datos.
        :param error_queue: Cola de salida de errores.
        """
        super(QLearningRecorrerWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_queue
        self._stoprequest = multiprocessing.Event()
        self.name = "QLearningRecorrerWorker"
        self.input_data = None
        self._contador_ref = {}
        self._visitados = []

        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG,
                            format="[%(levelname)s] – %(threadName)-10s : %(message)s")  # @IgnorePep8

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        logging.debug("En ejecución.")

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        logging.debug("Terminando.")
        self._inp_queue.close()
        self._error_queue.close()
        self._out_queue.close()

    def run(self):
        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener la referencia a la instancia desde la cola de entrada
        try:
            self.input_data = self._inp_queue.get()
        except Queue.Empty:
            logging.debug("Cola de entrada vacía")
            return None

        matriz_q = self.input_data[0]
        estado_inicial = self.input_data[1]

        logging.debug("Matriz Q: {0}".format(matriz_q))
        logging.debug("Estado Inicial: {0}".format(estado_inicial))

        # Lista que contiene la secuencia de estados comenzando por el
        # Estado Inicial
        camino_optimo = [estado_inicial]

        if sys.platform == 'win32':
            _timer = time.clock
        else:
            _timer = time.time

        # Registrar tiempo de comienzo
        rec_start_time = _timer()
        x_act, y_act = estado_inicial
        estado_actual = matriz_q[x_act - 1][y_act - 1]
        while (not self._stoprequest.is_set()) and (not estado_actual[0] == TIPOESTADO.FINAL):
            vecinos = estado_actual[1]
            vecinos = dict([(key, value) for key, value in vecinos.iteritems()
                            if key not in self._visitados])

            # Buscar el estado que posea el mayor valor de Q
            maximo = None
            estados_qmax = []
            for key, value in vecinos.items():
                logging.debug("X:{0} Y:{1}".format(key[0], key[1]))  # FIXME: Eliminar print de debug
                q_valor = value
                logging.debug("Q Valor: {0}".format(q_valor))  # FIXME: Eliminar print de debug

                if maximo is None:
                    maximo = q_valor

                if q_valor > maximo:
                    maximo = q_valor
                    estados_qmax = [key]
                elif q_valor == maximo:
                    estados_qmax.append(key)

            # Comprobar si hay estados con valores Q iguales y elegir uno
            # de forma aleatoria
            if len(estados_qmax) == 1:
                estado_qmax = estados_qmax[0]
                logging.debug("Existe un sólo estado vecino con Q máximo")  # FIXME: Eliminar print de debug @IgnorePep8
            else:
                estado_qmax = random.choice(estados_qmax)
                logging.debug("Existen varios estados con igual valor Q")  # FIXME: Eliminar print de debug @IgnorePep8

            logging.debug("Estado Q Máximo: {0}".format(estado_qmax))
            x_eleg, y_eleg = estado_qmax

            # Marcar como visitado
            self._contar_ref((x_eleg, y_eleg))

            # Agregar estado al camino óptimo
            camino_optimo.append(estado_qmax)

            try:
                self._out_queue.put({'EstAct': (x_act, y_act), 'Joined': False})
            except Queue.Full:
                logging.debug("Cola llena")
                pass

            # Actualizar estado actual
            x_act, y_act = (x_eleg, y_eleg)
            estado_actual = matriz_q[x_act - 1][y_act - 1]

        # Registrar tiempo de finalización
        rec_end_time = _timer()
        rec_exec_time = rec_end_time - rec_start_time

        logging.debug("Camino óptimo: {0}".format(camino_optimo))

        # Encolar la información generada por el algoritmo para realizar
        # estadísticas
        try:
            self._out_queue.put({'EstAct': (x_act, y_act),
                                 'OptPath': camino_optimo,
                                 'RecExecT': rec_exec_time,
                                 'Joined': False})
        except Queue.Full:
            logging.debug("Cola llena")
            pass

        # Poner en cola un valor booleano para indicar que se finalizó el trabajo
        # self._out_queue.put(True)
        # Realizar tareas al finalizar
        self._on_end()

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        logging.debug("Join")
        self._out_queue.put({'Joined': True})
        self._stoprequest.set()
        super(QLearningRecorrerWorker, self).join(timeout)

    def _contar_ref(self, estado):
        umbral = 1

        if self._contador_ref.has_key(estado):
            self._contador_ref[estado] += 1
        else:
            self._contador_ref[estado] = 0

        if self._contador_ref[estado] == umbral:
            self._visitados.append(estado)

        logging.debug("Contador de referencias actualizado: {0}"
                          .format(self._contador_ref))
        logging.debug("Visitados: {0}".format(self._visitados))
