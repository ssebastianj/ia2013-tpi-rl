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
        u"""
        Inicializa los distintos tipos de estados
        """
        self._tipos_estados = {}
        # Estado Inicial
        self._tipos_estados[TIPOESTADO.INICIAL] = TipoEstado(TIPOESTADO.INICIAL, None, "Inicial", "I")
        # Estado Final
        self._tipos_estados[TIPOESTADO.FINAL] = TipoEstado(TIPOESTADO.FINAL, None, "Final", "F")
        # Estado Agente
        self._tipos_estados[TIPOESTADO.AGENTE] = TipoEstado(TIPOESTADO.AGENTE, None, "Agente", "A")
        # Estados Intermedios
        self._tipos_estados[TIPOESTADO.EXCELENTE] = TipoEstado(TIPOESTADO.EXCELENTE, 100, "Excelente", "E")
        self._tipos_estados[TIPOESTADO.BUENO] = TipoEstado(TIPOESTADO.BUENO, 50, "Bueno", "B")
        self._tipos_estados[TIPOESTADO.MALO] = TipoEstado(TIPOESTADO.MALO, 10, "Malo", "M")
        self._tipos_estados[TIPOESTADO.NEUTRO] = TipoEstado(TIPOESTADO.NEUTRO, 0, "Neutro", "N")
        self._tipos_estados[TIPOESTADO.PARED] = TipoEstado(TIPOESTADO.PARED, -100, "Pared", "P")

    def _inicializar_estados(self, default=TIPOESTADO.NEUTRO):
        u"""
        Armar la matriz de estados con un tipo de estado predeterminado
        """
        default_tipo = self._tipos_estados[default]

        self._estados = []
        for i in range(1, self._alto + 1):
            fila = []
            for j in range(1, self._ancho + 1):
                fila.append(Estado(i, j, default_tipo))
            self._estados.append(fila)

    def get_estado(self, i, j):
        return self._estados[i][j]

    def set_estado(self, i, j, estado):
        if isinstance(estado, Estado):
            self._estados[i][j] = estado
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
