# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\mainwindow.ui'
#
# Created: Thu Mar 28 23:05:00 2013
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(811, 585)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(304, 8, 337, 113))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(16, 24, 122, 22))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        self.GridWorld = QtGui.QTableWidget(self.centralWidget)
        self.GridWorld.setGeometry(QtCore.QRect(16, 8, 256, 192))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GridWorld.sizePolicy().hasHeightForWidth())
        self.GridWorld.setSizePolicy(sizePolicy)
        self.GridWorld.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.GridWorld.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GridWorld.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GridWorld.setAutoScroll(False)
        self.GridWorld.setTabKeyNavigation(False)
        self.GridWorld.setProperty("showDropIndicator", False)
        self.GridWorld.setDragDropOverwriteMode(False)
        self.GridWorld.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.GridWorld.setCornerButtonEnabled(False)
        self.GridWorld.setObjectName(_fromUtf8("GridWorld"))
        self.GridWorld.setColumnCount(0)
        self.GridWorld.setRowCount(0)
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(304, 256, 369, 97))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setGeometry(QtCore.QRect(304, 136, 369, 97))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 811, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menu_Archivo = QtGui.QMenu(self.menuBar)
        self.menu_Archivo.setObjectName(_fromUtf8("menu_Archivo"))
        self.menuEdici_n = QtGui.QMenu(self.menuBar)
        self.menuEdici_n.setObjectName(_fromUtf8("menuEdici_n"))
        self.menuAy_uda = QtGui.QMenu(self.menuBar)
        self.menuAy_uda.setObjectName(_fromUtf8("menuAy_uda"))
        self.menu_Tablero = QtGui.QMenu(self.menuBar)
        self.menu_Tablero.setObjectName(_fromUtf8("menu_Tablero"))
        self.menu_Operaciones = QtGui.QMenu(self.menuBar)
        self.menu_Operaciones.setObjectName(_fromUtf8("menu_Operaciones"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionAppSalir = QtGui.QAction(MainWindow)
        self.actionAppSalir.setObjectName(_fromUtf8("actionAppSalir"))
        self.actionAcercaDe = QtGui.QAction(MainWindow)
        self.actionAcercaDe.setObjectName(_fromUtf8("actionAcercaDe"))
        self.menu_Archivo.addAction(self.actionAppSalir)
        self.menuAy_uda.addAction(self.actionAcercaDe)
        self.menuBar.addAction(self.menu_Archivo.menuAction())
        self.menuBar.addAction(self.menuEdici_n.menuAction())
        self.menuBar.addAction(self.menu_Tablero.menuAction())
        self.menuBar.addAction(self.menu_Operaciones.menuAction())
        self.menuBar.addAction(self.menuAy_uda.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Grid World", None))
        self.label.setText(_translate("MainWindow", "Dimensión:", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "6 x 6", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "7 x 7", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "8 x 8", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "9 x 9", None))
        self.comboBox.setItemText(4, _translate("MainWindow", "10 x 10", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Operaciones", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Q-Learning", None))
        self.menu_Archivo.setTitle(_translate("MainWindow", "&Archivo", None))
        self.menuEdici_n.setTitle(_translate("MainWindow", "&Edición", None))
        self.menuAy_uda.setTitle(_translate("MainWindow", "Ay&uda", None))
        self.menu_Tablero.setTitle(_translate("MainWindow", "&Grid World", None))
        self.menu_Operaciones.setTitle(_translate("MainWindow", "&Operaciones", None))
        self.actionAppSalir.setText(_translate("MainWindow", "Salir", None))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de...", None))

