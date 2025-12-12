#!/usr/bin/env python


from PyQt4 import QtCore, QtGui
from gui.qtgen.codetailsdialog import Ui_CODetailsDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class ShowCODetailsDialog(QtGui.QDialog):
    """
    Clase de diálogo 'Opciones' heredada de QDialog.
    """

    def __init__(self, caminooptimo, valoresq, dimgw, tblgridref=None, parent=None):
        """
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super().__init__(parent)

        self.ShowCODetailsD = Ui_CODetailsDialog()
        self.ShowCODetailsD.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
        )

        self.camino_optimo = caminooptimo
        self.valores_q = valoresq
        self.dim_gw = dimgw

        self.initialize_dialog()

    def initialize_dialog(self):
        """
        Configura y establece el estado de los widgets en el cuadro de diálogo.
        """
        self._set_dialog_signals()

        # Cachear acceso a métodos y atributos
        camino_optimo = self.camino_optimo
        valores_q = self.valores_q
        tblSecuenciaEstados = self.ShowCODetailsD.tblSecuenciaEstados
        alto = self.dim_gw[1]
        item_text_align = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter
        item_flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        long_camino_optimo = len(camino_optimo)
        tblSecuenciaEstados.setRowCount(long_camino_optimo)

        self.ShowCODetailsD.lblCOCantidadEstados.setText(str(long_camino_optimo))
        self.ShowCODetailsD.lblCOSumValQ.setText(_tr("{:.4f}".format(sum(valores_q))))

        for idx, (x, y) in enumerate(camino_optimo):
            nro_estado = ((x - 1) * alto) + y

            if idx == 0:
                item_valor_q = QtGui.QTableWidgetItem(_tr("-"))
            else:
                valor_q = valores_q[idx - 1]
                item_valor_q = QtGui.QTableWidgetItem(_tr("{:.2f}".format(valor_q)))

            item_nro_estado = QtGui.QTableWidgetItem(_tr("E{}".format(nro_estado)))
            item_coord = QtGui.QTableWidgetItem(
                _tr("Fila: {} Columna: {}".format(x, y))
            )

            item_valor_q.setTextAlignment(item_text_align)
            item_valor_q.setFlags(item_flags)
            item_coord.setTextAlignment(item_text_align)
            item_coord.setFlags(item_flags)
            item_nro_estado.setTextAlignment(item_text_align)
            item_nro_estado.setFlags(item_flags)

            tblSecuenciaEstados.setItem(idx, 0, item_nro_estado)
            tblSecuenciaEstados.setItem(idx, 1, item_coord)
            tblSecuenciaEstados.setItem(idx, 2, item_valor_q)

        tblSecuenciaEstados.resizeColumnsToContents()

    def _set_dialog_signals(self):
        pass

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()
