#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO: Implementar Q-Learning
class QLearning(object):
    u"""Algoritmo QLearning"""
    def __init__(self, gamma):
        """
        :param gamma: Parámetro Gamma de QLearning.
        """
        super(QLearning, self).__init__()
        self._gamma = gamma

    def get_gamma(self):
        return self._gamma

    def set_gamma(self, valor):
        self._gamma = valor

    gamma = property(get_gamma, set_gamma, None, u"Parámetro Gamma de QLearning.")
