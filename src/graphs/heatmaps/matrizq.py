#!/usr/bin/env python


import numpy
import matplotlib.pyplot as plt


class ShowMatrizQHeatMap:
    """
    Clase dedicada a generar y mostrar un heatmap de la Matriz Q.
    """
    def __init__(self, matrizq, parent=None):
        """
        Inicializador de la clase.

        :param matrizq: Matriz Q a representar.
        :param parent: Ventana padre.
        """
        super().__init__()
        self.matriz = matrizq

    def show_heatmap(self, interpolation=None):
        """
        Generar y mostrar heatmap.

        :param interpolation: Parámetro válido de interpolación del heatmap.
        """
        # Dimensiones de la matriz
        ancho_mat, alto_mat = self.matriz.shape

        # Dimensiones del GridWorld
        alto_gw = int(alto_mat ** 0.5)
        ancho_gw = int(ancho_mat ** 0.5)
        dim_gw = ancho_gw * alto_gw

        suma_acciones = numpy.round(numpy.nansum(self.matriz, 0))

        x = numpy.empty((dim_gw,), numpy.int)
        y = numpy.empty((dim_gw,), numpy.int)

        for i in xrange(dim_gw):
            fila = int(i / alto_gw)
            columna = i - (fila * ancho_gw)
            x[i] = fila
            y[i] = columna

        heatmap, xedges, yedges = numpy.histogram2d(x, y,
                                                    bins=ancho_gw,
                                                    weights=suma_acciones)

        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        figure = plt.gcf()
        figure.canvas.set_window_title("Heatmap de Matriz Q")

        plt.grid(True)
        plt.clf()
        plt.imshow(heatmap, extent=extent, interpolation=interpolation)
        cb = plt.colorbar()
        cb.set_label("Valor Q")
        plt.show()
        plt.close()
