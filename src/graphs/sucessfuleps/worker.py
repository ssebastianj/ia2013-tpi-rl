#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import csv
import decimal
import matplotlib.pyplot as plt
import numpy

from PyQt4 import QtCore


class GraphSucessfulEpisodesWorker(QtCore.QObject):
    def __init__(self, input_data):
        super(GraphSucessfulEpisodesWorker, self).__init__()

        self.input_data = input_data
        self._init_plt()

    def _init_plt(self):
        decimal.getcontext().prec = 6
        run_values = self.input_data[0]
        gamma = run_values[0]
        id_tecnica, parametro, paso_decrem, interv_decrem = run_values[1]
        cant_episodios = run_values[2]
        limitar_nro_iter, cant_max_iter = run_values[3]
        init_value = run_values[4]

        try:
            xy_values = self.input_data[1]

            self.x_values = [pair[0][0] for pair in xy_values
                             if not numpy.equal(pair, None)]
            self.y_values = [pair[0][1] for pair in xy_values
                             if not numpy.equal(pair, None)]

            figure = plt.gcf()
            figure.canvas.set_window_title(u"Porcentaje de episodios finalizados")

            plt.plot(self.x_values, self.y_values)
            plt.grid(True)
            plt.title(u"Porcentaje de episodios finalizados")
            plt.xlabel(u"Episodios")
            plt.ylabel(u"% episodios finalizados")

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

            # Mostrar parámetros de entrenamiento
            plt.text(plt.axis()[0] + 5,
                     plt.axis()[1] - 10,
                     "{0}\n{1} ({2})\n".format(str_gamma,
                                               str_tecnica,
                                               str_parametro
                                              ),
                     fontdict={'fontsize': 12}
                     )

        except TypeError:
            raise TypeError
        except ValueError:
            raise ValueError

    def mostrar_figura(self):
        # Renderizar gráfico y mostrar ventana
        plt.show()
        # Liberar memoria
        plt.close()

    def guardar_dibujo(self, filename):
        # Renderizar gráfico y guardar a archivo
        plt.savefig(filename)
        # Liberar memoria
        plt.close()


    def exportar_info(self, filepath, append=False):
        mode = 'ab' if append else 'wb'

        with open(filepath, mode) as csvf:
            csv_writer = csv.writer(csvf, dialect='excel', delimiter=';')

            csv_writer.writerow(['Episodios', 'Episodios Exitosos'])
            for x, y in zip(self.x_values, self.y_values):
                x = "{0}".format(decimal.Decimal(x))
                y = "{0}".format(decimal.Decimal(y))
                y = y.replace('.', ',')
                csv_writer.writerow([x, y])

            csv_writer.writerow([])
