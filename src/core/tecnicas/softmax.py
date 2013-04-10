#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO: Implementar técnica
class Softmax(object):
    u"""Técnica Softmax"""
    def __init__(self, tau):
        super(Softmax, self).__init__()
        self._tau = tau

    def get_tau(self):
        return self._tau

    def set_tau(self, valor):
        self._tau = valor

    tau = property(get_tau, set_tau, None, u"Parámetro Tau de la técnica")
