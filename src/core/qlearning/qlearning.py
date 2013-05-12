#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import multiprocessing
import numpy
import random

from core.qlearning.workers import QLearningEntrenarWorker, QLearningRecorrerWorker
from core.gridworld.gridworld import GridWorld
from core.tecnicas.tecnica import QLTecnica


class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gridworld, gamma, tecnica, episodes,
                 init_value_fn, excluir_tipos_vecinos=None):
        """
        Inicializador de QLearning.

        :param gridworld: GridWorld sobre el cual se aplicará el algoritmo.
        :param gamma: Parámetro Gamma de QLearning.
        :param tecnica: Técnica a utilizar.
        :param episodes: Cantidad de veces que se puede alcanzar el estado final.
        :param init_value: Valor con que se inicializa cada estado de la matriz.
        """
        super(QLearning, self).__init__()

        # FIXME: Logging
        self._logger = logging.getLogger()

        self._gridworld = gridworld
        self._gamma = gamma
        self._tecnica = tecnica
        self._episodes = episodes
        self._excluir_tipos_vecinos = excluir_tipos_vecinos
        self._init_value_fn = init_value_fn

    def _generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        x = random.randint(1, self._gridworld.ancho)
        y = random.randint(1, self._gridworld.alto)
        return (x, y)

    def entrenar(self, out_queue, error_queue):
        u"""
        Ejecuta el algoritmo de aprendizaje en otro hilo/proceso. Devuelve una
        referencia al hilo/proceso ejecutado.

        :param out_queue: Cola de salida.
        :param error_q: Cola de errores (salida)
        """
        inp_queue = multiprocessing.Queue()
        # Encolar Matriz R, Matriz Q, Número de episodios, Parámetro Gamma
        inp_queue.put((self._gridworld.estados,
                       self.gridworld.coordenadas,
                       self._gamma,
                       self._episodes,
                       self._tecnica,
                       (self._gridworld.alto, self._gridworld.ancho),
                       False,
                       self._gridworld.tipos_vecinos_excluidos,
                       self._init_value_fn
                      ))

        qlearning_entrenar_worker = None

        try:
            qlearning_entrenar_worker = QLearningEntrenarWorker(inp_queue,
                                                                out_queue,
                                                                error_queue
                                                                )
            qlearning_entrenar_worker.start()
        except multiprocessing.ProcessError as pe:
            self._logger.debug(pe)
            raise multiprocessing.ProcessError
        finally:
            pass

        return qlearning_entrenar_worker

    def recorrer(self, matriz_q, estado_inicial, out_queue, error_queue):
        u"""
        Ejecuta el algoritmo de recorrido en otro hilo/proceso. Devuelve una
        referencia al hilo/proceso ejecutado.

        :param out_queue: Cola de salida.
        :param error_q: Cola de errores (salida)
        """
        inp_queue = multiprocessing.Queue()
        inp_queue.put((matriz_q, estado_inicial))
        qlearning_recorrer_worker = None

        try:
            qlearning_recorrer_worker = QLearningRecorrerWorker(inp_queue,
                                                                out_queue,
                                                                error_queue
                                                                )
            qlearning_recorrer_worker.start()
        except multiprocessing.ProcessError as pe:
            self._logger.debug(pe)
            raise multiprocessing.ProcessError
        finally:
            pass

        return qlearning_recorrer_worker

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
        """
        Devuelve la referencia al estado determinado por las coordenadas X e Y.

        :param x: Coordenada X del estado (fila)
        :param y: Coordenada Y del estado (columna)
        """
        return self._matriz_q[x - 1][y - 1]

    def set_estado(self, x, y, estado):
        """
        Almacena un estado dado en una posición determinada por las coordenadas
        X e Y.

        :param x: Coordenada X de destino (fila)
        :param y: Coordenada Y de destino (columna)
        :param estado: Estado a almacenar en la matriz.
        """
        self._matriz_q[x - 1][y - 1] = estado

    def get_episodes(self):
        return self._episodes

    def set_episodes(self, value):
        self._episodes = value

    def get_coordenadas(self):
        return self._coordenadas

    def get_matriz_q(self):
        u"""
        Crea la matriz Q con un valor inicial.

        :param default: Valor con que se inicializa cada estado de la matriz.
        """
        matriz_r = self._gridworld.matriz_r
        ancho = self.gridworld.ancho
        alto = self.gridworld.alto
        matriz_q = numpy.empty((ancho, alto), object)

        for i in xrange(0, alto):
            for j in xrange(0, ancho):
                tipo_estado = matriz_r[i][j][0]
                vecinos = matriz_r[i][j][1]
                vecinos = dict([(key, self._init_value_fn.procesar_valor(value))
                                for key, value in vecinos.iteritems()])
                matriz_q[i][j] = (tipo_estado, vecinos)
        return matriz_q

    def get_vecinos_estado(self, x, y):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila de la celda
        :param y: Columna de la celda
        """
        vecinos = []
        coordenadas = self._gridworld.coordenadas
        for fila, columna in ((x + i, y + j)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if i != 0 or j != 0):
            if (fila, columna) in coordenadas:
                vecinos.append(self.get_estado(fila, columna))
        return numpy.array(vecinos)

    def matriz_q_to_string(self):
        u"""
        Devuelve un string representando la matriz Q en una estructura tabular.
        """
        matriz_q = self.get_matriz_q()
        return "\n".join(["| {0} |".format(" | ".join(j))
                          for j in [[str(i) for i in f]
                                                for f in matriz_q]])

    gamma = property(get_gamma, set_gamma, None, u"Propiedad Gamma de QLearning")
    tecnica = property(get_tecnica, set_tecnica, None, u"Propiedad Técnica de QLearning")
    matriz_q = property(get_matriz_q, None, None, "Propiedad Matriz Q")
    gridworld = property(get_gridworld, set_gridworld, None, "Propiedad GridWorld")
    coordenadas = property(get_coordenadas, None, None, "Propiedad Coordenadas")
    episodes = property(get_episodes, set_episodes, None, "Propiedad Episodios")
