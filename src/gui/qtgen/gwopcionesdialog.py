# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\gwopcionesdialog.ui'
#
# Created: Thu May 09 21:26:43 2013
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
        GWOpcionesDialog.resize(261, 137)
        GWOpcionesDialog.setModal(True)
        self.groupBox = QtGui.QGroupBox(GWOpcionesDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 111, 55))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.sbGWEstadoSize = QtGui.QSpinBox(self.groupBox)
        self.sbGWEstadoSize.setMinimum(20)
        self.sbGWEstadoSize.setMaximum(100)
        self.sbGWEstadoSize.setProperty("value", 40)
        self.sbGWEstadoSize.setObjectName(_fromUtf8("sbGWEstadoSize"))
        self.horizontalLayout.addWidget(self.sbGWEstadoSize)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(GWOpcionesDialog)
        self.pushButton.setGeometry(QtCore.QRect(176, 104, 75, 23))
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label.setBuddy(self.sbGWEstadoSize)

        self.retranslateUi(GWOpcionesDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), GWOpcionesDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(GWOpcionesDialog)
        GWOpcionesDialog.setTabOrder(self.pushButton, self.sbGWEstadoSize)

    def retranslateUi(self, GWOpcionesDialog):
        GWOpcionesDialog.setWindowTitle(_translate("GWOpcionesDialog", "Configurar Grid World", None))
        self.groupBox.setTitle(_translate("GWOpcionesDialog", "Estado", None))
        self.label.setText(_translate("GWOpcionesDialog", "Tamaño:", None))
        self.pushButton.setText(_translate("GWOpcionesDialog", "&Aceptar", None))

