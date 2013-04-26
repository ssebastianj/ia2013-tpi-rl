#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import random
from core.tecnicas.tecnica import QLTecnica


class EGreedy(QLTecnica):
    u"""Técnica EGreedy"""
    def __init__(self, epsilon, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador.

        :param epsilon: Parámetro Epsilon de la técnica.
        """
        super(EGreedy, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = epsilon
        self._name = "EGreedy"

    def get_epsilon_general(self):
        return self._val_param_general

    def set_epsilon_general(self, valor):
        self._val_param_general = valor

    def get_epsilon_parcial(self):
        return self._val_param_parcial

    def set_epsilon_parcial(self, valor):
        self._val_param_parcial = valor

    def obtener_accion(self, vecinos):
        logging.debug("Vecinos para EGreedy: {0}".format(vecinos))

        # Generar un número aleatorio para saber cuál política usar
        valor = random.uniform(0, 1)
        if ((valor >= 0) and (valor <= (1 - self.epsilon_parcial))):
            # EXPLOTAR
            logging.debug("EXPLOTAR")  # FIXME: Eliminar print de debug

            maximo = None
            estados_qmax = []
            for key, value in vecinos.items():
                logging.debug("X:{0} Y:{1}".format(*key))  # FIXME: Eliminar print de debug
                q_valor = value
                logging.debug("Q Valor: {0}".format(q_valor))  # FIXME: Eliminar print de debug

                if maximo is None:
                    maximo = q_valor

                if q_valor > maximo:
                    maximo = q_valor
                    estados_qmax = [key]
                elif q_valor == maximo:
                    estados_qmax.append(key)

            logging.debug("Estados Q-Max: {0}".format(estados_qmax))

            # Comprobar si hay estados con recompensas iguales y elegir uno
            # de forma aleatoria
            if len(estados_qmax) == 1:
                estado_qmax = estados_qmax[0]
                logging.debug("Existe un sólo estado vecino máximo")  # FIXME: Eliminar print de debug
            else:
                estado_qmax = self.elegir_estado_aleatorio(estados_qmax)
                logging.debug("Existen varios estados con igual recompensa")  # FIXME: Eliminar print de debug
        else:
            # EXPLORAR
            logging.debug("EXPLORAR")  # FIXME: Eliminar print de debug
            # Elegir un estado vecino de forma aleatoria
            estado_qmax = self.elegir_estado_aleatorio(vecinos.keys())
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
            self.restaurar_val_parametro()

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
    def __init__(self):
        u"""
        Inicializador
        """
        super(Greedy, self).__init__(0)
        self._epsilon = 0
        self._name = "Greedy"
