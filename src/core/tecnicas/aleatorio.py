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

    def obtener_accion(self, matriz_q, vecinos):
        indice = random.randint(0, (len(vecinos) - 1))
        return vecinos[indice]

    def decrementar_parametro(self):
        pass
