#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica


class Aleatorio(QLTecnica):
    u"""Técnica Aleatorio"""
    def __init__(self, parametro=None, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador

        :param comienzo_rango: Valor inicial del rango de generación.
        :param fin_rango: Valor final del rango de generación.
        """
        super(Aleatorio, self).__init__()

    def obtener_accion(self, vecinos):
        u"""
        Dado un conjunto de vecinos selecciona acorde uno de ellos.

        :param vecinos: Diccionario conteniendo los vecinos de un estado.
        """
        return random.choice(list(vecinos.keys()))

    def decrementar_parametro(self):
        u"""
        Decrementa el parámetro general en un valor dado.
        """
        pass
