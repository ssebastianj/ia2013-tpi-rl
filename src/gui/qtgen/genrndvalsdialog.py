# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\genrndvalsdialog.ui'
#
# Created: Mon Apr 22 17:45:39 2013
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

class Ui_GenRndValsDialog(object):
    def setupUi(self, GenRndValsDialog):
        GenRndValsDialog.setObjectName(_fromUtf8("GenRndValsDialog"))
        GenRndValsDialog.setWindowModality(QtCore.Qt.WindowModal)
        GenRndValsDialog.resize(323, 203)
        GenRndValsDialog.setMinimumSize(QtCore.QSize(323, 203))
        GenRndValsDialog.setMaximumSize(QtCore.QSize(323, 203))
        self.gridLayout_4 = QtGui.QGridLayout(GenRndValsDialog)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox = QtGui.QGroupBox(GenRndValsDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkDimensionAleatoria = QtGui.QCheckBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkDimensionAleatoria.sizePolicy().hasHeightForWidth())
        self.chkDimensionAleatoria.setSizePolicy(sizePolicy)
        self.chkDimensionAleatoria.setObjectName(_fromUtf8("chkDimensionAleatoria"))
        self.gridLayout.addWidget(self.chkDimensionAleatoria, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.optGenerarEstados = QtGui.QRadioButton(self.groupBox)
        self.optGenerarEstados.setObjectName(_fromUtf8("optGenerarEstados"))
        self.gridLayout.addWidget(self.optGenerarEstados, 0, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.chkTecnicaAleatoria = QtGui.QCheckBox(self.groupBox)
        self.chkTecnicaAleatoria.setObjectName(_fromUtf8("chkTecnicaAleatoria"))
        self.gridLayout_2.addWidget(self.chkTecnicaAleatoria, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.optGenerarValoresParam = QtGui.QRadioButton(self.groupBox)
        self.optGenerarValoresParam.setObjectName(_fromUtf8("optGenerarValoresParam"))
        self.gridLayout_2.addWidget(self.optGenerarValoresParam, 0, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.optGenerarTodo = QtGui.QRadioButton(self.groupBox)
        self.optGenerarTodo.setObjectName(_fromUtf8("optGenerarTodo"))
        self.gridLayout_3.addWidget(self.optGenerarTodo, 2, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnGenRndVals = QtGui.QPushButton(GenRndValsDialog)
        self.btnGenRndVals.setMinimumSize(QtCore.QSize(85, 0))
        self.btnGenRndVals.setDefault(True)
        self.btnGenRndVals.setObjectName(_fromUtf8("btnGenRndVals"))
        self.horizontalLayout.addWidget(self.btnGenRndVals)
        self.btnCancelGenRndVals = QtGui.QPushButton(GenRndValsDialog)
        self.btnCancelGenRndVals.setObjectName(_fromUtf8("btnCancelGenRndVals"))
        self.horizontalLayout.addWidget(self.btnCancelGenRndVals)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(GenRndValsDialog)
        QtCore.QObject.connect(self.btnGenRndVals, QtCore.SIGNAL(_fromUtf8("clicked()")), GenRndValsDialog.accept)
        QtCore.QObject.connect(self.btnCancelGenRndVals, QtCore.SIGNAL(_fromUtf8("clicked()")), GenRndValsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GenRndValsDialog)
        GenRndValsDialog.setTabOrder(self.optGenerarEstados, self.chkDimensionAleatoria)
        GenRndValsDialog.setTabOrder(self.chkDimensionAleatoria, self.optGenerarValoresParam)
        GenRndValsDialog.setTabOrder(self.optGenerarValoresParam, self.chkTecnicaAleatoria)
        GenRndValsDialog.setTabOrder(self.chkTecnicaAleatoria, self.optGenerarTodo)
        GenRndValsDialog.setTabOrder(self.optGenerarTodo, self.btnGenRndVals)
        GenRndValsDialog.setTabOrder(self.btnGenRndVals, self.btnCancelGenRndVals)

    def retranslateUi(self, GenRndValsDialog):
        GenRndValsDialog.setWindowTitle(_translate("GenRndValsDialog", "Generar valores aleatorios", None))
        self.groupBox.setTitle(_translate("GenRndValsDialog", "Generar...", None))
        self.chkDimensionAleatoria.setText(_translate("GenRndValsDialog", "Dimensión aleatoria", None))
        self.optGenerarEstados.setText(_translate("GenRndValsDialog", "Estados aleatorios de diferente tipo", None))
        self.chkTecnicaAleatoria.setText(_translate("GenRndValsDialog", "Técnica aleatoria", None))
        self.optGenerarValoresParam.setText(_translate("GenRndValsDialog", "Valores de los parámetros", None))
        self.optGenerarTodo.setText(_translate("GenRndValsDialog", "Ambos", None))
        self.btnGenRndVals.setText(_translate("GenRndValsDialog", "&Generar", None))
        self.btnCancelGenRndVals.setText(_translate("GenRndValsDialog", "Cancelar", None))

