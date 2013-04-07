#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from core.estado.estado import Estado, TipoEstado, TIPOESTADO


class GridWorld(object):
    """Clase GridWorld"""
    def __init__(self, ancho, alto):
        """
        @param ancho: Ancho
        @param alto: Alto
        @param estados: Conjunto de estados
        """
        super(GridWorld, self).__init__()
        self._ancho = ancho
        self._alto = alto
        self._tipos_estados = None
        self._estados = None
        self._inicializar_tipos_estados()
        self._inicializar_estados()

    def _inicializar_tipos_estados(self):
        """
        Inicializa los distintos tipos de estados
        """
        # Identificadores de estado reservados
        # Ide = 0 (Estado Intermedio)
        # Ide = 1 (Estado Inicial)
        # Ide = 2 (Estado Final)
        # Ide = 3 (Agente)

        self._tipos_estados = []
        # Estado Inicial
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INICIAL, None, "Inicial", "I", None))
        # Estado Final
        self._tipos_estados.append(TipoEstado(TIPOESTADO.FINAL, None, "Final", "F", None))
        # Estado Agente
        self._tipos_estados.append(TipoEstado(TIPOESTADO.AGENTE, None, "Agente", "A", None))
        # Estados Intermedios
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INTERMEDIO, 100, "Excelente", "E", None))
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INTERMEDIO, 50, "Bueno", "B", None))
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INTERMEDIO, 10, "Malo", "M", None))
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INTERMEDIO, 0, "Neutro", "", None))
        self._tipos_estados.append(TipoEstado(TIPOESTADO.INTERMEDIO, -100, "Pared", "P", None))

    def _inicializar_estados(self, default=None):
        """
        Armar la matriz de estados con un tipo de estado predeterminado
        """
        if default is None:
            default_tipo = TipoEstado(TIPOESTADO.INTERMEDIO, 0, "Neutro", "N", None)

        self._estados = []
        for i in range(1, self._alto + 1):
            fila = []
            for j in range(1, self._ancho + 1):
                fila.append(Estado(i, j, default_tipo))
            self._estados.append(fila)

    def get_estado(self, i, j):
        return self._estados[i][j]

    def set_estado(self, estado):
        if isinstance(estado, Estado):
            self._estados[estado.tipo.fila][estado.tipo.columna] = estado
        else:
            raise ValueError

    def get_ancho(self):
        return self._ancho

    def set_ancho(self, valor):
        self._ancho = valor

    def get_alto(self):
        return self._alto

    def set_alto(self, valor):
        self._alto = valor

    def get_estados(self):
        return self._estados

    def set_estados(self, valor):
        self._estados = valor

    def get_tipos_estados(self):
        return self._tipos_estados

    def set_tipos_estados(self, valor):
        self._tipos_estados = valor

    ancho = property(get_ancho, set_ancho, None, "Ancho del GridWorld")
    alto = property(get_alto, set_alto, None, "Alto del GridWorld")
    estados = property(get_estados, set_estados, None, "Estados del GridWorld")
    tipos_estados = property(get_tipos_estados, set_tipos_estados, None, "Tipos de estados del GridWorld")
