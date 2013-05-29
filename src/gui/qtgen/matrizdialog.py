# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\matrizdialog.ui'
#
# Created: Wed May 29 13:39:57 2013
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

class Ui_MatrizDialog(object):
    def setupUi(self, MatrizDialog):
        MatrizDialog.setObjectName(_fromUtf8("MatrizDialog"))
        MatrizDialog.resize(430, 392)
        MatrizDialog.setWindowTitle(_fromUtf8(""))
        MatrizDialog.setSizeGripEnabled(True)
        MatrizDialog.setModal(True)
        self.gridLayout_2 = QtGui.QGridLayout(MatrizDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblMatriz = QtGui.QTableWidget(MatrizDialog)
        self.tblMatriz.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tblMatriz.setLocale(QtCore.QLocale(QtCore.QLocale.Spanish, QtCore.QLocale.Argentina))
        self.tblMatriz.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tblMatriz.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tblMatriz.setAutoScroll(False)
        self.tblMatriz.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblMatriz.setTabKeyNavigation(False)
        self.tblMatriz.setProperty("showDropIndicator", False)
        self.tblMatriz.setDragDropOverwriteMode(False)
        self.tblMatriz.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tblMatriz.setCornerButtonEnabled(False)
        self.tblMatriz.setObjectName(_fromUtf8("tblMatriz"))
        self.tblMatriz.setColumnCount(0)
        self.tblMatriz.setRowCount(0)
        self.gridLayout_2.addWidget(self.tblMatriz, 1, 1, 1, 1)
        self.label = QtGui.QLabel(MatrizDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(MatrizDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnCerrarDialogo = QtGui.QPushButton(MatrizDialog)
        self.btnCerrarDialogo.setDefault(True)
        self.btnCerrarDialogo.setObjectName(_fromUtf8("btnCerrarDialogo"))
        self.gridLayout.addWidget(self.btnCerrarDialogo, 1, 1, 1, 1)
        self.line = QtGui.QFrame(MatrizDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 2)

        self.retranslateUi(MatrizDialog)
        QtCore.QObject.connect(self.btnCerrarDialogo, QtCore.SIGNAL(_fromUtf8("clicked()")), MatrizDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(MatrizDialog)

    def retranslateUi(self, MatrizDialog):
        self.label.setText(_translate("MatrizDialog", "Acciones", None))
        self.label_2.setText(_translate("MatrizDialog", "Estados", None))
        self.btnCerrarDialogo.setText(_translate("MatrizDialog", "&Cerrar", None))

