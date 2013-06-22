#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import numpy
import random
from core.tecnicas.tecnica import QLTecnica


class EGreedy(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, epsilon, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador.

        :param epsilon: Parámetro Epsilon de la técnica.
        :param paso_decremento: Valor flotante con el que se decrementará el parámetro general.
        :param intervalo_decremento: Intervalo de episodios entre los cuales se realizará el decremento.
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

    def obtener_accion(self, acciones):
        u"""
        Dado un conjunto de acciones selecciona acorde uno de ellos.

        :param acciones: Diccionario conteniendo los acciones de un estado.
        """
        # Generar un número aleatorio para saber cuál política usar
        random_num = random.uniform(0, 1)

        if 0 <= random_num <= (1 - self.epsilon_parcial):
            # EXPLOTAR
            estado_qmax = numpy.random.choice(numpy.where(acciones == numpy.nanmax(acciones))[0])
        else:
            # EXPLORAR
            # Elegir una acción de forma aleatoria
            estado_qmax = self.elegir_accion_aleatoria(acciones)
        return estado_qmax

    def elegir_accion_aleatoria(self, acciones):
        u"""
        Dada una lista de estados acciones elige aleatoriamente sólo uno.
        Fuente: http://stackoverflow.com/questions/4859292/get-random-value-in-python-dictionary

        :param acciones: Lista de acciones de un estado dado.
        """
        return numpy.random.choice(numpy.where(1 ^ numpy.isnan(acciones))[0])

    def decrementar_parametro(self):
        u"""
        Decrementa el parámetro general en un valor dado.
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
