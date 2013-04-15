#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.tecnicas.tecnica import QLTecnica
import random
from test.test_iterlen import len


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador

        :param tau: Parámetro Tau de la técnica.
        """
        super(Softmax, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = tau




    def obtener_accion(self, matriz_q, vecinos):

        valor = random.uniform(0, 1)

        probabilidades_vecinos = self.obtener_probabilidades(matriz_q, vecinos)

        for i in range (0, len(vecinos)):
            if valor <= probabilidades_vecinos[i]:
                estado = vecinos[i]

        print "Este es el estado Elegido: {0}".format(estado)
        return estado



    def obtener_probabilidades(self, matriz_q, vecinos):

        probabilidades_vecinos = []
        e = 2.71828

        # Calcula las probabilidades de cada vecino
        for i in vecinos:
            q_valor_vecino = matriz_q[i.fila - 1][i.columna - 1]
            probabilidad_vecino = e ** (q_valor_vecino / self.tau_general)
            probabilidades_vecinos.append(probabilidad_vecino)

            print "Esta es la probabilidad del vecino: {0}".format(probabilidad_vecino)



        # N = constante de Normalización
        N = sum(probabilidades_vecinos)
        print "Este es el valor de N : {0}".format(N)



        probabilidades_vecinos_normalizadas = []

        # Calcula las probabilidades de cada vecino normalizadas
        for i in range (0, len(vecinos)):
            probabilidad_vecino_normalizada = probabilidades_vecinos[i] / N
            probabilidades_vecinos_normalizadas.append(probabilidad_vecino_normalizada)


        print "Sumatoria de las probabilidades Normalizadas: {0}".format(sum(probabilidades_vecinos_normalizadas))
        """ Si este calculo está bien deberia dar 1"""


        # Realiza la Sumatoria Ponderada de las probabilidades de los vecinos
        probabilidades_vecinos_ponderadas = []


        for i in range(0, len(vecinos)):
            probabilidad_vecino_ponderada = 0
            for j in range(0, i + 1):
                probabilidad_vecino_ponderada += probabilidades_vecinos_normalizadas[j]

            print "Esta es la probabilidad Ponderada del vecino: {0}".format(probabilidad_vecino_ponderada)
            probabilidades_vecinos_ponderadas.append(probabilidad_vecino_ponderada)

        print "Esta es la probabilidad ponderada del ultimo vecino: {0}".format(probabilidades_vecinos_ponderadas[len(vecinos) - 1])
        """Si este calculo esta bien deberia dar 1"""

        return probabilidades_vecinos_ponderadas



    def decrementar_parametro(self):
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
