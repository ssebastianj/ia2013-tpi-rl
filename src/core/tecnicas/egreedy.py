#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica


class EGreedy(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, epsilon):
        u"""
        Inicializador.

        :param epsilon: Parámetro Epsilon de la técnica.
        """
        super(EGreedy, self).__init__()
        self._epsilon = epsilon

    def get_epsilon(self):
        return self._epsilon

    def set_epsilon(self, valor):
        self._epsilon = valor

    def obtener_accion(self, matriz_q, vecinos):
        # Generar un número aleatorio para saber cuál política usar
        valor = random.uniform(0, 1)
        if ((valor >= 0) and (valor <= (1 - self._epsilon))):
            # EXPLOTAR
            print "EXPLOTAR"
            maximo = 0
            estados_qmax = []
            for i in vecinos:
                print "X:{0} Y:{1}".format(i.fila, i.columna)  # FIXME: Eliminar print de debug
                q_valor = matriz_q[i.fila - 1][i.columna - 1]
                print "Q Valor: {0}".format(q_valor)  # FIXME: Eliminar print de debug
                if q_valor > maximo:
                    maximo = q_valor
                    estados_qmax = [i]
                elif q_valor == maximo:
                    estados_qmax.append(i)

            # Comprobar si hay estados con recompensas iguales y elegir uno
            # de forma aleatoria
            if len(estados_qmax) == 1:
                estado_qmax = estados_qmax[0]
                print "Existe un sólo estado vecino máximo"  # FIXME: Eliminar print de debug
            else:
                estado_qmax = self.elegir_estado_aleatorio(estados_qmax)
                print "Existen varios estados con igual recompensa"  # FIXME: Eliminar print de debug
        else:
            # EXPLORAR
            print "EXPLORAR"
            # Elegir un estado vecino de forma aleatoria
            estado_qmax = self.elegir_estado_aleatorio(vecinos)
        return estado_qmax

    def elegir_estado_aleatorio(self, lista_estados):
        u"""
        Dada una lista de estados vecinos elige aleatoriamente sólo uno.

        :param lista_estados: Lista de vecinos de un estado dado.
        """
        indice = random.randint(0, (len(lista_estados) - 1))
        return lista_estados[indice]

    epsilon = property(get_epsilon, set_epsilon, None, u"Parámetro Epsilon de la técnica")


class Greedy(EGreedy):
    u"""Técnica Greedy"""
    def __init__(self):
        u"""
        Inicializador
        """
        super(Greedy, self).__init__(0)
        self._epsilon = 0
