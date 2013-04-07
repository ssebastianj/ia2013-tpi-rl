#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tools.enum import enum

# Identificadores de estado reservados
# Ide = 0 (Estado Neutro)
# Ide = 1 (Estado Inicial)
# Ide = 2 (Estado Final)
# Ide = 3 (Agente)
TIPOESTADO = enum(NEUTRO=0, INICIAL=1, FINAL=2, AGENTE=3)


class TipoEstado(object):
    """Clase TipoEstado"""
    def __init__(self, ide, recompensa, nombre, letra, icono=None):
        """
        @param ide: Identificador del estado
        @param recompensa: Recompensa devuelta
        @param nombre: Texto indicando el tipo de estado
        @param letra: Letra a mostrar en el GridWorld
        @param icono: Icono a mostrar en el GridWorld
        """
        super(TipoEstado, self).__init__()
        self._ide = ide
        self._nombre = nombre
        self._recompensa = recompensa
        self._icono = icono
        self._letra = letra

    def get_ide(self):
        return self._ide

    def set_ide(self, valor):
        self._ide = valor

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_recompensa(self):
        return self._recompensa

    def set_recompensa(self, valor):
        self._recompensa = valor

    def get_letra(self):
        return self._letra

    def set_letra(self, valor):
        self._letra = valor

    def get_icono(self):
        return self._icono

    def set_icono(self, icono):
        self._icono = icono

    ide = property(get_ide, set_ide, None, "Propiedad ID del Tipo de Estado")
    nombre = property(get_icono, set_icono, None, "Propiedad Nombre del Tipo de Estado")
    recompensa = property(get_recompensa, set_recompensa, None, "Propiedad Recompensa del Tipo de Estado")
    letra = property(get_letra, set_letra, None, "Propiedad Letra del Tipo de Estado")
    icono = property(get_icono, set_icono, None, "Propiedad Icono del Tipo de Estado")


class Estado(object):
    """Clase Estado"""
    def __init__(self, fila, columna, tipo):
        """
        @param fila: Fila que ocupa en el GridWorld
        @param columna: Columna que ocupa en el GridWorld
        @param tipo: Objeto indicando el tipo de estado
        """
        super(Estado, self).__init__()
        self._fila = fila
        self._columna = columna
        self._tipo = tipo

    def get_fila(self):
        return self._fila

    def set_fila(self, valor):
        self._fila = valor

    def get_columna(self):
        return self._columna

    def set_columna(self, valor):
        self._columna = valor

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, valor):
        self._tipo = valor

    fila = property(get_fila, set_fila, None, "Propiedad Fila del estado")
    columna = property(get_columna, set_columna, None, "Propiedad Columna del estado")
    tipo = property(get_tipo, set_tipo, None, "Propiedad Tipo del estado")
