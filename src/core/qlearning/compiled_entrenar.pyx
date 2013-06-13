#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random


def sumar_avg_rwds(matriz_avg_rwd):
    return sum([datos[1] / float(datos[0])
               for fila in matriz_avg_rwd
               for datos in fila
               if datos[0] != 0]) / float(len(matriz_avg_rwd))


def obtener_q_maximo(vecinos_estado_elegido):
    return max([q_val for q_val in vecinos_estado_elegido.values()])


def get_estado_inicial_random(dimension, matriz_r, tipos_vecinos_excluidos):
    x_act, y_act = generar_estado_aleatorio(dimension)

    # Generar estados aleatorios hasta que las coordenadas no
    # coincidan con las de un tipo excluido
    estado_actual = matriz_r[x_act - 1][y_act - 1]
    tipo_estado = estado_actual[0]

    while tipo_estado in tipos_vecinos_excluidos:
        x_act, y_act = generar_estado_aleatorio(dimension)
        estado_actual = matriz_r[x_act - 1][y_act - 1]

    return estado_actual


def generar_estado_aleatorio(dimension):
    # Devolver un estado seleccionado aleatoriamente del conjunto de vecinos
    return (random.randint(1, dimension[0]), random.randint(1, dimension[1]))
