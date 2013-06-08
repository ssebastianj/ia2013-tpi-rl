#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import Queue
import logging
import matplotlib.pyplot as plt
import threading


# ============================================================================
# GraphEpsExitososWorker
# ============================================================================
class GraphEpsExitososWorker(threading.Thread):
    u"""
    Worker encargado de graficar los Episodios Exitosos.
    """
    def __init__(self, inp_queue):
        super(GraphEpsExitososWorker, self).__init__()

        self._inp_queue = inp_queue
        self.setName('GraphEpsExitososWorker')
        self.alive = threading.Event()
        self.alive.set()

    def run(self):
        u"""
        Reimplementa el método 'run' de la clase padre. Ejecuta el código
        principal.
        """
        self._do_on_start()

        input_data = self.procesar_entrada()

        try:
            run_values = input_data[0]
            logging.debug(run_values)
            gamma = run_values[0]
            id_tecnica, parametro, paso_decrem, interv_decrem = run_values[1]
            cant_episodios = run_values[2]
            limitar_nro_iter, cant_max_iter = run_values[3]
            init_value = run_values[4]

            xy_values = input_data[1]
            x_values = [pair[0][0] for pair in xy_values]
            y_values = [pair[0][1] for pair in xy_values]

            figure = plt.gcf()
            figure.canvas.set_window_title(u"Definir título de la ventana")

            plt.plot(x_values, y_values)
            plt.grid(True)
            plt.title(u"Definir título del gráfico")
            plt.xlabel(u"Episodios")
            plt.ylabel(u"%")

            str_gamma = r"$\gamma={0}$".format(gamma)

            if id_tecnica == 0:
                str_tecnica = "Greedy"
                str_parametro = ""
            elif id_tecnica == 1:
                str_tecnica = r"$\epsilon$-Greedy"
                str_parametro = r"$\epsilon={0}$".format(parametro)
            elif id_tecnica == 2:
                str_tecnica = "Softmax"
                str_parametro = r"$\tau={0}$".format(parametro)
            elif id_tecnica == 3:
                str_tecnica = "Aleatorio"
                str_parametro = ""
            else:
                pass

            if limitar_nro_iter:
                str_limit_iter = "Limitar a {0} iteraciones".format(cant_max_iter)
            else:
                str_limit_iter = ""

            logging.debug(str_limit_iter)

            # Mostrar parámetros de entrenamiento
            plt.text(plt.axis()[0] + 5,
                     plt.axis()[1] - 10,
                     "{0}\n{1} ({2})\n".format(str_gamma,
                                               str_tecnica,
                                               str_parametro
                                              ),
                     fontdict={'fontsize': 12}
                     )

            # Renderizar gráfico
            plt.show()
        except TypeError:
            pass
        except ValueError:
            pass

        self._on_end()

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        pass

    def procesar_entrada(self):
        u"""
        Recibe e inicializa los datos de entradas que se utilizarán en el
        entrenamiento.
        """
        # Obtener matriz R y matriz Q
        try:
            input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None
        return input_data

    def join(self, timeout=None):
        u"""Reimplementa el método 'join' de la clase padre.

        :param timeout: Tiempo de espera.
        """
        self.alive.clear()
        # threading.Thread.join(self, timeout)
        super(GraphEpsExitososWorker, self).join(timeout)


# ============================================================================
# GraphRecompPromedioWorker
# ============================================================================
class GraphRecompPromedioWorker(threading.Thread):
    u"""
    Worker encargado de graficar las Recompensas Promedio.
    """
    def __init__(self, inp_queue):
        super(GraphRecompPromedioWorker, self).__init__()

        self._inp_queue = inp_queue
        self.setName('GraphRecompPromedioWorker')
        self.alive = threading.Event()
        self.alive.set()
        self.input_data = None

    def run(self):
        u"""
        Reimplementa el método 'run' de la clase padre. Ejecuta el código
        principal.
        """
        self._do_on_start()

        self.procesar_entrada()

        plt.plot(range(1000), range(1000))
        plt.show()

        self._on_end()

    def _do_on_start(self):
        u"""
        Ejecuta tareas al comenzar el thread.
        """
        pass

    def _on_end(self):
        u"""
        Ejecuta tareas al finalizar el thread.
        """
        pass

    def procesar_entrada(self):
        u"""
        Recibe e inicializa los datos de entradas que se utilizarán en el
        entrenamiento.
        """
        # Obtener matriz R y matriz Q
        try:
            input_data = self._inp_queue.get(True, 0.05)
        except Queue.Empty:
            return None
        return input_data

    def join(self, timeout=None):
        u"""Reimplementa el método 'join' de la clase padre.

        :param timeout: Tiempo de espera.
        """
        self.alive.clear()
        # threading.Thread.join(self, timeout)
        super(GraphRecompPromedioWorker, self).join(timeout)
