#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cython
import random


@cython.locals(epsilon_parcial=cython.double,
               random_num=cython.double,
               q_valor=cython.double,
               value=cython.double,
               long_vecinos=cython.int)
@cython.boundscheck(False)
@cython.wraparound(False)
def obtener_accion(vecinos, epsilon_parcial):
    # Generar un número aleatorio para saber cuál política usar
    random_num = random.uniform(0, 1)

    if 0 <= random_num <= (1 - epsilon_parcial):
        # EXPLOTAR
        maximo = None
        estados_qmax = []
        eq_append = estados_qmax.append

        for key, value in vecinos.iteritems():
            q_valor = value

            try:
                if q_valor > maximo:
                    maximo = q_valor
                    estados_qmax = [key]
                elif q_valor == maximo:
                    eq_append(key)
            except TypeError:
                maximo = q_valor

        # Comprobar si hay estados con recompensas iguales y elegir uno
        # de forma aleatoria
        long_vecinos = len(estados_qmax)
        if long_vecinos == 1:
            estado_qmax = estados_qmax[0]
        elif long_vecinos > 1:
            estado_qmax = elegir_estado_aleatorio(estados_qmax)
        else:
            pass
    else:
        # EXPLORAR
        # Elegir un estado vecino de forma aleatoria
        estado_qmax = elegir_estado_aleatorio(vecinos.keys())
    return estado_qmax


@cython.boundscheck(False)
@cython.wraparound(False)
def elegir_estado_aleatorio(lista_estados):
    return random.choice(lista_estados)
