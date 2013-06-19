#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random

try:
    import cdecimal as decimal
except ImportError:
    import decimal

from core.tecnicas.tecnica import QLTecnica

import pyximport; pyximport.install()
from core.tecnicas.compiled import csoftmax


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador Softmax.

        :param tau: Parámetro Tau de la técnica.
        :param paso_decremento: Valor flotante con el que se decrementará el parámetro general.
        :param intervalo_decremento: Intervalo de episodios entre los cuales se realizará el decremento.
        """
        super(Softmax, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = decimal.Decimal(tau)
        self._val_param_parcial = decimal.Decimal(tau)
        self._name = "Softmax"
        self._paso_decremento = decimal.Decimal(paso_decremento)
        self._intervalo_decremento = decimal.Decimal(intervalo_decremento)

        # Establecer cantidad de ranuras
        self.cant_ranuras = 100

        # Establecer precisión de decimales a 5 dígitos
        decimal.getcontext().prec = 2

    def obtener_accion(self, vecinos):
        u"""
        Dado un conjunto de vecinos selecciona acorde uno de ellos.

        :param vecinos: Diccionario conteniendo los vecinos de un estado.
        """
        return csoftmax.obtener_accion(vecinos, self.cant_ranuras, self._val_param_parcial)

    def decrementar_parametro(self):
        u"""
        Decrementa el valor del parámetro generar en función del paso de decremento.
        """
        decremento = self._val_param_parcial - self._paso_decremento
        # No puede ser igual a cero sino se estaría ante un caso de
        # técnica Greedy (E = 0)
        if decremento > 0:
            self._val_param_parcial = decremento
        else:
            # Restaurar valor original de parámetro
            # self.restaurar_val_parametro()
            pass

    def get_tau_general(self):
        return self._val_param_general

    def set_tau_general(self, valor):
        self._val_param_general = valor

    def get_tau_parcial(self):
        return self._val_param_parcial

    def set_tau_parcial(self, valor):
        self._val_param_parcial = valor

    tau_general = property(get_tau_general,
                           set_tau_general,
                           None,
                           u"Parámetro Tau General de la técnica")

    tau_parcial = property(get_tau_parcial,
                           set_tau_parcial,
                           None,
                           u"Parámetro Tau Parcial de la técnica")
