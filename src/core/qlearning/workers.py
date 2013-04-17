#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import threading
import time
from core.estado.estado import TIPOESTADO


class QLearningEntrenarWorker(threading.Thread):
    def __init__(self, inp_queue, out_queue, error_q):
        super(QLearningEntrenarWorker, self).__init__()
        self._inp_queue = inp_queue
        self._out_queue = out_queue
        self._error_queue = error_q
        self._stoprequest = threading.Event()
        self.name = "QLearningEntrenarWorker"
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")

    def _do_on_start(self):
        logging.debug("En ejecución.")

    def _on_end(self):
        logging.debug("Terminando.")

    def run(self):
        self._do_on_start()

        ql_ref = self._inp_queue.get()
        logging.debug("Entrada al proceso: {0}".format(ql_ref))

        # Obtener matriz R de recompensa
        matriz_r = ql_ref._gridworld.get_matriz_r()
        ql_ref.inicializar_matriz_q()

        # Ejecutar una cantidad dada de Episodios
        for epnum in range(1, ql_ref._episodes + 1):
            ep_start_time = time.clock()
            logging.debug("Numero de episodio: {0}".format(epnum))  # FIXME: Logging
            # Obtener coordenadas aleatorias y obtener Estado asociado
            (x, y) = ql_ref._generar_estado_aleatorio()

            # Generar estados aleatorios hasta que las coordenadas no
            # coincidan con las del estado final
            aux_estado = ql_ref._gridworld.get_estado(x, y)
            while aux_estado.tipo.ide == TIPOESTADO.FINAL:
                (x, y) = ql_ref._generar_estado_aleatorio()
                aux_estado = ql_ref._gridworld.get_estado(x, y)

            estado_actual = ql_ref._gridworld.get_estado(x, y)

            # Forzar restauración del valor de parámetro de la técnica
            # utilizada antes de comenzar un nuevo Episodio
            ql_ref._tecnica.restaurar_val_parametro()

            # Realizar 1 Episodio mientras no estemos en el Estado Final
            cant_iteraciones = 0
            while (not self._stoprequest.is_set()) and (not estado_actual.tipo.ide == TIPOESTADO.FINAL):
                iter_start_time = time.clock()

                vecinos = matriz_r[estado_actual.fila - 1][estado_actual.columna - 1]
                estado_elegido = ql_ref.tecnica.obtener_accion(ql_ref._matriz_q, vecinos)
                recompensa_estado = estado_elegido.tipo.recompensa
                vecinos_est_elegido = ql_ref._gridworld.matriz_r[estado_elegido.fila - 1][estado_elegido.columna - 1]

                recompensa_vecinos = []
                for j in vecinos_est_elegido:
                    recompensa_vecinos.append(j.tipo.recompensa)
                recompensa_max = max(recompensa_vecinos)

                if recompensa_estado is not None:
                    nuevo_q = recompensa_estado + (ql_ref._gamma * recompensa_max)
                ql_ref.matriz_q[estado_elegido.fila - 1][estado_elegido.columna - 1] = nuevo_q
                estado_actual = estado_elegido

                cant_iteraciones += 1

                # Comprobar si es necesario decrementar el valor del parámetro
                if ql_ref.tecnica.intervalo_decremento == cant_iteraciones:
                    # Decrementar valor del parámetro en 1 paso
                    ql_ref.tecnica.decrementar_parametro()

                logging.debug("Valor parámetro: {0}".format(ql_ref._tecnica.valor_param_parcial))  # FIXME: Logging
                logging.debug("Iteraciones {0}".format(cant_iteraciones))  # FIXME: Logging
                logging.debug("Matriz Q: {0}".format(ql_ref._matriz_q))
                self._out_queue.put(((x, y), epnum, cant_iteraciones, 0, 0))

            iter_end_time = time.clock()
            ep_end_time = time.clock()
            ep_exec_time = ep_end_time - ep_start_time
            iter_exec_time = iter_end_time - iter_start_time

            self._out_queue.put(((x, y),
                                epnum,
                                cant_iteraciones,
                                ep_exec_time,
                                iter_exec_time))

            if self._stoprequest.is_set():
                self._out_queue.put(False)
                break

        self._out_queue.put(False)
        self._on_end()

    def join(self, timeout=None):
        self._stoprequest.set()
        super(QLearningEntrenarWorker, self).join(timeout)
