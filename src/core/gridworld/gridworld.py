#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import numpy
import random
import threading

from core.estado.estado import Estado, TIPOESTADO


class GridWorld(object):
    """Clase GridWorld"""
    def __init__(self, ancho, alto, tipos_estados, estados=None,
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
        self._logger = logging.getLogger()

        self._ancho = ancho
        self._alto = alto
        self._tipos_estados = tipos_estados
        self._estados = estados
        self._coordenadas = None
        self._excluir_tipos_vecinos = excluir_tipos_vecinos
        self._estado_final = None

        self._inicializar_estados()

    def _inicializar_estados(self, default=TIPOESTADO.NEUTRO):
        u"""
        Inicializa los estados del GridWorld a un tipo de estado predeterminado.

        :param default: Tipo de estado predeterminado para cada Estado del GridWorld.
        """
        if isinstance(self._tipos_estados, dict):
            self._estado_final = None

            inicializar_estados_worker = threading.Thread(None,
                                                          self._inicializar_estados_worker,
                                                          "GWInicializarEstadosWorker",
                                                          (default,),
                                                          None,
                                                          None)
            inicializar_estados_worker.start()
            inicializar_estados_worker.join(0.05)
            self._logger.debug(inicializar_estados_worker)
        else:
            return None

    def _inicializar_estados_worker(self, default=TIPOESTADO.NEUTRO):
        u"""
        Crea la matriz de estados con un tipo de estado predeterminado.
        """
        if self._estados is None:
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
        else:
            self._coordenadas = []
            for i in xrange(1, self._alto + 1):
                for j in xrange(1, self._ancho + 1):
                    self._coordenadas.append((i, j))

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

    def set_tipos_estados(self, tipos_estados):
        if isinstance(tipos_estados, dict):
            self._tipos_estados = tipos_estados
            self.actualizar_info_estados()

    def get_tipos_vecinos_excluidos(self):
        return self._excluir_tipos_vecinos

    def set_tipos_vecinos_excluidos(self, valor):
        if isinstance(valor, dict):
            self._excluir_tipos_vecinos = valor
        else:
            raise TypeError

    def get_coordenadas(self):
        return self._coordenadas

    def get_dimension(self):
        return (self._ancho, self._alto)

    def set_dimension(self, dimension):
        self._ancho, self._alto = dimension

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

    def __len__(self):
        return len(self._estados)

    def generar_estados_aleatorios(self, incluir_final=False):
        u"""
        Genera estados aleatorios en el GridWorld utilizando número pseudo-aleatorios.

        :param incluir_final: Boooleano que determina si se generará de manera aleatoria al Estado Final.
        """
        if isinstance(self._tipos_estados, dict):
            gen_estados_random_worker = threading.Thread(None,
                                                         self._generar_estados_aleatorios_worker,
                                                         "GWGenerarEstadosAleatoriosWorker",
                                                         (incluir_final,),
                                                         None,
                                                         None)
            gen_estados_random_worker.start()
            gen_estados_random_worker.join(0.05)
            self._logger.debug(gen_estados_random_worker)
            return self._estado_final
        else:
            return None

    def _generar_estados_aleatorios_worker(self, incluir_final=False):
        u"""
        Crea la matriz de estados tipos de estados aleatorios.
        """
        excluir_estados_random = [TIPOESTADO.AGENTE,
                                  TIPOESTADO.INICIAL,
                                  TIPOESTADO.FINAL]

        estado_final = None

        if self._estados is None:
            self._estados = numpy.empty((self.alto, self.ancho), Estado)
            self._coordenadas = []

            # Crear una lista de listas
            for i in xrange(1, self._alto + 1):
                fila = numpy.empty((1, self.ancho), Estado)
                for j in xrange(1, self._ancho + 1):
                    # Generar tipo de estado aleatorio
                    rnd_tipo = random.choice(self._tipos_estados.values())

                    # Generar hasta que no coincida con un tipo de estado prohibido
                    while rnd_tipo.ide in excluir_estados_random:
                        rnd_tipo = random.choice(self._tipos_estados.values())

                    fila[0][j - 1] = Estado(i, j, rnd_tipo)
                    self._coordenadas.append((i, j))
                self._estados[i - 1] = fila

                # Generar Estado Final aleatorio si es necesario
                if incluir_final:
                    coord_x = random.randint(1, self.ancho - 1)
                    coord_y = random.randint(1, self.alto - 1)
                    estado = self.get_estado(coord_x, coord_y)
                    estado.tipo = self._tipos_estados[TIPOESTADO.FINAL]
                    estado_final = estado
        else:
            for fila in self._estados:
                for estado in fila:
                    # Generar tipo de estado aleatorio
                    rnd_tipo = random.choice(self._tipos_estados.values())

                    # Generar hasta que no coincida con un tipo de estado prohibido
                    while rnd_tipo.ide in excluir_estados_random:
                        rnd_tipo = random.choice(self._tipos_estados.values())

                    estado.tipo = rnd_tipo

            # Generar Estado Final aleatorio si es necesario
            if incluir_final:
                coord_x = random.randint(1, self.ancho - 1)
                coord_y = random.randint(1, self.alto - 1)
                estado = self.get_estado(coord_x, coord_y)
                estado.tipo = self._tipos_estados[TIPOESTADO.FINAL]
                estado_final = estado

        # Guardar referencia al estado final generado
        self._estado_final = estado_final

    def actualizar_info_estados(self):
        u"""
        Actualiza la información de los Estados acerca del tipo de dato modificado.
        """
        if self._estados is not None:
            for fila in self._estados:
                for estado in fila:
                    estado.tipo = self._tipos_estados[estado.tipo.ide]

    def get_matriz_tipos_estados(self):
        if self._estados is not None:
            return [[j.tipo.ide for j in i] for i in self._estados]
        else:
            return None

    def from_matriz_tipos_estados(self, estados_num):
        # Crear una lista de listas
        ancho, alto = len(estados_num), len(estados_num[0])
        self.ancho = ancho
        self.alto = alto
        estados = numpy.empty((ancho, alto), Estado)

        for i in xrange(1, alto + 1):
            fila = numpy.empty((1, ancho), Estado)
            for j in xrange(1, ancho + 1):
                fila[0][j - 1] = Estado(i, j, self.tipos_estados[estados_num[i - 1][j - 1]])
                self.coordenadas.append((i, j))
            estados[i - 1] = fila
        self.estados = estados

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
    dimension = property(get_dimension, set_dimension, None, "Dimensión del GridWorld")
