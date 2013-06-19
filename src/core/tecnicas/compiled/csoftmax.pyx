#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import cython
import random

import decimal


@cython.locals(rnd_valor=cython.int,
               cant_ranuras=cython.int,
               valor_param_parcial=cython.double)
@cython.boundscheck(False)
@cython.wraparound(False)
def obtener_accion(vecinos, cant_ranuras, valor_param_parcial):
    rnd_valor = random.randint(0, cant_ranuras - 1)

    intervalos_probabilidad = obtener_probabilidades(vecinos, cant_ranuras, valor_param_parcial)

    for key, intervalo in intervalos_probabilidad.iteritems():
        if intervalo[0] <= rnd_valor <= intervalo[1]:
            return key

    return None


@cython.locals(cant_ranuras=cython.int,
               valor_param_parcial=cython.double,
               val_param_parcial=cython.double,
               sigma=cython.int,
               sumatoria=cython.long,
               ext_sup=cython.long,
               calculo=cython.long,
               probabilidad_vecino=cython.long
               )
@cython.boundscheck(False)
@cython.wraparound(False)
def obtener_probabilidades(vecinos, cant_ranuras, val_param_parcial):
    probabilidades_vecinos = {}
    sigma = 0

    # Calcula las probabilidades de cada vecino
    valor_param_parcial = val_param_parcial

    for key, q_valor in vecinos.iteritems():
        try:
            exponente = decimal.Decimal(q_valor) / decimal.Decimal(valor_param_parcial)
            probabilidad_vecino = exponente.exp()
            probabilidades_vecinos[key] = probabilidad_vecino
            sigma += probabilidad_vecino
        except OverflowError:
            pass
        except decimal.Overflow:
            raise decimal.Overflow

    # Calcula las probabilidades de cada vecino normalizadas
    for key, prob in probabilidades_vecinos.iteritems():
        probabilidades_vecinos[key] = prob / sigma

    sumatoria = 0
    intervalos = {}
    cant_ranuras = cant_ranuras

    redondear = round
    for key, prob in probabilidades_vecinos.iteritems():
        aux = sumatoria
        calculo = redondear(prob * cant_ranuras)
        sumatoria += calculo
        ext_sup = sumatoria - 1

        if cant_ranuras > aux <= ext_sup:
            intervalos[key] = (aux, ext_sup)

    return intervalos
