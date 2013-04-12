#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.gridworld.gridworld import GridWorld
from core.tecnicas.tecnica import QLTecnica
from core.tecnicas.egreedy import EGreedy
from core.tecnicas.softmax import Softmax


class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gridworld, gamma, tecnica, init_value=0):
        """
        Inicializador

        :param gridworld: GridWorld sobre el cual se aplicará el algoritmo.
        :param gamma: Parámetro Gamma de QLearning.
        :param tecnica: Técnica a utilizar.
        :param init_value: Valor con que se inicializa cada estado de la matriz.
        """
        super(QLearning, self).__init__()
        self._gridworld = gridworld
        self._gamma = gamma
        self._tecnica = tecnica
        self._matriz_q = None
        self._inicializar_matriz_q(init_value)

    def get_matriz_q(self):
        return self._matriz_q

    def set_matriz_q(self, valor):
        self._matriz_q = valor

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
            raise ValueError(u"El parámetro debe ser del tipo QLTécnica")

    def get_gridworld(self):
        return self._gridworld

    def set_gridworld(self, valor):
        if isinstance(valor, GridWorld):
            self._gridworld = valor
        else:
            raise ValueError(u"El parámetro debe ser del tipo GridWorld")

    def get_estado(self, x, y):
        return self._matriz_q[(x, y)]

    def set_estado(self, x, y, estado):
        self._matriz_q[(x, y)] = estado

    def set_valor_estado(self, x, y, valor):
        u"""
        Establece el valor numérico del estado.

        :param x: Fila del estado
        :param y: Columna del estado
        :param valor: Valor númerico
        """
        self._matriz_q[x][y] = valor

    def _inicializar_matriz_q(self, default=0):
        u"""
        Crea la matriz Q con un valor inicial.

        :param default: Valor con que se inicializa cada estado de la matriz.
        """
        self._matriz_q = {}
        for i in range(1, self._gridworld.alto + 1):
            for j in range(1, self._gridworld.ancho + 1):
                self._matriz_q[(i, j)] = default

    def get_vecinos_estado(self, x, y):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila de la celda
        :param y: Columna de la celda
        """
        vecinos = {}
        for fila, columna in [(x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if (fila, columna) in self._matriz_q.keys():
                vecinos[(fila, columna)] = self.get_estado(fila, columna)
        return vecinos

    gamma = property(get_gamma, set_gamma, None, u"Propiedad Gamma de QLearning")
    tecnica = property(get_tecnica, set_tecnica, None, u"Propiedad Técnica de QLearning")
    matriz_q = property(get_matriz_q, set_matriz_q, None, "Propiedad Matriz Q")
    gridworld = property(get_gridworld, set_gridworld, None, "Propiedad GridWorld")
