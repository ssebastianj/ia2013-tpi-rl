#!/usr/bin/env python
# -*- coding: utf-8 -*-


class QLTecnica(object):
    u"""Técnica para Q-Learning"""
    def __init__(self, paso_decremento=0, intervalo_decremento=0):
        super(QLTecnica, self).__init__()
        self._paso_decremento = paso_decremento
        self._intervalo_decremento = intervalo_decremento
        self._val_param_general = None
        self._val_param_parcial = self._val_param_general
        self._name = "QLTecnica"

    def obtener_accion(self, matriz_q, vecinos):
        u"""
        Devuelve un sólo estado vecino de una lista de estados vecinos.

        :param matriz_q: Matriz Q a utilizar.
        :param vecinos: Vecinos del estado actual.
        """
        pass

    def decrementar_parametro(self):
        pass

    def get_paso_decremento(self):
        return self._paso_decremento

    def set_paso_decremento(self, paso):
        self._paso_decremento = paso

    def get_intervalo_decremento(self):
        return self._intervalo_decremento

    def set_intervalo_decremento(self, valor):
        self._intervalo_decremento = valor

    def get_valor_param_general(self):
        return self._val_param_general

    def set_valor_param_general(self, valor):
        self._val_param_general = valor
        self._val_param_parcial = valor

    def _get_valor_param_parcial(self):
        return self._val_param_parcial

    def restaurar_val_parametro(self):
        self._val_param_parcial = self._val_param_general

    def get_name(self):
        return self._name

    def set_name(self, nombre):
        self._name = nombre

    paso_decremento = property(get_paso_decremento,
                               set_paso_decremento,
                               None,
                               "Valor de decremento")

    intervalo_decremento = property(get_intervalo_decremento,
                                    set_intervalo_decremento,
                                    None,
                                    u"Número entero indicando cada cuantas \
                                    iteraciones decrementar el parámetro \
                                    utilizando un \
                                    valor de paso dado")

    valor_param_general = property(get_valor_param_general,
                                   set_valor_param_general,
                                   None,
                                   u"Número indicando el valor del \
                                   parámetro general")

    valor_param_parcial = property(_get_valor_param_parcial,
                                   None,
                                   None,
                                   u"Número indicando el valor del \
                                   parámetro parcial")

    nombre = property(get_name, set_name, None, "Nombre de la técnica")
