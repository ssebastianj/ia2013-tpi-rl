#!/usr/bin/env python


from PyQt4 import QtCore, QtGui
from gui.qtgen.gwgenrndestadosdialog import Ui_GWGenRndEstadosDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GWGenRndEstadosDialog(QtGui.QDialog):
    """
    Clase de diálogo 'Opciones' heredada de QDialog.
    """
    def __init__(self, parent=None):
        """
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super().__init__(parent)

        self.GWGenRndEstadosD = Ui_GWGenRndEstadosDialog()
        self.GWGenRndEstadosD.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)

        self.initialize_dialog()

    def initialize_dialog(self):
        """
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        pass
