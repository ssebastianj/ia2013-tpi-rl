#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import numpy

try:
    import cdecimal as decimal
except ImportError:
    import decimal

from core.tecnicas.tecnica import QLTecnica


class Softmax(QLTecnica):
    u"""Técnica Softmax"""
    def __init__(self, tau, paso_decremento=0, intervalo_decremento=0):
        u"""
        Inicializador Softmax.

        :param tau: Parámetro Tau de la técnica.
        :param paso_decremento: Valor flotante con el que se decrementará el parámetro general.
        :param intervalo_decremento: Intervalo de episodios entre los cuales se realizará el decremento.
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

    def obtener_accion(self, acciones):
        u"""
        Dado un conjunto de acciones selecciona acorde uno de ellos.

        :param acciones: Diccionario conteniendo los acciones de un estado.
        """
        # Cachear acceso a métodos y atributos
        rnd_func = numpy.random.randint
        np_where = numpy.where
        cant_ranuras = self.cant_ranuras

        # Armar intervalos de probabilidad
        intervalos_probabilidad = self.obtener_probabilidades(acciones)

        # Generar número aleatorio
        rnd_valor = rnd_func(0, cant_ranuras)
        # Obtener índice de acuerdo al intervalo de probabilidad
        idx = np_where(rnd_valor <= intervalos_probabilidad)[0][0]

        return idx

    def obtener_probabilidades(self, acciones):
        """
        Calcula y devuelve los intervalos de probabilidad para cada vecino.

        :param acciones: Diccionario conteniendo acciones de un estado.
        """
        # Calcula las probabilidades de cada vecino
        valor_param_parcial = self._val_param_parcial
        c_decimal = decimal.Decimal

        # Crear arreglo para almacenar cálculos
        probabilidades_acciones = numpy.empty(acciones.size, numpy.float)

        # Calcular probabilidades
        for i, q_valor in numpy.ndenumerate(acciones):
            try:
                exponente = c_decimal(q_valor) / valor_param_parcial
                # Calcular función exponencial
                probabilidades_acciones[i[0]] = exponente.exp()
            except OverflowError:
                pass
            except decimal.Overflow:
                raise decimal.Overflow

        # Constante de normalización
        sigma = numpy.nansum(probabilidades_acciones)

        # Calcular las probabilidades normalizadas de cada vecino
        probabilidades_acciones = numpy.true_divide(probabilidades_acciones, sigma)

        # Multiplicar por cantidad de ranuras
        probabilidades_acciones *= self.cant_ranuras
        # probabilidades_acciones = numpy.round(probabilidades_acciones * self.cant_ranuras)

        # probabilidades_acciones[probabilidades_acciones == 0] = numpy.nan
        # probabilidades_acciones[probabilidades_acciones < 1] = numpy.nan

        # Armar intervalos sumando de manera acumulada
        probabilidades_acciones = numpy.add(probabilidades_acciones * 0,
                                            numpy.add.accumulate(numpy.nan_to_num(probabilidades_acciones)))

        return probabilidades_acciones

    def decrementar_parametro(self):
        u"""
        Decrementa el valor del parámetro generar en función del paso de decremento.
        """
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
