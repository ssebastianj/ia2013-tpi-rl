#!/usr/bin/env python


import random


class QLMatrixInicializador:
    """
    Clase base para inicializar los valores de la Matriz Q.
    """
    def __init__(self, default=None):
        super().__init__()
        self.default = default

    def procesar_valor(self, valor):
        return valor


class QLMatrixInitEnCero(QLMatrixInicializador):
    """
    Inicializa la Matriz Q con todos los valores en cero.
    """
    def __init__(self):
        super().__init__()

    def procesar_valor(self, valor):
        return 0


class QLMatrixInitRandom(QLMatrixInicializador):
    """
    Inicializa la Matriz Q con valores aleatorios entre cero y "valor".
    """
    def __init__(self):
        super().__init__()

    def procesar_valor(self, valor):
        return random.randint(0, valor)


class QLMatrixInitEnRecompensa(QLMatrixInicializador):
    """
    Inicializa la Matriz Q con valores iguales al de la transición.
    """
    def __init__(self):
        super(QLMatrixInitEnCero, self).__init__()

    def procesar_valor(self, valor):
        return valor


class QLMatrixInitOptimista(QLMatrixInicializador):
    def __init__(self, default):
        super().__init__()
        self.default = default

    def procesar_valor(self, valor):
        return self.default + (self.default / 2.0)
