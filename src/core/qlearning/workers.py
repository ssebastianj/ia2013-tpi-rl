#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import Queue
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
        self.tipos_vec_excluidos = None

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        # Cerrar Queues
        self._inp_queue.close()
        self._error_queue.close()
        self._out_queue.close()

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        aprendizaje de Q-Learning.
        """
        # En Windows se obtiene mayor precisión al utilizar clock()
        # En UNIX conviene utilizar time()
        if sys.platform == 'win32':
            wtimer = time.clock
        else:
            wtimer = time.time

        # Registrar tiempo de comienzo
        running_start_time = wtimer()

        # Realizar tareas al comienzo
        self._do_on_start()

        # Procesar datos de entrada
        self.procesar_entrada()

        if self.detector_bloqueo:
            self._contador_ref = self._crear_cont_ref(self.tipos_vec_excluidos)
            self._cant_estados_libres = len(self._contador_ref)
            self._visitados_1 = []
            self._visitados_2 = []

        # Variable utilizada para saber cuando decrementar el parámetro de la técnica
        decrementar_step = 0

        # Descontador utilizado para saber en que momento calcular la diferencia
        # entre dos matrices Q
        calc_mat_diff_cont = self.interv_diff_calc - 1

        # Variables auxiliar para resguardar los resultados de las sumas
        suma_matriz_q_actual = None
        suma_matriz_q_anterior = None

        min_diff_mat = self.min_diff_mat  # Diferencia mínima entre matrices
        # Diferencia mínima temporal entre matrices (calculada)
        # Se le suma 1 para que la condición para entrar en el bucle 'while'
        # se cumpla al comenzar
        tmp_diff_mat = min_diff_mat + 1
        cantidad_episodios = self.cant_episodios  # Cantidad de episodios a ejecutar
        epnum = 1  # Inicializar número de episodio

        # Registrar tiempo de comienzo de los episodios
        ep_start_time = wtimer()

        # Ejecutar una cantidad dada de episodios o detener antes si se considera necesario
        while (not self._stoprequest.is_set()) and (epnum <= cantidad_episodios) and (tmp_diff_mat > min_diff_mat):

            # Obtener coordenadas aleatorias y obtener Estado asociado
            x_act, y_act = self.generar_estado_aleatorio()

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las de un tipo excluido
            estado_actual = self.matriz_r[x_act - 1][y_act - 1]
            tipo_estado = estado_actual[0]

            while tipo_estado in self.tipos_vec_excluidos:
                x_act, y_act = self.generar_estado_aleatorio()
                estado_actual = self.matriz_r[x_act - 1][y_act - 1]
                tipo_estado = estado_actual[0]

            # Recorrer hasta encontrar el estado final
            cant_iteraciones = 1
            while (not self._stoprequest.is_set()) and (estado_actual[0] != TIPOESTADO.FINAL):
                # Registrar tiempo de comienzo de las iteraciones
                iter_start_time = wtimer()

                # TODO: Utilizar detector de bloqueos
                if self.detector_bloqueo:
                    self._contar_ref((x_act, y_act))

                # Obtener vecinos del estado actual
                vecinos = estado_actual[1]
                # Invocar a la técnica para que seleccione uno de los vecinos
                estado_elegido = self.tecnica.obtener_accion(vecinos)
                # Asignar coordenadas X,Y
                x_eleg, y_eleg = estado_elegido

                # Obtener recompensa inmediata del estado actual
                recompensa_estado = vecinos[(x_eleg, y_eleg)]

                # Obtener vecinos del estado elegido por la acción
                vecinos_est_elegido = self.matriz_q[x_eleg - 1][y_eleg - 1][1]

                # Calcular el máximo valor Q de todos los vecinos
                max_q = max([q_val for q_val in vecinos_est_elegido.values()])

                # -------------------------------------------------------------
                # Fórmula principal de Q-Learning
                # -------------------------------------------------------------
                try:
                    nuevo_q = recompensa_estado + (self.gamma * max_q)
                    # Actualizar valor de Q en matriz Q
                    self.matriz_q[x_act - 1][y_act - 1][1][(x_eleg, y_eleg)] = nuevo_q
                except TypeError:
                    pass
                except ValueError:
                    pass

                self.encolar_salida({'EstadoActual': (x_act, y_act),
                                     'NroEpisodio': epnum,
                                     'NroIteracion': cant_iteraciones,
                                     'ValorParametro': self.tecnica.valor_param_parcial,
                                     'ProcesoJoined': False
                                      })

                # Actualizar estado actual
                x_act, y_act = (x_eleg, y_eleg)
                estado_actual = self.matriz_r[x_act - 1][y_act - 1]

                # Comprobar si se alcanzó el número máximo de iteraciones
                if self.limitar_iteraciones and (self.cant_max_iter == cant_iteraciones):
                    # Terminar y comenzar en un episodio nuevo
                    self.encolar_salida({'CorteIteracion': epnum})
                    break

                # Incrementar cantidad de iteraciones realizadas
                cant_iteraciones += 1
                # ==================== Fin de iteraciones ====================

            iter_end_time = wtimer()

            try:
                # Calcular tiempo de ejecución de las iteraciones
                iter_exec_time = iter_end_time - iter_start_time
            except UnboundLocalError:
                iter_exec_time = 0

            decrementar_step += 1
            # Comprobar si es necesario decrementar el valor del parámetro
            if self.tecnica.intervalo_decremento == decrementar_step:
                # Decrementar valor del parámetro en 1 paso
                self.tecnica.decrementar_parametro()
                decrementar_step = 0

            if calc_mat_diff_cont == 0:
                try:
                    # Sumar todos los valores Q de la matriz actual
                    suma_matriz_q_actual = numpy.sum([elto for fila in self.matriz_q
                                                           for columna in fila
                                                           for elto in columna[1].itervalues()])

                    # Restar valores de ambas matrices
                    resta_diff_mat = numpy.subtract(suma_matriz_q_anterior,
                                                    suma_matriz_q_actual)

                    # Calcular el error medio cuadrático
                    # tmp_diff_mat = numpy.true_divide(numpy.power(resta_diff_mat, 2), 2)
                    tmp_diff_mat = numpy.absolute(resta_diff_mat)

                    # Volver a cargar valor inicial a contador
                    calc_mat_diff_cont = self.interv_diff_calc
                except TypeError:
                    pass
            elif calc_mat_diff_cont == 1:
                # Sumar todos los valores Q de la matriz actual
                suma_matriz_q_anterior = numpy.sum([elto for fila in self.matriz_q
                                                         for columna in fila
                                                         for elto in columna[1].itervalues()])

            # Poner en la cola de salida los resultados
            self.encolar_salida({'EstadoActual': (x_act, y_act),
                                 'NroEpisodio': epnum,
                                 'NroIteracion': cant_iteraciones,
                                 'IteracionesExecTime': iter_exec_time,
                                 'ValorParametro': self.tecnica.valor_param_parcial,
                                 'ProcesoJoined': False,
                                 'MatDiff': tmp_diff_mat
                                 })

            # Decrementar contador para saber si es necesario calcular
            # la diferencia entre las matrices Q
            calc_mat_diff_cont -= 1

            # Avanzar un episodio
            epnum += 1
            # ======================= Fin de episodios =======================

        # Calcular tiempos de finalización
        running_end_time = ep_end_time = wtimer()

        try:
            ep_exec_time = ep_end_time - ep_start_time
            running_exec_time = running_end_time - running_start_time
        except UnboundLocalError:
            ep_exec_time = 0
            running_exec_time = 0

        # Poner en la cola de salida los resultados
        self.encolar_salida({'EstadoActual': (x_act, y_act),
                             'NroEpisodio': epnum - 1,
                             'NroIteracion': cant_iteraciones,
                             'MatrizQ': self.matriz_q,
                             'EpisodiosExecTime': ep_exec_time,
                             'IteracionesExecTime': iter_exec_time,
                             'ProcesoJoined': False,
                             'ValorParametro': self.tecnica.valor_param_parcial,
                             'RunningExecTime': running_exec_time,
                             'MatDiff': tmp_diff_mat
                             })

        # Realizar tareas al finalizar
        self._on_end()

    def encolar_salida(self, salida):
        u"""
        Colocar los resultandos del procesamiento en la cola de salida.

        :param salida: Información a colocar en la cola.
        """
        try:
            self._out_queue.put(salida)
        except Queue.Full:
            pass

    def encolar_errores(self, error):
        u"""
        Colocar los mensajes de errore en la cola de errores.

        :param error: Mensaje de error a colocar en la cola.
        """
        try:
            self._error_queue.put(error)
        except Queue.Full:
            pass

    def procesar_entrada(self):
        u"""
        Recibe e inicializa los datos de entradas que se utilizarán en el
        entrenamiento.
        """
        # Obtener matriz R y matriz Q
        try:
            self.input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None

        # Obtener valores de entrada
        self.estados = self.input_data[0]
        self.coordenadas = self.input_data[1]
        self.gamma = self.input_data[2]
        self.cant_episodios = self.input_data[3]
        self.limitar_iteraciones, self.cant_max_iter = self.input_data[4]
        self.tecnica_pack = self.input_data[5]
        self.ancho, self.alto = self.input_data[6]
        self.detector_bloqueo = self.input_data[7]
        self.tipos_vec_excluidos = self.input_data[8]
        self.q_init_value_fn = self.input_data[9]
        self.min_diff_mat, self.interv_diff_calc = self.input_data[10]

        self.matriz_r = self.get_matriz_r()
        self.matriz_q = self.get_matriz_q(self.matriz_r)
        self.tecnica = self.tecnica_pack[0](self.tecnica_pack[1],
                                            self.tecnica_pack[2],
                                            self.tecnica_pack[3])

    def generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        # Devolver un estado seleccionado aleatoriamente del conjunto de vecinos
        return (random.randint(1, self.ancho), random.randint(1, self.alto))

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        # Activar flag indicando de que se solicitó detener el proceso
        self._stoprequest.set()
        # Notificar a proceso padre
        self.encolar_salida({'Joined': True})
        super(QLearningEntrenarWorker, self).join(timeout)

    def _crear_cont_ref(self, tipos_vec_exc):
        u"""
        Crea y configura un contador de referencias por cada estado accesible.

        :param tipos_vec_exc: Tipos de vecinos a excluir del contador.
        """
        matriz_q = self.matriz_q
        tipos_vec_exc.append(TIPOESTADO.FINAL)

        contador_ref = {}
        for i, fila in enumerate(matriz_q):
            for j, columna in enumerate(fila):
                if columna[0] not in tipos_vec_exc:
                    contador_ref[(i + 1, j + 1)] = 0

        return contador_ref

    def _contar_ref(self, estado):
        u"""
        Incrementa en 1 el contador de cada estado por cada acceso a sus coordenadas.

        :param estado: Estado al cual se ha accedido.
        """
        umbral_1 = 1
        umbral_2 = 2

        self._contador_ref[estado] += 1
        cont = self._contador_ref[estado]

        if cont == umbral_1:
            self._visitados_1.append(estado)
        elif cont == umbral_2:
            self._visitados_2.append(estado)

        self._comprobar_visitados()

    def _comprobar_visitados(self):
        u"""
        Verifica si el agente no puede acceder al estado final y finaliza la
        ejecución del algoritmo.
        """
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
        if self.tipos_vec_excluidos is None:
            self.tipos_vec_excluidos = []

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
                    if vecino.tipo.ide not in self.tipos_vec_excluidos:
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

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        self._inp_queue.close()
        self._error_queue.close()
        self._out_queue.close()

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        recorrido de Q-Learning.
        """
        if sys.platform == 'win32':
            wtimer = time.clock
        else:
            wtimer = time.time

        # Registrar tiempo de comienzo
        running_start_time = wtimer()

        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener la referencia a la instancia desde la cola de entrada
        try:
            self.input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None

        matriz_q = self.input_data[0]
        estado_inicial = self.input_data[1]

        # Lista que contiene la secuencia de estados comenzando por el
        # Estado Inicial
        camino_optimo = [estado_inicial]

        # Registrar tiempo de comienzo
        rec_start_time = wtimer()

        x_act, y_act = estado_inicial
        estado_actual = matriz_q[x_act - 1][y_act - 1]

        while (not self._stoprequest.is_set()) and (estado_actual[0] != TIPOESTADO.FINAL):
            self.encolar_salida({'EstadoActual': (x_act, y_act),
                                 'ProcesoJoined': False})

            vecinos = estado_actual[1]

            # Buscar el estado que posea el mayor valor de Q
            maximo = None
            estados_qmax = []

            for key, q_valor in vecinos.iteritems():
                if maximo is None:
                    maximo = q_valor

                if q_valor > maximo:
                    maximo = q_valor
                    estados_qmax = [key]
                elif q_valor == maximo:
                    estados_qmax.append(key)

            # Comprobar si hay estados con valores Q iguales y elegir uno
            # de forma aleatoria
            long_vecinos = len(estados_qmax)
            if long_vecinos == 1:
                estado_qmax = estados_qmax[0]
            elif long_vecinos > 1:
                estado_qmax = random.choice(estados_qmax)
            else:
                pass

            # Descomponer coordenadas de estado
            x_eleg, y_eleg = estado_qmax

            # Agregar estado al camino óptimo
            camino_optimo.append(estado_qmax)

            # Actualizar estado actual
            x_act, y_act = x_eleg, y_eleg
            estado_actual = matriz_q[x_act - 1][y_act - 1]

        # Registrar tiempo de finalización
        running_end_time = rec_end_time = wtimer()

        try:
            rec_exec_time = rec_end_time - rec_start_time
            running_exec_time = running_end_time - running_start_time
        except UnboundLocalError:
            rec_exec_time = 0
            running_exec_time = 0

        # Poner en la cola de salida los resultados
        self.encolar_salida({'EstadoActual': (x_act, y_act),
                             'CaminoRecorrido': camino_optimo,
                             'RecorridoExecTime': rec_exec_time,
                             'ProcesoJoined': False,
                             'RunningExecTime': running_exec_time})

        # Realizar tareas al finalizar
        self._on_end()

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        self._stoprequest.set()
        self.encolar_salida({'Joined': True})
        super(QLearningRecorrerWorker, self).join(timeout)

    def encolar_salida(self, salida):
        u"""
        Colocar los resultandos del procesamiento en la cola de salida.

        :param salida: Información a colocar en la cola.
        """
        try:
            self._out_queue.put(salida)
        except Queue.Full:
            pass

    def encolar_errores(self, error):
        u"""
        Colocar los mensajes de errore en la cola de errores.

        :param error: Mensaje de error a colocar en la cola.
        """
        try:
            self._error_queue.put(error)
        except Queue.Full:
            pass
