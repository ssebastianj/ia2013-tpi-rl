#!/usr/bin/env python
# -*- coding: utf-8 -*-


class GridWorld(object):
    """Clase GridWorld"""
    def __init__(self, ancho, alto, estados=None):
        super(GridWorld, self).__init__()
        self._ancho = ancho
        self._alto = alto
        self._estados = estados

    def _get_ancho(self):
        return self._ancho

    def _set_ancho(self, valor):
        self._ancho = valor

    ancho = property(_get_ancho, _set_ancho, None, "Ancho del GridWorld")

    def _get_alto(self):
        return self._alto

    def _set_alto(self, valor):
        self._alto = valor

    alto = property(_get_alto, _set_alto, None, "Alto del GridWorld")

    def _get_estados(self):
        return self._estados

    def _set_estados(self, valor):
        self._estados = valor

    estados = property(_get_estados, _set_estados, None, "Estados del GridWorld")
