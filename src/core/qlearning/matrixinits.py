#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random


class QLMatrixInicializador(object):
    u"""
    Clase base para inicializar los valores de la Matriz Q.
    """
    def __init__(self, default=None):
        super(QLMatrixInicializador, self).__init__()
        self.default = default

    def procesar_valor(self, valor):
        return valor


class QLMatrixInitEnCero(QLMatrixInicializador):
    u"""
    Inicializa la Matriz Q con todos los valores en cero.
    """
    def __init__(self):
        super(QLMatrixInitEnCero, self).__init__()

    def procesar_valor(self, valor):
        return 0


class QLMatrixInitRandom(QLMatrixInicializador):
    u"""
    Inicializa la Matriz Q con valores aleatorios entre cero y "valor".
    """
    def __init__(self):
        super(QLMatrixInitRandom, self).__init__()

    def procesar_valor(self, valor):
        return random.randint(0, valor)


class QLMatrixInitEnRecompensa(QLMatrixInicializador):
    u"""
    Inicializa la Matriz Q con valores iguales al de la transición.
    """
    def __init__(self):
        super(QLMatrixInitEnCero, self).__init__()

    def procesar_valor(self, valor):
        return valor

class QLMatrixInitOptimista(QLMatrixInicializador):
    def __init__(self, default):
        super(QLMatrixInitOptimista, self).__init__()
        self.default = default

    def procesar_valor(self, valor):
        return self.default + (self.default / 2.0)
