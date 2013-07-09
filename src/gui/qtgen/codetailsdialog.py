# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\codetailsdialog.ui'
#
# Created: Tue Jul 09 15:27:46 2013
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

class Ui_CODetailsDialog(object):
    def setupUi(self, CODetailsDialog):
        CODetailsDialog.setObjectName(_fromUtf8("CODetailsDialog"))
        CODetailsDialog.setWindowModality(QtCore.Qt.WindowModal)
        CODetailsDialog.resize(345, 490)
        self.gridLayout_2 = QtGui.QGridLayout(CODetailsDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(CODetailsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.tblSecuenciaEstados = QtGui.QTableWidget(CODetailsDialog)
        self.tblSecuenciaEstados.setObjectName(_fromUtf8("tblSecuenciaEstados"))
        self.tblSecuenciaEstados.setColumnCount(3)
        self.tblSecuenciaEstados.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblSecuenciaEstados.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblSecuenciaEstados.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblSecuenciaEstados.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tblSecuenciaEstados)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 2)
        self.btnCerrar = QtGui.QPushButton(CODetailsDialog)
        self.btnCerrar.setDefault(True)
        self.btnCerrar.setObjectName(_fromUtf8("btnCerrar"))
        self.gridLayout_2.addWidget(self.btnCerrar, 4, 1, 1, 1)
        self.line = QtGui.QFrame(CODetailsDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(CODetailsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(125, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblCOCantidadEstados = QtGui.QLabel(CODetailsDialog)
        self.lblCOCantidadEstados.setObjectName(_fromUtf8("lblCOCantidadEstados"))
        self.gridLayout.addWidget(self.lblCOCantidadEstados, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(CODetailsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(125, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lblCOSumValQ = QtGui.QLabel(CODetailsDialog)
        self.lblCOSumValQ.setObjectName(_fromUtf8("lblCOSumValQ"))
        self.gridLayout.addWidget(self.lblCOSumValQ, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)

        self.retranslateUi(CODetailsDialog)
        QtCore.QObject.connect(self.btnCerrar, QtCore.SIGNAL(_fromUtf8("clicked()")), CODetailsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(CODetailsDialog)

    def retranslateUi(self, CODetailsDialog):
        CODetailsDialog.setWindowTitle(_translate("CODetailsDialog", "Detalles de camino óptimo", None))
        self.label_3.setText(_translate("CODetailsDialog", "Secuencia de estados:", None))
        item = self.tblSecuenciaEstados.horizontalHeaderItem(0)
        item.setText(_translate("CODetailsDialog", "Estado", None))
        item = self.tblSecuenciaEstados.horizontalHeaderItem(1)
        item.setText(_translate("CODetailsDialog", "Coordenadas", None))
        item = self.tblSecuenciaEstados.horizontalHeaderItem(2)
        item.setText(_translate("CODetailsDialog", "Valor Q", None))
        self.btnCerrar.setText(_translate("CODetailsDialog", "&Cerrar", None))
        self.label.setText(_translate("CODetailsDialog", "Cantidad de estados:", None))
        self.lblCOCantidadEstados.setText(_translate("CODetailsDialog", "-", None))
        self.label_2.setText(_translate("CODetailsDialog", "Sumatoria de valores Q:", None))
        self.lblCOSumValQ.setText(_translate("CODetailsDialog", "-", None))

