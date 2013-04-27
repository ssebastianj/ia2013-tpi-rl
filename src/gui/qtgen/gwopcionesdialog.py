# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\gwopcionesdialog.ui'
#
# Created: Sat Apr 27 12:55:33 2013
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

class Ui_GWOpcionesDialog(object):
    def setupUi(self, GWOpcionesDialog):
        GWOpcionesDialog.setObjectName(_fromUtf8("GWOpcionesDialog"))
        GWOpcionesDialog.resize(400, 300)
        GWOpcionesDialog.setModal(True)

        self.retranslateUi(GWOpcionesDialog)
        QtCore.QMetaObject.connectSlotsByName(GWOpcionesDialog)

    def retranslateUi(self, GWOpcionesDialog):
        GWOpcionesDialog.setWindowTitle(_translate("GWOpcionesDialog", "Configurar Grid World", None))

