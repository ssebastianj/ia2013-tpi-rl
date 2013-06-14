#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import numpy


def get_estados(dimension, estado_class, tipos_estados, estados_num):
    ancho = dimension[0]
    alto = dimension[1]

    # Crear GridWorld de estados
    estados = numpy.empty((ancho, alto), estado_class)
    coordenadas = []

    # Crear una lista de listas
    for i in xrange(1, alto + 1):
        fila = numpy.empty((1, ancho), estado_class)
        for j in xrange(1, ancho + 1):
            fila[0][j - 1] = estado_class(i, j, tipos_estados[estados_num[i - 1][j - 1]])
            coordenadas.append((i, j))
        estados[i - 1] = fila

    return (estados, coordenadas)
