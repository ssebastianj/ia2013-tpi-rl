# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\gwgenrndestadosdialog.ui'
#
# Created: Fri Jun 14 23:03:42 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GWGenRndEstadosDialog(object):
    def setupUi(self, GWGenRndEstadosDialog):
        GWGenRndEstadosDialog.setObjectName(_fromUtf8("GWGenRndEstadosDialog"))
        GWGenRndEstadosDialog.resize(400, 300)
        GWGenRndEstadosDialog.setModal(True)

        self.retranslateUi(GWGenRndEstadosDialog)
        QtCore.QMetaObject.connectSlotsByName(GWGenRndEstadosDialog)

    def retranslateUi(self, GWGenRndEstadosDialog):
        GWGenRndEstadosDialog.setWindowTitle(_translate("GWGenRndEstadosDialog", "Generar estados aleatorios", None))

