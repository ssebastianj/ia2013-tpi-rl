#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica


class TRandom(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, comienzo_rango=0, fin_rango=1):
        u"""
        Inicializador

        :param comienzo_rango: Valor inicial del rango de generación.
        :param fin_rango: Valor final del rango de generación.
        """
        super(TRandom, self).__init__()
        if comienzo_rango < fin_rango:
            self._comienzo_rango = comienzo_rango
            self._fin_rango = fin_rango
        else:
            raise ValueError

    def get_comienzo_rango(self):
        return self._comienzo_rango

    def get_fin_rango(self):
        return self._fin_rango

    def set_comienzo_rango(self, valor):
        self._comienzo_rango = valor

    def set_fin_rango(self, valor):
        self._fin_rango = valor

    comienzo_rango = property(get_comienzo_rango, set_comienzo_rango, None, "Valor inicial del rango de generación")
    fin_rango = property(get_fin_rango, set_fin_rango, None, "Valor final del rango de generación")
