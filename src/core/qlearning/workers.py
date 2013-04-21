#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import threading
import time
import random
from core.estado.estado import TIPOESTADO


class QLearningEntrenarWorker(threading.Thread):
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
        self._stoprequest = threading.Event()
        self.name = "QLearningEntrenarWorker"
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")  # @IgnorePep8

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

    def run(self):
        u"""
        Método sobrecargado de clase padre Thread. Ejecuta el algoritmo de
        aprendizaje de Q-Learning.
        """
        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener matriz R y matriz Q
        self.input_data = self._inp_queue.get()
        matriz_r = self.input_data[0]
        matriz_q = self.input_data[1]
        gamma = self.input_data[2]
        cant_episodios = self.input_data[3]
        tecnica = self.input_data[4]

        logging.debug("Matriz R: {0}".format(matriz_r))
        logging.debug("Matriz Q: {0}".format(matriz_q))
        logging.debug("Gamma: {0}".format(gamma))
        logging.debug("Episodios: {0}".format(cant_episodios))
        logging.debug("Técnica: {0}".format(tecnica))

        # Ejecutar una cantidad dada de Episodios
        for epnum in range(1, cant_episodios + 1):
            # Registrar tiempo de comienzo del episodio
            ep_start_time = time.clock()

            logging.debug("Numero de episodio: {0}".format(epnum))  # FIXME: Logging @IgnorePep8

            # Obtener coordenadas aleatorias y obtener Estado asociado
            (x_act, y_act) = self.generar_estado_aleatorio()

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las del estado final
            estado_actual = matriz_r[x_act - 1][y_act - 1]
            while estado_actual[0] == TIPOESTADO.FINAL:
                (x_act, y_act) = self.generar_estado_aleatorio()
                estado_actual = matriz_r[x_act - 1][y_act - 1]

            logging.debug("Estado Inicial Generado: {0}".format(estado_actual))

            # Forzar restauración del valor de parámetro de la técnica
            # utilizada antes de comenzar un nuevo Episodio
            tecnica.restaurar_val_parametro()

            # Realizar 1 Episodio mientras no estemos en el Estado Final
            cant_iteraciones = 0
            while (not self._stoprequest.is_set()) and (not estado_actual[0] == TIPOESTADO.FINAL):
                # Registrar tiempo de comienzo de las iteraciones
                iter_start_time = time.clock()

                # Obtener vecinos del estado actual
                vecinos = estado_actual[1]
                logging.debug("Vecinos Estado Actual: {0}".format(vecinos))
                # Invocar a la técnica para que seleccione uno de los vecinos
                estado_elegido = tecnica.obtener_accion(vecinos)
                logging.debug("Estado Elegido: {0}".format(estado_elegido))
                x_eleg, y_eleg = estado_elegido

                recompensa_estado = vecinos[(x_eleg, y_eleg)]

                # Obtener vecinos del estado elegido por la acción
                vecinos_est_elegido = matriz_q[x_eleg - 1][y_eleg - 1]
                logging.debug("Vecinos Elegidos del Elegido: {0}".format(vecinos_est_elegido))

                max_q = max([q_val for q_val in vecinos_est_elegido.values()])

                # Fórmula principal de Q-Learning
                # -------------------------------
                if recompensa_estado is not None:
                    logging.debug("Gamma: {0}".format(gamma))
                    nuevo_q = recompensa_estado + (gamma * max_q)
                    # Actualizar valor de Q en matriz Q
                    matriz_q[x_act - 1][y_act - 1][(x_eleg, y_eleg)] = nuevo_q

                cant_iteraciones += 1

                # Comprobar si es necesario decrementar el valor del parámetro
                if tecnica.intervalo_decremento == cant_iteraciones:
                    # Decrementar valor del parámetro en 1 paso
                    tecnica.decrementar_parametro()

                logging.debug("Valor parámetro: {0}".format(tecnica._val_param_parcial))  # FIXME: Logging @IgnorePep8
                logging.debug("Iteraciones {0}".format(cant_iteraciones))  # FIXME: Logging @IgnorePep8
                logging.debug("Matriz Q: {0}".format(matriz_q))  # FIXME: Logging @IgnorePep8

                self._out_queue.put(((x_act, y_act),
                                     epnum, cant_iteraciones, None, None))

                # Actualizar estado actual
                x_act, y_act = x_eleg, y_eleg
                estado_actual = matriz_r[x_act - 1][y_act - 1]

            iter_end_time = time.clock()
            ep_end_time = time.clock()
            # Calcular tiempo de ejecución del episodio
            ep_exec_time = ep_end_time - ep_start_time
            # Calcular tiempo de ejecución de las iteraciones
            iter_exec_time = iter_end_time - iter_start_time

            # Poner en la cola de salida los resultados
            self._out_queue.put(((x_act, y_act),
                                epnum,
                                cant_iteraciones,
                                ep_exec_time,
                                iter_exec_time))

            # Verificar si se solicitó externamente finalizar el thread
            if self._stoprequest.is_set():
                # self._out_queue.put(True)
                break

        # Poner en cola un valor booleano para indicar que se finalizó el trabajo
        # self._out_queue.put(True)
        # Realizar tareas al finalizar
        self._on_end()

    def elegir_estado_aleatorio(self):
        pass

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
        super(QLearningEntrenarWorker, self).join(timeout)


