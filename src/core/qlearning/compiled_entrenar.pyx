#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random
import numpy


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

    return (x_act, y_act, estado_actual)


def generar_estado_aleatorio(dimension):
    # Devolver un estado seleccionado aleatoriamente del conjunto de vecinos
    return (random.randint(1, dimension[0]), random.randint(1, dimension[1]))


def sumar_eltos_matriz(matriz):
    return sum([elto for fila in matriz
                for columna in fila
                for elto in columna[1].itervalues()])


def get_vecinos_estado(x, y, estados, coordenadas):
    vecinos = []
    for fila, columna in ((x + i, y + j)
                          for i in (-1, 0, 1) for j in (-1, 0, 1)
                          if i != 0 or j != 0):
        if (fila, columna) in coordenadas:
            vecinos.append(estados[fila - 1][columna - 1])
    return numpy.array(vecinos, object)


def get_matriz_avg_rwd(dimension, matriz_r):
    ancho = dimension[0]
    alto = dimension[1]

    matriz_avg_rwd = numpy.empty((ancho, alto), object)

    for i in xrange(0, alto):
        for j in xrange(0, ancho):
            vecinos = matriz_r[i][j][1]
            vecinos = {key: 0 for key in vecinos.iterkeys()}
            matriz_avg_rwd[i][j] = [0, 0]
    return matriz_avg_rwd


def get_matriz_q(dimension, matriz_q_aux, matriz_r, q_init_value_fn):
    ancho = dimension[0]
    alto = dimension[1]

    for i in xrange(0, alto):
        for j in xrange(0, ancho):
            tipo_estado = matriz_r[i][j][0]
            vecinos = matriz_r[i][j][1]
            vecinos = dict([(key, q_init_value_fn)
                            for key in vecinos.iterkeys()])
            matriz_q_aux[i][j] = (tipo_estado, vecinos)
    return matriz_q_aux


def get_matriz_r(dimension, matriz_r_aux, estados, coordenadas, tipos_vec_excluidos):
    ancho = dimension[0]
    alto = dimension[1]

    # Verificar si hay tipos de vecinos a excluir de la matriz R
    if tipos_vec_excluidos is None:
        tipos_vec_excluidos = []

    # Crear una lista de listas
    for i in xrange(1, alto + 1):
        fila = []
        for j in xrange(1, ancho + 1):
            # Obtener estado actual y su ID de tipo
            estado = estados[i - 1][j - 1]
            estado_ide = estado.tipo.ide
            # Obtener los estados vecinos del estado actual (i, j)
            vecinos = get_vecinos_estado(i, j, estados, coordenadas)
            # Agregar vecinos y su recompensa al estado
            # excluyendo los prohibidos
            recomp_and_vec = {}

            for vecino in vecinos:
                if vecino.tipo.ide not in tipos_vec_excluidos:
                    recomp_and_vec[(vecino.fila, vecino.columna)] = vecino.tipo.recompensa

            fila.append((estado_ide, recomp_and_vec))
        matriz_r_aux[i - 1] = fila
    return matriz_r_aux
