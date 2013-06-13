#!/usr/bin/env python
#! -*- coding: utf-8 -*-

from __future__ import absolute_import

import decimal
import random


def obtener_probabilidades(vecinos, cant_ranuras, tau):
    probabilidades_vecinos = {}
    sigma = 0

    # Calcula las probabilidades de cada vecino
    for key, q_valor in vecinos.iteritems():
        try:
            exponente = decimal.Decimal(q_valor) / tau
            probabilidad_vecino = exponente.exp()
        except OverflowError:
            pass
        else:
            probabilidades_vecinos[key] = probabilidad_vecino
            sigma += probabilidad_vecino

    # N = constante de Normalización
    # n = sum(probabilidades_vecinos.itervalues())

    # Calcula las probabilidades de cada vecino normalizadas
    for key, prob in probabilidades_vecinos.iteritems():
        probabilidades_vecinos[key] = prob / sigma

    sumatoria = 0
    intervalos = {}

    for key, prob in probabilidades_vecinos.iteritems():
        aux = sumatoria
        calculo = round(prob * cant_ranuras)
        sumatoria += calculo
        ext_sup = sumatoria - 1

        if cant_ranuras > aux <= ext_sup:
            intervalos[key] = (aux, ext_sup)

    return intervalos


def get_estado(vecinos, cant_ranuras, tau):
    rnd_valor = random.randint(0, cant_ranuras - 1)

    intervalos_probabilidad = obtener_probabilidades(vecinos, cant_ranuras, tau)

    for key, intervalo in intervalos_probabilidad.iteritems():
        if intervalo[0] <= rnd_valor <= intervalo[1]:
            return key

    return None