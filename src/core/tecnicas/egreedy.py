#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica



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

    def obtener_accion(self, matriz_q, vecinos):
        valor = random.uniform(0, 1)
        if ((valor >= 0) and (valor <= (1 - self._epsilon))):
            # esta tecnica es de explotaciòn
            print "EXPLOTAR"
            maximo = 0
            estado_qmax = None
            for i in vecinos:
                print i.fila, i.columna
                q_valor = matriz_q[i.fila - 1][i.columna - 1]
                print q_valor
                if q_valor >= maximo:
                    maximo = q_valor
                    estado_qmax = i
                # Si existen varios estados con el mismo q_maximo, por defecto se elige el último
        else:
            # tecnica de exploraciòn
            print "EXPLORAR"
            indice = random.randint(0, (len(vecinos) - 1))
            estado_qmax = vecinos[indice]
        return estado_qmax

    epsilon = property(get_epsilon, set_epsilon, None, u"Parámetro Epsilon de la técnica")


class Greedy(EGreedy):
    u"""Técnica Greedy"""
    def __init__(self):
        u"""
        Inicializador
        """
        super(Greedy, self).__init__(0.00)
        self._epsilon = 0.00
