#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.tecnicas.tecnica import QLTecnica


# TODO: Implementar técnica E-Greedy
class EGreedy(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, epsilon):
        u"""
        Inicializador

        :param epsilon: Parámetro Epsilon de la técnica.
        """
        super(EGreedy, self).__init__()
        self._epsilon = epsilon

    def get_epsilon(self):
        return self._epsilon

    def set_epsilon(self, valor):
        self._epsilon = valor

    epsilon = property(get_epsilon, set_epsilon, None, u"Parámetro Epsilon de la técnica")