class QLearningRecorrerWorker(threading.Thread):
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
        self._stoprequest = threading.Event()
        self.name = "QLearningRecorrerWorker"
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")  # @IgnorePep8

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

    def run(self):
        # Realizar tareas al comienzo
        self._do_on_start()

        # Obtener la referencia a la instancia desde la cola de entrada
        (ql_ref, estado_inicial) = self._inp_queue.get()
        logging.debug("Entrada al proceso: {0}".format(ql_ref))

        # Obtener las matrices R y Q para realizar el recorrido
        matriz_r = ql_ref._gridworld.matriz_r
        matriz_q = ql_ref.matriz_q
        logging.debug("matriz Q par ale recorrido: {0}".format(matriz_q))
        # Lista que contiene la secuencia de estados comenzando por el
        # Estado Inicial
        camino_optimo = [estado_inicial]

        # Registrar tiempo de comienzo
        proc_start_time = time.clock()
        estado_actual = estado_inicial
        while (not self._stoprequest.is_set()) and (not estado_actual.tipo.ide == TIPOESTADO.FINAL):
            vecinos = matriz_r[estado_actual.fila - 1][estado_actual.columna - 1]

            # Buscar el estado que posea el mayor valor de Q
            maximo_q = 0
            estados_qmax = []
            for i in vecinos:
                logging.debug("X:{0} Y:{1}".format(i.fila, i.columna))  # FIXME: Eliminar print de debug @IgnorePep8
                q_valor = matriz_q[i.fila - 1][i.columna - 1]
                logging.debug("Q Valor: {0}".format(q_valor))  # FIXME: Eliminar print de debug @IgnorePep8
                if q_valor > maximo_q:
                    maximo_q = q_valor
                    estados_qmax = [i]
                elif q_valor == maximo_q:
                    estados_qmax.append(i)

            # Comprobar si hay estados con valores Q iguales y elegir uno
            # de forma aleatoria
            if len(estados_qmax) == 1:
                estado_qmax = estados_qmax[0]
                logging.debug("Existe un sólo estado vecino con Q máximo")  # FIXME: Eliminar print de debug @IgnorePep8
            else:
                estado_qmax = estados_qmax[random.randint(0, (len(estados_qmax) - 1))]
                logging.debug("Existen varios estados con igual valor Q")  # FIXME: Eliminar print de debug @IgnorePep8

            # Agregar estado al camino óptimo
            camino_optimo.append(estado_qmax)
            self._out_queue.put(((estado_actual.fila,
                                  estado_actual.columna),
                                  None,
                                  None))

            # Actualizar estado actual con el estado con mayor valor de Q
            estado_actual = estado_qmax

        # Registrar tiempo de finalización
        proc_end_time = time.clock()
        proc_exec_time = proc_end_time - proc_start_time

        logging.debug("Camino óptimo: {0}".format(camino_optimo))

        # Encolar la información generada por el algoritmo para realizar
        # estadísticas
        self._out_queue.put(((estado_actual.fila, estado_actual.columna),
                            camino_optimo, proc_exec_time))

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
        self._stoprequest.set()
        super(QLearningRecorrerWorker, self).join(timeout)
