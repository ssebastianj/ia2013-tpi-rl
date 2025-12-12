#!/usr/bin/env python


import random
from core.tecnicas.tecnica import QLTecnica


class Aleatorio(QLTecnica):
    """Técnica Aleatorio"""
    def __init__(self, parametro=None, paso_decremento=0, intervalo_decremento=0):
        """
        Inicializador

        :param comienzo_rango: Valor inicial del rango de generación.
        :param fin_rango: Valor final del rango de generación.
        """
        super().__init__()

    def obtener_accion(self, vecinos):
        """
        Dado un conjunto de vecinos selecciona acorde uno de ellos.

        :param vecinos: Diccionario conteniendo los vecinos de un estado.
        """
        return random.choice(list(vecinos.keys()))

    def decrementar_parametro(self):
        """
        Decrementa el parámetro general en un valor dado.
        """
        pass
