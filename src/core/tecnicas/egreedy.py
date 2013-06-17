#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
from core.tecnicas.tecnica import QLTecnica


class EGreedy(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, epsilon, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador.

        :param epsilon: Parámetro Epsilon de la técnica.
        """
        super(EGreedy, self).__init__()
        self._val_param_general = epsilon
        self._val_param_parcial = epsilon
        self._name = "EGreedy"
        self._paso_decremento = paso_decremento
        self._intervalo_decremento = intervalo_decremento

    def get_epsilon_general(self):
        return self._val_param_general

    def set_epsilon_general(self, valor):
        self._val_param_general = valor

    def get_epsilon_parcial(self):
        return self._val_param_parcial

    def set_epsilon_parcial(self, valor):
        self._val_param_parcial = valor

    def obtener_accion(self, vecinos):
        # Generar un número aleatorio para saber cuál política usar
        random_num = random.uniform(0, 1)
        elegir_estado_aleatorio = self.elegir_estado_aleatorio

        if 0 <= random_num <= (1 - self.epsilon_parcial):
            # EXPLOTAR
            maximo = None
            estados_qmax = []
            eq_append = estados_qmax.append

            for key, value in vecinos.iteritems():
                q_valor = value

                try:
                    if q_valor > maximo:
                        maximo = q_valor
                        estados_qmax = [key]
                    elif q_valor == maximo:
                        eq_append(key)
                except TypeError:
                    maximo = q_valor

            # Comprobar si hay estados con recompensas iguales y elegir uno
            # de forma aleatoria
            long_vecinos = len(estados_qmax)
            if long_vecinos == 1:
                estado_qmax = estados_qmax[0]
            elif long_vecinos > 1:
                estado_qmax = elegir_estado_aleatorio(estados_qmax)
            else:
                pass
        else:
            # EXPLORAR
            # Elegir un estado vecino de forma aleatoria
            estado_qmax = elegir_estado_aleatorio(vecinos.keys())
        return estado_qmax

    def elegir_estado_aleatorio(self, lista_estados):
        u"""
        Dada una lista de estados vecinos elige aleatoriamente sólo uno.
        Fuente: http://stackoverflow.com/questions/4859292/get-random-value-in-python-dictionary

        :param lista_estados: Lista de vecinos de un estado dado.
        """
        return random.choice(lista_estados)

    def decrementar_parametro(self):
        decremento = self._val_param_parcial - self._paso_decremento
        # No puede ser igual a cero sino se estaría ante un caso de
        # técnica Greedy (E = 0)
        if decremento > 0:
            self._val_param_parcial = decremento
        else:
            # Restaurar valor original de parámetro
            # self.restaurar_val_parametro()
            pass

    epsilon_general = property(get_epsilon_general,
                               set_epsilon_general,
                               None,
                               u"Parámetro Epsilon General de la técnica")

    epsilon_parcial = property(get_epsilon_parcial,
                               set_epsilon_parcial,
                               None,
                               u"Parámetro Epsilon Parcial de la técnica")


class Greedy(EGreedy):
    u"""Técnica Greedy"""
    def __init__(self, epsilon=0, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador
        """
        super(Greedy, self).__init__(0, 0, 0)
        self._epsilon = 0
        self._name = "Greedy"
