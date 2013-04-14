#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.tecnicas.tecnica import QLTecnica


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador

        :param tau: Parámetro Tau de la técnica.
        """
        super(Softmax, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = tau

    def obtener_accion(self, matriz_q, vecinos):
        pass

    def decrementar_parametro(self):
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
