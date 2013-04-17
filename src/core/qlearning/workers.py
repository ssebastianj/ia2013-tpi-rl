#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import threading
import time
from core.estado.estado import TIPOESTADO


class QLearningEntrenarWorker(threading.Thread):
    u"""
    Worker encargado de realizar el aprendizaje de Q-Learning.
    """
    def __init__(self, inp_queue, out_queue, error_q):
        """
        Inicializador del worker.

        :param inp_queue: Cola de entrada.
        :param out_queue: Cola de salida.
        :param error_q: Cola de errores (salida)
        """
        super(QLearningEntrenarWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_q
        self._stoprequest = threading.Event()
        self.name = "QLearningEntrenarWorker"
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")

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

        # Obtener la referencia a la instancia desde la cola de entrada
        ql_ref = self._inp_queue.get()
        logging.debug("Entrada al proceso: {0}".format(ql_ref))

        # Obtener matriz R de recompensa
        matriz_r = ql_ref._gridworld.get_matriz_r()
        # Inicializar matriz Q a un valor dado
        ql_ref.inicializar_matriz_q()

        # Ejecutar una cantidad dada de Episodios
        for epnum in range(1, ql_ref._episodes + 1):
            # Registrar tiempo de comienzo del episodio
            ep_start_time = time.clock()

            logging.debug("Numero de episodio: {0}".format(epnum))  # FIXME: Logging

            # Obtener coordenadas aleatorias y obtener Estado asociado
            (x, y) = ql_ref._generar_estado_aleatorio()

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las del estado final
            estado_actual = ql_ref._gridworld.get_estado(x, y)
            while estado_actual.tipo.ide == TIPOESTADO.FINAL:
                (x, y) = ql_ref._generar_estado_aleatorio()
                estado_actual = ql_ref._gridworld.get_estado(x, y)

            # Forzar restauración del valor de parámetro de la técnica
            # utilizada antes de comenzar un nuevo Episodio
            ql_ref._tecnica.restaurar_val_parametro()

            # Realizar 1 Episodio mientras no estemos en el Estado Final
            cant_iteraciones = 0
            while (not self._stoprequest.is_set()) and (not estado_actual.tipo.ide == TIPOESTADO.FINAL):
                # Registrar tiempo de comienzo de las iteraciones
                iter_start_time = time.clock()

                # Obtener vecinos del estado actual
                vecinos = matriz_r[estado_actual.fila - 1][estado_actual.columna - 1]
                # Invocar a la técnica para que seleccione uno de los vecinos
                estado_elegido = ql_ref.tecnica.obtener_accion(ql_ref._matriz_q, vecinos)
                recompensa_estado = estado_elegido.tipo.recompensa
                # Obtener vecinos del estado elegido por la acción
                vecinos_est_elegido = matriz_r[estado_elegido.fila - 1][estado_elegido.columna - 1]

                # Obtener la recompensa de cada vecino y buscar el máximo valor
                recompensa_vecinos = []
                for j in vecinos_est_elegido:
                    recompensa_vecinos.append(j.tipo.recompensa)
                recompensa_max = max(recompensa_vecinos)

                # Fórmula principal de Q-Learning
                if recompensa_estado is not None:
                    nuevo_q = recompensa_estado + (ql_ref._gamma * recompensa_max)
                # Actualizar valor de Q en matriz Q
                ql_ref.matriz_q[estado_elegido.fila - 1][estado_elegido.columna - 1] = nuevo_q
                # Cambiar de estado
                estado_actual = estado_elegido

                cant_iteraciones += 1

                # Comprobar si es necesario decrementar el valor del parámetro
                if ql_ref.tecnica.intervalo_decremento == cant_iteraciones:
                    # Decrementar valor del parámetro en 1 paso
                    ql_ref.tecnica.decrementar_parametro()

                logging.debug("Valor parámetro: {0}".format(ql_ref._tecnica._val_param_parcial))  # FIXME: Logging
                logging.debug("Iteraciones {0}".format(cant_iteraciones))  # FIXME: Logging
                logging.debug("Matriz Q: {0}".format(ql_ref._matriz_q))
                self._out_queue.put(((x, y), epnum, cant_iteraciones, 0, 0))

            iter_end_time = time.clock()
            ep_end_time = time.clock()
            # Calcular tiempo de ejecución del episodio
            ep_exec_time = ep_end_time - ep_start_time
            # Calcular tiempo de ejecución de las iteraciones
            iter_exec_time = iter_end_time - iter_start_time

            # Poner en la cola de salida los resultados
            self._out_queue.put(((x, y),
                                epnum,
                                cant_iteraciones,
                                ep_exec_time,
                                iter_exec_time))

            # Verificar si se solicitó externamente finalizar el thread
            if self._stoprequest.is_set():
                self._out_queue.put(True)
                break

        # Poner en cola un valor booleano para indicar que se finalizó el trabajo
        self._out_queue.put(True)
        # Realizar tareas al finalizar
        self._on_end()

    def join(self, timeout=None):
        u"""
        Sobrecarga del método 'join'.

        :param timeout: Tiempo en milisegundos de espera.
        """
        logging.debug("Join")
        self._stoprequest.set()
        super(QLearningEntrenarWorker, self).join(timeout)
