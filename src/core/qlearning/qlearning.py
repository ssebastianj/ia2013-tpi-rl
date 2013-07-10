#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import multiprocessing
import numpy
import random
import sys

from core.qlearning.workers import QLearningEntrenarWorker, QLearningRecorrerWorker
from core.gridworld.gridworld import GridWorld
from core.tecnicas.tecnica import QLTecnica


class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gridworld, gamma, tecnica, episodes, iterations_pack,
                 init_value_fn, matriz_diff_pack, cant_max_iter_gral_pack=(sys.maxint, 1),
                 excluir_tipos_vecinos=None):
        """
        Inicializador de QLearning.

        :param gridworld: GridWorld sobre el cual se aplicará el algoritmo.
        :param gamma: Parámetro Gamma de QLearning.
        :param tecnica: Técnica a utilizar.
        :param episodes: Cantidad de veces que se puede alcanzar el estado final.
        :param init_value: Valor con que se inicializa cada estado de la matriz.
        """
        super(QLearning, self).__init__()

        self._logger = logging.getLogger()

        self._gridworld = gridworld
        self._gamma = gamma
        self._tecnica_pack = tecnica
        self._episodes = episodes
        self._excluir_tipos_vecinos = excluir_tipos_vecinos
        self._init_value_fn = init_value_fn
        self._iterations_pack = iterations_pack
        self._mat_diff_pack = matriz_diff_pack
        self._cant_max_iter_gral_pack = cant_max_iter_gral_pack

    def _generar_estado_aleatorio(self):
        u"""
        Devuelve una tupla conteniendo las coordenadas X e Y aleatorias.
        """
        # Fila
        x = random.randint(1, self._gridworld.ancho)
        # Columna
        y = random.randint(1, self._gridworld.alto)
        return (x, y)

    def entrenar(self, out_queue, error_queue):
        u"""
        Ejecuta el algoritmo de aprendizaje en otro hilo/proceso. Devuelve una
        referencia al hilo/proceso ejecutado.

        :param out_queue: Cola de salida.
        :param error_q: Cola de errores (salida)
        """
        # Cola de entrada
        inp_queue = multiprocessing.Queue()

        # Encolar Matriz R, Matriz Q, Número de episodios, Parámetro Gamma
        inp_queue.put((self._gridworld.estados,
                       self._gridworld.coordenadas,
                       self._gamma,
                       self._episodes,
                       self._iterations_pack,
                       self._tecnica_pack,
                       (self._gridworld.alto, self._gridworld.ancho),
                       False,
                       self._gridworld.tipos_vecinos_excluidos,
                       self._init_value_fn,
                       self._mat_diff_pack,
                       self._cant_max_iter_gral_pack
                       ))

        qlearning_entrenar_worker = None

        try:
            # Crear worker de Entrenamiento
            qlearning_entrenar_worker = QLearningEntrenarWorker(inp_queue,
                                                                out_queue,
                                                                error_queue
                                                                )
            qlearning_entrenar_worker.daemon = True
            qlearning_entrenar_worker.start()
        except multiprocessing.ProcessError as pe:
            self._logger.debug(pe)
            raise multiprocessing.ProcessError
        finally:
            pass

        return qlearning_entrenar_worker

    def recorrer(self, matriz_q, mat_est_acc, estado_inicial, out_queue, error_queue):
        u"""
        Ejecuta el algoritmo de recorrido en otro hilo/proceso. Devuelve una
        referencia al hilo/proceso ejecutado.

        :param out_queue: Cola de salida.
        :param error_q: Cola de errores (salida)
        """
        # Cola de entrada
        inp_queue = multiprocessing.Queue()
        inp_queue.put((matriz_q, mat_est_acc, estado_inicial))
        qlearning_recorrer_worker = None

        try:
            # Crear worker de Explotación
            qlearning_recorrer_worker = QLearningRecorrerWorker(inp_queue,
                                                                out_queue,
                                                                error_queue
                                                                )
            qlearning_recorrer_worker.daemon = True
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
        return self._tecnica_pack

    def set_tecnica(self, valor):
        if isinstance(valor, QLTecnica):
            self._tecnica_pack = valor
        else:
            raise TypeError(u"El parámetro debe ser del tipo QLTécnica")

    def get_gridworld(self):
        return self._gridworld

    def set_gridworld(self, valor):
        u"""
        Asigna un GridWorld dado a Q-Learning.

        :param valor: Arreglo de estados conteniendo un GridWorld.
        """
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

    def get_iterations_pack(self):
        return self._iterations_pack

    def set_iterations_pack(self, valor):
        u"""
        Establece un conjunto de opciones referidas a las iteraciones de Q-Learning.

        :param valor: Tupla con el formato: (Activar Limitador (Booleano), Cantidad Iteraciones Máxima (Entero))
        """
        self._iterations_pack = valor

    def get_max_iterations(self):
        self._iterations_pack[1]

    def get_matriz_q(self, include_vecinos=False):
        u"""
        Genera y devuelve la matriz de vecinos, matriz R y matriz Q.
        """
        # Verificar si hay tipos de vecinos a excluir de la matriz R
        if self.tipos_vec_excluidos is None:
            self.tipos_vec_excluidos = []

        # Cachear acceso a métodos y atributos
        get_vecinos_estado = self.get_vecinos_estado
        get_estado = self.get_estado
        tipos_vec_excluidos = self.tipos_vec_excluidos
        q_init_value_fn = self.q_init_value_fn
        ancho = self.ancho
        alto = self.alto
        dimension = ancho * alto

        # Matriz de vecinos
        matriz_estados = numpy.empty((alto, ancho), numpy.int)

        # Matriz Q
        matriz_q = numpy.empty((dimension, dimension), numpy.float)
        matriz_q.fill(numpy.nan)

        for i in xrange(alto):
            fila = []
            fappend = fila.append

            for j in xrange(ancho):
                # Obtener estado actual y su ID de tipo
                estado = get_estado(i + 1, j + 1)
                estado_ide = estado.tipo.ide
                # Obtener los estados vecinos del estado actual (i, j)
                vecinos = get_vecinos_estado(i + 1, j + 1, True)

                # Calcular posición en eje Y
                y_coord = (i * alto) + j

                if include_vecinos:
                    evecinos = []
                    evappend = evecinos.append

                for x, y in vecinos:
                    est_vec = get_estado(x, y)

                    if est_vec.tipo.ide not in tipos_vec_excluidos:
                        # Calcular posición en eje X
                        x_coord = ((x - 1) * ancho) + (y - 1)

                        # Establecer valor Q inicial en matriz
                        matriz_q[y_coord][x_coord] = q_init_value_fn

                        if include_vecinos:
                            # Agregar coordenadas de vecino
                            evappend((y_coord, x_coord))

                if include_vecinos:
                    # Agregar columna a la fila
                    fappend((estado_ide, evecinos))
                else:
                    fappend(estado_ide)

            # Agregar fila a matriz de vecinos
            matriz_estados[i] = fila

        return matriz_q

    def get_vecinos_estado(self, x, y, iterate=False):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila del estado
        :param y: Columna del estado
        """
        coordenadas = self.coordenadas
        vecinos = []
        vappend = vecinos.append

        for fila, columna in ((x + i, y + j)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if i != 0 or j != 0):
            if (fila, columna) in coordenadas:
                vappend((fila, columna))
        if iterate:
            return iter(vecinos)
        else:
            return vecinos

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
