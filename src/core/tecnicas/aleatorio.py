#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica


class Aleatorio(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self):
        u"""
        Inicializador

        :param comienzo_rango: Valor inicial del rango de generación.
        :param fin_rango: Valor final del rango de generación.
        """
        super(Aleatorio, self).__init__()

    def obtener_accion(self, vecinos):
        return random.choice(list(vecinos.keys()))

    def decrementar_parametro(self):
        pass
