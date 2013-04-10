#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.tecnicas.tecnica import QLTecnica


# TODO: Implementar técnica
class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau):
        u"""
        Inicializador

        :param tau: Parámetro Tau de la técnica.
        """
        super(Softmax, self).__init__()
        self._tau = tau

    def get_tau(self):
        return self._tau

    def set_tau(self, valor):
        self._tau = valor

    tau = property(get_tau, set_tau, None, u"Parámetro Tau de la técnica")
