#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.tecnicas.tecnica import QLTecnica
from core.tecnicas.egreedy import EGreedy
from core.tecnicas.softmax import Softmax


# TODO: Implementar Q-Learning
class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gamma, tecnica):
        """
        Inicializador

        :param gamma: Parámetro Gamma de QLearning.
        :param tecnica: Técnica a utilizar.
        """
        super(QLearning, self).__init__()
        self._gamma = gamma
        self._tecnica = tecnica

    def get_gamma(self):
        return self._gamma

    def set_gamma(self, valor):
        self._gamma = valor

    def get_tecnica(self):
        return self._tecnica

    def set_tecnica(self, valor):
        if isinstance(valor, QLTecnica):
            self._tecnica = valor
        else:
            raise ValueError

    gamma = property(get_gamma, set_gamma, None, u"Parámetro Gamma de QLearning.")
    tecnica = property(get_tecnica, set_tecnica, None, u"Parámetro Técnica de QLearning.")
