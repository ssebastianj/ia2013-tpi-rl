# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\mainwindow.ui'
#
# Created: Sat Mar 30 12:35:26 2013
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
        MainWindow.resize(653, 365)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.GridWorld = QtGui.QTableWidget(self.centralWidget)
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
        self.horizontalLayout_6.addWidget(self.GridWorld)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cbGWDimension = QtGui.QComboBox(self.groupBox)
        self.cbGWDimension.setObjectName(_fromUtf8("cbGWDimension"))
        self.horizontalLayout.addWidget(self.cbGWDimension)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.sbQLEpsilon = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLEpsilon.setObjectName(_fromUtf8("sbQLEpsilon"))
        self.horizontalLayout_5.addWidget(self.sbQLEpsilon)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.sbQLAlpha = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLAlpha.setObjectName(_fromUtf8("sbQLAlpha"))
        self.horizontalLayout_3.addWidget(self.sbQLAlpha)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.sbQLGamma = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLGamma.setObjectName(_fromUtf8("sbQLGamma"))
        self.horizontalLayout_4.addWidget(self.sbQLGamma)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cbQLTecnicas = QtGui.QComboBox(self.groupBox_3)
        self.cbQLTecnicas.setObjectName(_fromUtf8("cbQLTecnicas"))
        self.horizontalLayout_2.addWidget(self.cbQLTecnicas)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 653, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuArchivo = QtGui.QMenu(self.menuBar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuEdicion = QtGui.QMenu(self.menuBar)
        self.menuEdicion.setObjectName(_fromUtf8("menuEdicion"))
        self.menuAyuda = QtGui.QMenu(self.menuBar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        self.menuGridWorld = QtGui.QMenu(self.menuBar)
        self.menuGridWorld.setObjectName(_fromUtf8("menuGridWorld"))
        self.menuDimension = QtGui.QMenu(self.menuGridWorld)
        self.menuDimension.setObjectName(_fromUtf8("menuDimension"))
        self.menuOperaciones = QtGui.QMenu(self.menuBar)
        self.menuOperaciones.setObjectName(_fromUtf8("menuOperaciones"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionAppSalir = QtGui.QAction(MainWindow)
        self.actionAppSalir.setObjectName(_fromUtf8("actionAppSalir"))
        self.actionAcercaDe = QtGui.QAction(MainWindow)
        self.actionAcercaDe.setObjectName(_fromUtf8("actionAcercaDe"))
        self.actionGenerarValoresAleatorios = QtGui.QAction(MainWindow)
        self.actionGenerarValoresAleatorios.setObjectName(_fromUtf8("actionGenerarValoresAleatorios"))
        self.menuArchivo.addAction(self.actionAppSalir)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menuGridWorld.addAction(self.menuDimension.menuAction())
        self.menuOperaciones.addAction(self.actionGenerarValoresAleatorios)
        self.menuBar.addAction(self.menuArchivo.menuAction())
        self.menuBar.addAction(self.menuEdicion.menuAction())
        self.menuBar.addAction(self.menuGridWorld.menuAction())
        self.menuBar.addAction(self.menuOperaciones.menuAction())
        self.menuBar.addAction(self.menuAyuda.menuAction())
        self.label.setBuddy(self.cbGWDimension)
        self.label_2.setBuddy(self.cbQLTecnicas)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Grid World", None))
        self.label.setText(_translate("MainWindow", "Dimensión:", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Q-Learning", None))
        self.label_5.setText(_translate("MainWindow", "Epsilon (ɛ):", None))
        self.label_3.setText(_translate("MainWindow", "Alfa (ɑ):", None))
        self.label_4.setText(_translate("MainWindow", "Gamma (Ɣ):", None))
        self.label_2.setText(_translate("MainWindow", "Técnica de aprendizaje:", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Operaciones", None))
        self.pushButton.setText(_translate("MainWindow", "Generar valores aleatorios", None))
        self.menuArchivo.setTitle(_translate("MainWindow", "&Archivo", None))
        self.menuEdicion.setTitle(_translate("MainWindow", "&Edición", None))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ay&uda", None))
        self.menuGridWorld.setTitle(_translate("MainWindow", "&Grid World", None))
        self.menuDimension.setTitle(_translate("MainWindow", "Dimensión", None))
        self.menuOperaciones.setTitle(_translate("MainWindow", "&Operaciones", None))
        self.actionAppSalir.setText(_translate("MainWindow", "Salir", None))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de...", None))
        self.actionGenerarValoresAleatorios.setText(_translate("MainWindow", "Generar valores aleatorios", None))

