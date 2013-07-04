# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\aboutdialog.ui'
#
# Created: Wed Jul 03 14:45:15 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(535, 292)
        AboutDialog.setMinimumSize(QtCore.QSize(535, 292))
        AboutDialog.setMaximumSize(QtCore.QSize(535, 292))
        AboutDialog.setModal(True)
        self.label = QtGui.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(184, 8, 321, 33))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.lblAppVersion = QtGui.QLabel(AboutDialog)
        self.lblAppVersion.setGeometry(QtCore.QRect(328, 104, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblAppVersion.setFont(font)
        self.lblAppVersion.setObjectName(_fromUtf8("lblAppVersion"))
        self.label_4 = QtGui.QLabel(AboutDialog)
        self.label_4.setGeometry(QtCore.QRect(16, 16, 129, 121))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(":/logos/LogoUTN.jpeg")))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(AboutDialog)
        self.label_5.setGeometry(QtCore.QRect(240, 40, 233, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cambria"))
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.groupBox = QtGui.QGroupBox(AboutDialog)
        self.groupBox.setGeometry(QtCore.QRect(16, 152, 513, 105))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(AboutDialog)
        self.pushButton.setGeometry(QtCore.QRect(448, 264, 75, 23))
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label_8 = QtGui.QLabel(AboutDialog)
        self.label_8.setGeometry(QtCore.QRect(208, 72, 313, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Acerca de Grupo Nº 1", None))
        self.label.setText(_translate("AboutDialog", "Inteligencia Artificial 2013", None))
        self.lblAppVersion.setText(_translate("AboutDialog", "Versión 1.0", None))
        self.label_5.setText(_translate("AboutDialog", " Aprendizaje por Refuerzo", None))
        self.groupBox.setTitle(_translate("AboutDialog", "Grupo Nº 1", None))
        self.label_2.setText(_translate("AboutDialog", "Fabián A. Levin", None))
        self.label_6.setText(_translate("AboutDialog", "Lucía B. Vallejos", None))
        self.label_7.setText(_translate("AboutDialog", "Sebastián J. Seba", None))
        self.pushButton.setText(_translate("AboutDialog", "&Cerrar", None))
        self.label_8.setText(_translate("AboutDialog", "Universidad Tecnológica Nacional - Facultad Regional Resistencia", None))

import recursos_rc
