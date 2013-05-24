#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import math
import random

from decimal import Decimal
from core.tecnicas.tecnica import QLTecnica


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador Softmax.

        :param tau: Parámetro Tau de la técnica.
        """
        super(Softmax, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = tau
        self._val_param_parcial = tau
        self._name = "Softmax"

    def obtener_accion(self, vecinos):
        rnd_valor = random.uniform(0, 1)

        probabilidades_vecinos = self.obtener_probabilidades(vecinos)

        for key, value in probabilidades_vecinos.iteritems():
            if rnd_valor <= value:
                estado = key

        logging.debug("Estado Elegido: {0}".format(estado))
        return estado

    def obtener_probabilidades(self, vecinos):
        probabilidades_vecinos = {}

        # Calcula las probabilidades de cada vecino
        for key, q_valor in vecinos.iteritems():
            exponente = Decimal(float(q_valor) / self._val_param_parcial)
            probabilidad_vecino = math.exp(exponente.adjusted())
            probabilidades_vecinos[key] = probabilidad_vecino

        logging.debug("Probabilidades de vecinos: {0}"
                      .format(probabilidades_vecinos))

        # N = constante de Normalización
        # Convertirlo a un número flotante para solucionar problema al dividir
        n = float(sum(probabilidades_vecinos.values()))

        logging.debug("Valor de constante de normalización N: {0}".format(n))

        probabilidades_vecinos_normalizadas = {}
        # Calcula las probabilidades de cada vecino normalizadas
        for key, value in probabilidades_vecinos.iteritems():
            probabilidades_vecinos_normalizadas[key] = value / n

        # Si éste cálculo está bien deberia dar 1
        logging.debug("Sumatoria de las Probabilidades Normalizadas: {0}"
                      .format(sum(probabilidades_vecinos_normalizadas.values())))

        # Realiza la Sumatoria Ponderada de las probabilidades de los vecinos
        probabilidades_vecinos_ponderadas = {}
        prob_vec_norm_aux = list(probabilidades_vecinos_normalizadas.iteritems())
        for i in xrange(len(prob_vec_norm_aux)):
            sumatoria = 0
            for j in xrange(i + 1):
                sumatoria += prob_vec_norm_aux[j][1]
            probabilidades_vecinos_ponderadas[prob_vec_norm_aux[j][0]] = sumatoria

        logging.debug("Probabilidades ponderadas: {0}"
                      .format(probabilidades_vecinos_ponderadas))

        return probabilidades_vecinos_ponderadas

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

    def get_tau_general(self):
        return self._val_param_general

    def set_tau_general(self, valor):
        self._val_param_general = valor

    def get_tau_parcial(self):
        return self._val_param_parcial

    def set_tau_parcial(self, valor):
        self._val_param_parcial = valor

    tau_general = property(get_tau_general,
                           set_tau_general,
                           None,
                           u"Parámetro Tau General de la técnica")

    tau_parcial = property(get_tau_parcial,
                           set_tau_parcial,
                           None,
                           u"Parámetro Tau Parcial de la técnica")
