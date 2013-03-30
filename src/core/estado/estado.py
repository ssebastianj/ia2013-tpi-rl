#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tools.enum import enum

TipoEstadoIntermedio = enum(EXCELENTE=0, BUENO=1, MALO=2, PARED=3)
TipoEstadoId = enum(INICIAL=0, INTERMEDIO=1, FINAL=2, AGENTE=3)


class TipoEstado(object):
    """Clase TipoEstado"""
    def __init__(self, ide, recompensa, nombre, letra=None, icono=None):
        super(TipoEstado, self).__init__()
        self._ide = ide
        self._nombre = nombre
        self._recompensa = recompensa
        self._icono = icono
        self._letra = letra

    def _get_ide(self):
        return self._ide

    def _set_ide(self, valor):
        self._ide = valor

    def _get_nombre(self):
        return self._nombre

    def _set_nombre(self, valor):
        self._nombre = valor

    def _get_recompensa(self):
        return self._recompensa

    def _set_recompensa(self, valor):
        self._recompensa = valor

    def _get_letra(self):
        return self._letra

    def _set_letra(self, valor):
        self._letra = valor

    def _get_icono(self):
        return self._icono

    def _set_icono(self, icono):
        self._icono = icono

    ide = property(_get_ide, _set_ide, None, "Propiedad ID")
    nombre = property(_get_icono, _set_icono, None, "Propiedad Nombre")
    recompensa = property(_get_recompensa, _set_recompensa, None, "Propiedad Recompensa")
    letra = property(_get_letra, _set_letra, None, "Propiedad Letra")
    icono = property(_get_icono, _set_icono, None, "Propiedad Icono")


class Estado(object):
    """Clase Estado"""
    def __init__(self, fila, columna, tipo):
        super(Estado, self).__init__()
        self._fila = fila
        self._columna = columna
        self._tipo = tipo

    def _get_fila(self):
        return self._fila

    def _set_fila(self, valor):
        self._fila = valor

    def _get_columna(self):
        return self._columna

    def _set_columna(self, valor):
        self._columna = valor

    def _get_tipo(self):
        return self._tipo

    def _set_tipo(self, valor):
        self._tipo = valor

    fila = property(_get_fila, _set_fila, None, "Propiedad Fila del estado")
    columna = property(_get_columna, _set_columna, None, "Propiedad Columna del estado")
    tipo = property(_get_tipo, _set_tipo, None, "Propiedad Tipo del estado")
