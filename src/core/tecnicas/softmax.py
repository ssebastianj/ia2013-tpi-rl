#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import math
import random
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
        self._name = "Softmax"

    def obtener_accion(self, matriz_q, vecinos):
        rnd_valor = random.uniform(0, 1)

        probabilidades_vecinos = self.obtener_probabilidades(matriz_q, vecinos)

        for i in xrange(0, len(vecinos)):
            if rnd_valor <= probabilidades_vecinos[i]:
                estado = vecinos[i]

        logging.debug("Estado Elegido: {0}".format(estado))
        return estado

    def obtener_probabilidades(self, matriz_q, vecinos):
        probabilidades_vecinos = []

        # Calcula las probabilidades de cada vecino
        for i in vecinos:
            q_valor_vecino = matriz_q[i.fila - 1][i.columna - 1]
            probabilidad_vecino = math.e ** (q_valor_vecino / float(self._val_param_parcial))
            probabilidades_vecinos.append(probabilidad_vecino)

            logging.debug("Probabilidad del vecino: {0}".format(probabilidad_vecino))

        # N = constante de Normalización
        # Convertirlo a un número flotante para solucionar problema al dividir
        n = sum(probabilidades_vecinos)
        logging.debug("Valor de constante de normalización N: {0}".format(n))

        probabilidades_vecinos_normalizadas = []
        # Calcula las probabilidades de cada vecino normalizadas
        for i in xrange(0, len(vecinos)):
            probabilidad_vecino_normalizada = probabilidades_vecinos[i] / float(n)
            probabilidades_vecinos_normalizadas.append(probabilidad_vecino_normalizada)

        # Si éste cálculo está bien deberia dar 1
        logging.debug("Sumatoria de las probabilidades Normalizadas: {0}"
                      .format(sum(probabilidades_vecinos_normalizadas)))

        # Realiza la Sumatoria Ponderada de las probabilidades de los vecinos
        probabilidades_vecinos_ponderadas = []
        for i in xrange(0, len(vecinos)):
            probabilidad_vecino_ponderada = 0
            for j in xrange(0, i + 1):
                probabilidad_vecino_ponderada += probabilidades_vecinos_normalizadas[j]

            logging.debug("Probabilidad ponderada del vecino: {0}"
                          .format(probabilidad_vecino_ponderada))
            probabilidades_vecinos_ponderadas.append(probabilidad_vecino_ponderada)

        # Si éste cálculo esta bien deberia dar 1
        logging.debug("Probabilidad ponderada del último vecino: {0}"
                      .format(probabilidades_vecinos_ponderadas[len(vecinos) - 1]))

        return probabilidades_vecinos_ponderadas

    def decrementar_parametro(self):
        decremento = self._val_param_parcial - self._paso_decremento
        # No puede ser igual a cero sino se estaría ante un caso de
        # técnica Greedy (E = 0)
        if decremento > 0:
            self._val_param_parcial = decremento
        else:
            # Restaurar valor original de parámetro
            self.restaurar_val_parametro()

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
