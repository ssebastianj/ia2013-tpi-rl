#!/usr/bin/env python
# -*- coding: utf-8 -*-


class GridWorld(object):
    """Clase GridWorld"""
    def __init__(self, ancho, alto, estados=None):
        """
        @param ancho: Ancho
        @param alto: Alto
        @param estados: Conjunto de estados
        """
        super(GridWorld, self).__init__()
        self._ancho = ancho
        self._alto = alto
        self._estados = estados

    def get_ancho(self):
        return self._ancho

    def set_ancho(self, valor):
        self._ancho = valor

    def get_alto(self):
        return self._alto

    def set_alto(self, valor):
        self._alto = valor

    def get_estados(self):
        return self._estados

    def set_estados(self, valor):
        self._estados = valor

    ancho = property(get_ancho, set_ancho, None, "Ancho del GridWorld")
    alto = property(get_alto, set_alto, None, "Alto del GridWorld")
    estados = property(get_estados, set_estados, None, "Estados del GridWorld")
