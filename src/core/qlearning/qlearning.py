#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import Queue
import random
import threading

from core.qlearning.workers import QLearningEntrenarWorker
from core.gridworld.gridworld import GridWorld
from core.tecnicas.tecnica import QLTecnica


class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gridworld, gamma, tecnica, episodes, init_value=0):
        """
        Inicializador.

        :param gridworld: GridWorld sobre el cual se aplicará el algoritmo.
        :param gamma: Parámetro Gamma de QLearning.
        :param tecnica: Técnica a utilizar.
        :param episodes: Cantidad de veces que se puede alcanzar el estado final.
        :param init_value: Valor con que se inicializa cada estado de la matriz.
        """
        super(QLearning, self).__init__()
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")

        self._gridworld = gridworld
        self._gamma = gamma
        self._tecnica = tecnica
        self._coordenadas = None
        self._matriz_q = None
        self._episodes = episodes

    def _generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        x = random.randint(1, self._gridworld.ancho)
        y = random.randint(1, self._gridworld.alto)
        return (x, y)

    def entrenar(self, out_queue):
        inp_queue = Queue.Queue()
        inp_queue.put(self)
        qlearning_entrenar_worker = None

        try:
            qlearning_entrenar_worker = QLearningEntrenarWorker(inp_queue,
                                                                out_queue
                                                                )
            qlearning_entrenar_worker.start()
        except threading.ThreadError as te:
            logging.debug(te)
            raise threading.ThreadError
        finally:
            pass

        return qlearning_entrenar_worker

    def get_matriz_q(self):
        return self._matriz_q

    def get_gamma(self):
        return self._gamma

    def set_gamma(self, valor):
        self._gamma = valor

    def get_tecnica(self):
        return self._tecnica

    def set_tecnica(self, valor):
        if isinstance(valor, QLTecnica):
            self._tecnica = valor
        else:
            raise TypeError(u"El parámetro debe ser del tipo QLTécnica")

    def get_gridworld(self):
        return self._gridworld

    def set_gridworld(self, valor):
        if isinstance(valor, GridWorld):
            self._gridworld = valor
        else:
            raise TypeError(u"El parámetro debe ser del tipo GridWorld")

    def get_estado(self, x, y):
        return self._matriz_q[x - 1][y - 1]

    def set_estado(self, x, y, estado):
        self._matriz_q[x - 1][y - 1] = estado

    def get_episodes(self):
        return self._episodes

    def set_episodes(self, value):
        self._episodes = value

    def set_valor_estado(self, x, y, valor):
        u"""
        Establece el valor numérico del estado.

        :param x: Fila del estado
        :param y: Columna del estado
        :param valor: Valor númerico
        """
        self._matriz_q[x - 1][y - 1] = valor

    def get_coordenadas(self):
        return self._coordenadas

    def inicializar_matriz_q(self, default=0):
        u"""
        Crea la matriz Q con un valor inicial.

        :param default: Valor con que se inicializa cada estado de la matriz.
        """
        self._matriz_q = []
        self._coordenadas = []
        for i in range(1, self._gridworld.alto + 1):
            fila = []
            for j in range(1, self._gridworld.ancho + 1):
                fila.append(default)
                self._coordenadas.append((i, j))
            self._matriz_q.append(fila)

        logging.debug(self._matriz_q)  # FIXME: Logging

    def get_vecinos_estado(self, x, y):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila de la celda
        :param y: Columna de la celda
        """
        vecinos = []
        for fila, columna in [(x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if (fila, columna) in self._coordenadas:
                vecinos.append(self.get_estado(fila, columna))
        return vecinos

    def elegir_accion(self, x, y):
        pass

    gamma = property(get_gamma, set_gamma, None, u"Propiedad Gamma de QLearning")
    tecnica = property(get_tecnica, set_tecnica, None, u"Propiedad Técnica de QLearning")
    matriz_q = property(get_matriz_q, None, None, "Propiedad Matriz Q")
    gridworld = property(get_gridworld, set_gridworld, None, "Propiedad GridWorld")
    coordenadas = property(get_coordenadas, None, None, "Propiedad Coordenadas")
    episodes = property(get_episodes, set_episodes, None, "episodes's docstring")
