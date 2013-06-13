#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
import decimal
from core.tecnicas.tecnica import QLTecnica


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador Softmax.

        :param tau: Parámetro Tau de la técnica.
        """
        super(Softmax, self).__init__(paso_decremento, intervalo_decremento)
        self._val_param_general = decimal.Decimal(tau)
        self._val_param_parcial = decimal.Decimal(tau)
        self._name = "Softmax"
        self._paso_decremento = decimal.Decimal(paso_decremento)
        self._intervalo_decremento = decimal.Decimal(intervalo_decremento)

        # Establecer cantidad de ranuras
        self.cant_ranuras = 100

        # Establecer precisión de decimales a 5 dígitos
        decimal.getcontext().prec = 2

    def obtener_accion(self, vecinos):
        rnd_valor = random.randint(0, self.cant_ranuras - 1)

        intervalos_probabilidad = self.obtener_probabilidades(vecinos)

        for key, intervalo in intervalos_probabilidad.iteritems():
            if intervalo[0] <= rnd_valor <= intervalo[1]:
                return key

        return None

    def obtener_probabilidades(self, vecinos):
        probabilidades_vecinos = {}
        sigma = 0

        # Calcula las probabilidades de cada vecino
        for key, q_valor in vecinos.iteritems():
            try:
                exponente = decimal.Decimal(q_valor) / self._val_param_parcial
                probabilidad_vecino = exponente.exp()
                probabilidades_vecinos[key] = probabilidad_vecino
                sigma += probabilidad_vecino
            except OverflowError:
                pass
            except decimal.Overflow:
                pass

        # N = constante de Normalización
        # n = sum(probabilidades_vecinos.itervalues())

        # Calcula las probabilidades de cada vecino normalizadas
        for key, prob in probabilidades_vecinos.iteritems():
            probabilidades_vecinos[key] = prob / sigma

        sumatoria = 0
        intervalos = {}
        cant_ranuras = self.cant_ranuras

        for key, prob in probabilidades_vecinos.iteritems():
            aux = sumatoria
            calculo = round(prob * cant_ranuras)
            sumatoria += calculo
            ext_sup = sumatoria - 1

            if cant_ranuras > aux <= ext_sup:
                intervalos[key] = (aux, ext_sup)

        return intervalos

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
