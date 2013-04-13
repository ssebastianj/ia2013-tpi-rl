#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tools.enum import enum

# Identificadores de estado reservados
# Ide = 0 (Estado Inicial)
# Ide = 1 (Estado Final)
# Ide = 2 (Estado Agente)
# Ide = 3 (Neutro)
# Ide = 4 (Excelente)
# Ide = 5 (Bueno)
# Ide = 6 (Pared)
TIPOESTADO = enum(INICIAL=0,
                  FINAL=1,
                  AGENTE=2,
                  NEUTRO=3,
                  EXCELENTE=4,
                  BUENO=5,
                  MALO=6,
                  PARED=7)


class TipoEstado(object):
    """Clase TipoEstado"""
    def __init__(self, ide, recompensa, nombre, letra="", color="#FFFFFF", icono=None):
        """
        :param ide: Identificador del estado
        :param recompensa: Recompensa devuelta
        :param nombre: Texto indicando el tipo de estado
        :param letra: Letra a mostrar en el GridWorld
        :param color: Color a mostrar en el GridWorld
        :param icono: Icono a mostrar en el GridWorld
        """
        super(TipoEstado, self).__init__()
        self._ide = ide
        self._nombre = nombre
        self._recompensa = recompensa
        self._icono = icono
        self._letra = letra
        self._color = color

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

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    ide = property(get_ide, set_ide, None, "Propiedad ID del Tipo de Estado")
    nombre = property(get_nombre, set_nombre, None, "Propiedad Nombre del Tipo de Estado")
    recompensa = property(get_recompensa, set_recompensa, None, "Propiedad Recompensa del Tipo de Estado")
    letra = property(get_letra, set_letra, None, "Propiedad Letra del Tipo de Estado")
    icono = property(get_icono, set_icono, None, "Propiedad Icono del Tipo de Estado")
    color = property(get_color, set_color, None, "Color del Estado")


class Estado(object):
    """Clase Estado"""
    def __init__(self, fila, columna, tipo):
        """
        :param fila: Fila que ocupa en el GridWorld
        :param columna: Columna que ocupa en el GridWorld
        :param tipo: Objeto indicando el tipo de estado
        """
        super(Estado, self).__init__()
        self._fila = fila
        self._columna = columna
        self._tipo = tipo
        self._vecinos = None

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
        if isinstance(valor, TipoEstado):
            self._tipo = valor
        else:
            raise ValueError

    def get_vecinos(self):
        return self._vecinos

    fila = property(get_fila, set_fila, None, "Propiedad Fila del estado")
    columna = property(get_columna, set_columna, None, "Propiedad Columna del estado")
    tipo = property(get_tipo, set_tipo, None, "Propiedad Tipo del estado")
    vecinos = property(get_vecinos, None, None, "Propiedad Vecinos del estado")
