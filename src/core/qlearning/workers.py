#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
from multiprocessing import Process, Queue
from core.estado.estado import TIPOESTADO


class QLearningEntrenarWorker(threading.Thread):
    def __init__(self, input_queue, output_queue):
        super(QLearningEntrenarThread, self).__init__()
        self._output_queue = output_queue
        self._input_queue = input_queue
        self._stoprequest = threading.Event()

    def run(self):
        ql_ref = self._input_queue.get(False)
        while not self._stoprequest.is_set():
            try:
                # Obtener matriz R de recompensa
                matriz_r = ql_ref._gridworld.get_matriz_r()
                ql_ref._inicializar_matriz_q()

                # Ejecutar una cantidad dada de Episodios
                for i in range(1, ql_ref._episodes + 1):
                    logging.debug("Numero de episodio: {0}".format(i))  # FIXME: Logging
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
                    contador = 0
                    while not estado_actual.tipo.ide == TIPOESTADO.FINAL:
                        vecinos = matriz_r[estado_actual.fila - 1][estado_actual.columna - 1]
                        estado_elegido = ql_ref._tecnica.obtener_accion(ql_ref._matriz_q, vecinos)
                        recompensa_estado = estado_elegido.tipo.recompensa
                        vecinos_est_elegido = ql_ref._gridworld.matriz_r[estado_elegido.fila - 1][estado_elegido.columna - 1]

                        recompensa_vecinos = []
                        for i in vecinos_est_elegido:
                            recompensa_vecinos.append(i.tipo.recompensa)
                        recompensa_max = max(recompensa_vecinos)
                        if recompensa_estado is not None:
                            nuevo_q = recompensa_estado + (ql_ref._gamma * recompensa_max)
                        ql_ref._matriz_q[estado_elegido.fila - 1][estado_elegido.columna - 1] = nuevo_q
                        estado_actual = estado_elegido

                        contador += 1

                        # Comprobar si es necesario decrementar el valor del parámetro
                        if ql_ref._tecnica.intervalo_decremento == contador:
                            # Decrementar valor del parámetro en 1 paso
                            ql_ref._tecnica.decrementar_parametro()

                        logging.debug("Valor parámetro: {0}".format(ql_ref._tecnica.valor_param_parcial))  # FIXME: Logging
                        logging.debug("Iteraciones {0}".format(contador))  # FIXME: Logging
                        logging.debug("Matriz Q: {0}".format(ql_ref._matriz_q))
                        # self._output_queue.put((x, y, contador))
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self._stoprequest.set()
        super(QLearningEntrenarThread, self).join(timeout)
