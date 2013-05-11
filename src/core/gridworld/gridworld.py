#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import numpy
import threading
from core.estado.estado import Estado, TipoEstado, TIPOESTADO


class GridWorld(object):
    """Clase GridWorld"""
    def __init__(self, ancho, alto, estados=None, tipos_estados=None,
                 excluir_tipos_vecinos=None):
        u"""
        :param ancho: Ancho
        :param alto: Alto
        :param estados: Matriz MxN conteniendo los estados (lista de lista)
        :param tipos_estados: Lista conteniendo los tipos de estados disponibles
        :param excluir_tipos_vecinos: Lista conteniendo los identificadores de
                                      tipos de estado a excluir al momento de
                                      obtener los vecinos de un estado dado.
        """
        super(GridWorld, self).__init__()
        # FIXME: Logging
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] – %(threadName)-10s : %(message)s")

        self._ancho = ancho
        self._alto = alto
        self._tipos_estados = None
        self._estados = None
        self._coordenadas = None
        self._excluir_tipos_vecinos = excluir_tipos_vecinos
        self._inicializar_tipos_estados()
        self._inicializar_estados()

    def _inicializar_tipos_estados(self):
        u"""
        Inicializa los distintos tipos de estados
        """
        if self._tipos_estados is None:
            self._tipos_estados = {}
            # Estado Agente
            self._tipos_estados[TIPOESTADO.AGENTE] = TipoEstado(TIPOESTADO.AGENTE,
                                                                None,
                                                                "Agente",
                                                                "A",
                                                                "#FF2288")
            # Estados Intermedios
            self._tipos_estados[TIPOESTADO.EXCELENTE] = TipoEstado(TIPOESTADO.EXCELENTE,
                                                                   100,
                                                                   "Excelente",
                                                                   "E",
                                                                   "#BB0011")
            self._tipos_estados[TIPOESTADO.BUENO] = TipoEstado(TIPOESTADO.BUENO,
                                                               50,
                                                               "Bueno",
                                                               "B",
                                                               "#4F0ACC")
            self._tipos_estados[TIPOESTADO.MALO] = TipoEstado(TIPOESTADO.MALO, 10,
                                                              "Malo",
                                                              "M",
                                                              "#EB00A1")
            self._tipos_estados[TIPOESTADO.NEUTRO] = TipoEstado(TIPOESTADO.NEUTRO,
                                                                0,
                                                                "Neutro",
                                                                "N")
            self._tipos_estados[TIPOESTADO.PARED] = TipoEstado(TIPOESTADO.PARED,
                                                               - 100,
                                                               "Pared",
                                                               "P",
                                                               "#000000")
            # Estado Inicial
            self._tipos_estados[TIPOESTADO.INICIAL] = TipoEstado(TIPOESTADO.INICIAL,
                                                                 None,
                                                                 "Inicial",
                                                                 "I",
                                                                 "#FF0011")

            # Estado Final
            # La recompensa se calcula buscando la mayor recompensa entre los estados
            # intermedios y sumándole un número dadon con el objetivo de que el
            # Estado Final tenga la máxima recompensa de todos los estados.
            recompensa_estado_final = max([i.recompensa
                                           for i in self._tipos_estados.values()
                                           if i is not None]) + 50

            self._tipos_estados[TIPOESTADO.FINAL] = TipoEstado(TIPOESTADO.FINAL,
                                                               recompensa_estado_final,
                                                               "Final",
                                                               "F",
                                                               "#2F4055")

    def _inicializar_estados(self, default=TIPOESTADO.NEUTRO):
        inicializar_estados_worker = threading.Thread(None,
                                                      self._inicializar_estados_worker,
                                                      "GWInicializarEstadosWorker",
                                                      (default,),
                                                      None,
                                                      None)
        inicializar_estados_worker.start()
        inicializar_estados_worker.join(0.05)
        logging.debug(inicializar_estados_worker)

    def _inicializar_estados_worker(self, default=TIPOESTADO.NEUTRO):
        u"""
        Crea la matriz de estados con un tipo de estado predeterminado.
        """
        # Tipo de estado con el que se inicializará cada estado
        default_tipo = self._tipos_estados[default]

        self._estados = numpy.empty((self.alto, self.ancho), Estado)
        self._coordenadas = []
        # Crear una lista de listas
        for i in xrange(1, self._alto + 1):
            fila = numpy.empty((1, self.ancho), Estado)
            for j in xrange(1, self._ancho + 1):
                fila[0][j - 1] = Estado(i, j, default_tipo)
                self._coordenadas.append((i, j))
            self._estados[i - 1] = fila

    def get_matriz_r(self):
        u"""
        Crea y devuelve la matriz R de recompensa en en función de la ubicación de los estados
        y sus vecinos. Representa las transiciones posibles.
        """
        # Verificar si hay tipos de vecinos a excluir de la matriz R
        if self._excluir_tipos_vecinos is None:
            self._excluir_tipos_vecinos = []

        matriz_r = numpy.empty((self.alto, self.ancho), object)
        # Crear una lista de listas
        for i in xrange(1, self._alto + 1):
            fila = []
            for j in xrange(1, self._ancho + 1):
                # Obtener estado actual y su ID de tipo
                estado = self.get_estado(i, j)
                estado_ide = estado.tipo.ide
                # Obtener los estados vecinos del estado actual (i, j)
                vecinos = self.get_vecinos_estado(i, j)
                # Agregar vecinos y su recompensa al estado
                # excluyendo los prohibidos
                recomp_and_vec = {}

                for vecino in vecinos:
                    if vecino.tipo.ide not in self._excluir_tipos_vecinos:
                        recomp_and_vec[(vecino.fila, vecino.columna)] = vecino.tipo.recompensa

                fila.append((estado_ide, recomp_and_vec))
            matriz_r[i - 1] = fila
        return matriz_r

    def get_estado(self, x, y):
        u"""
        Devuelve un estado dadas sus coordenadas.

        :param x: Fila del estado
        :param y: Columna del estado
        """
        return self._estados[x - 1][y - 1]

    def set_estado(self, x, y, estado):
        u"""
        Asigna un estado en una posición X,Y dada.

        :param x: Fila de destino
        :param y: Columna de destino
        :param estado: Estado a asignar
        """
        if isinstance(estado, Estado):
            self._estados[x - 1][y - 1] = estado
        else:
            raise TypeError

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

    def get_tipos_vecinos_excluidos(self):
        return self._excluir_tipos_vecinos

    def set_tipos_vecinos_excluidos(self, valor):
        self._excluir_tipos_vecinos = valor

    def get_coordenadas(self):
        return self._coordenadas

    def get_vecinos_estado(self, x, y):
        u"""
        Devuelve los estados adyacentes en función de un estado dado.
        Fuente: http://stackoverflow.com/questions/2373306/pythonic-and-efficient-way-of-finding-adjacent-cells-in-grid

        :param x: Fila del estado
        :param y: Columna del estado
        """
        vecinos = []
        for fila, columna in ((x + i, y + j)
                              for i in (-1, 0, 1) for j in (-1, 0, 1)
                              if i != 0 or j != 0):
            if (fila, columna) in self._coordenadas:
                vecinos.append(self.get_estado(fila, columna))
        return numpy.array(vecinos, object)

    def matriz_estados_to_string(self):
        u"""
        Devuelve un string representando los estados en una estructura tabular (matriz)
        """
        return "\n".join(["| {0} |".format(" | ".join(j))
                          for j in [[i.tipo.letra for i in f]
                                    for f in self._estados]])

    # Propiedades (atributos) de la clase
    ancho = property(get_ancho, set_ancho, None, "Ancho del GridWorld")
    alto = property(get_alto, set_alto, None, "Alto del GridWorld")
    matriz_r = property(get_matriz_r, None, None, "Matriz R del GridWorld")
    estados = property(get_estados, set_estados, None, "Estados del GridWorld")
    tipos_estados = property(get_tipos_estados, set_tipos_estados, None,
                             "Tipos de estados del GridWorld")
    tipos_vecinos_excluidos = property(get_tipos_vecinos_excluidos,
                                       set_tipos_vecinos_excluidos, None,
                                       "Tipos de vecinos excluidos al calcular los vecinos adyacentes")
    coordenadas = property(get_coordenadas, None, None, "Coordenadas")
