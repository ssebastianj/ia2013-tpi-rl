# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\mainwindow.ui'
#
# Created: Sun Apr 07 19:34:18 2013
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
        MainWindow.resize(505, 418)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
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
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grupoGamma = QtGui.QHBoxLayout()
        self.grupoGamma.setObjectName(_fromUtf8("grupoGamma"))
        self.lblGamma = QtGui.QLabel(self.groupBox_3)
        self.lblGamma.setObjectName(_fromUtf8("lblGamma"))
        self.grupoGamma.addWidget(self.lblGamma)
        self.sbQLGamma = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLGamma.setMaximum(0.99)
        self.sbQLGamma.setSingleStep(0.01)
        self.sbQLGamma.setObjectName(_fromUtf8("sbQLGamma"))
        self.grupoGamma.addWidget(self.sbQLGamma)
        self.verticalLayout.addLayout(self.grupoGamma)
        self.grupoTecnica = QtGui.QHBoxLayout()
        self.grupoTecnica.setObjectName(_fromUtf8("grupoTecnica"))
        self.lblTecnica = QtGui.QLabel(self.groupBox_3)
        self.lblTecnica.setObjectName(_fromUtf8("lblTecnica"))
        self.grupoTecnica.addWidget(self.lblTecnica)
        self.cbQLTecnicas = QtGui.QComboBox(self.groupBox_3)
        self.cbQLTecnicas.setObjectName(_fromUtf8("cbQLTecnicas"))
        self.grupoTecnica.addWidget(self.cbQLTecnicas)
        self.verticalLayout.addLayout(self.grupoTecnica)
        self.grupoEpsilon = QtGui.QHBoxLayout()
        self.grupoEpsilon.setObjectName(_fromUtf8("grupoEpsilon"))
        self.lblEpsilon = QtGui.QLabel(self.groupBox_3)
        self.lblEpsilon.setObjectName(_fromUtf8("lblEpsilon"))
        self.grupoEpsilon.addWidget(self.lblEpsilon)
        self.sbQLEpsilon = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLEpsilon.setMaximum(0.99)
        self.sbQLEpsilon.setSingleStep(0.01)
        self.sbQLEpsilon.setObjectName(_fromUtf8("sbQLEpsilon"))
        self.grupoEpsilon.addWidget(self.sbQLEpsilon)
        self.verticalLayout.addLayout(self.grupoEpsilon)
        self.grupoTau = QtGui.QHBoxLayout()
        self.grupoTau.setObjectName(_fromUtf8("grupoTau"))
        self.lblTau = QtGui.QLabel(self.groupBox_3)
        self.lblTau.setObjectName(_fromUtf8("lblTau"))
        self.grupoTau.addWidget(self.lblTau)
        self.sbQLTau = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.sbQLTau.setMaximum(0.99)
        self.sbQLTau.setSingleStep(0.01)
        self.sbQLTau.setObjectName(_fromUtf8("sbQLTau"))
        self.grupoTau.addWidget(self.sbQLTau)
        self.verticalLayout.addLayout(self.grupoTau)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.btnEntrenar = QtGui.QPushButton(self.groupBox_2)
        self.btnEntrenar.setObjectName(_fromUtf8("btnEntrenar"))
        self.gridLayout_3.addWidget(self.btnEntrenar, 2, 0, 1, 1)
        self.btnComenzarPlay = QtGui.QPushButton(self.groupBox_2)
        self.btnComenzarPlay.setObjectName(_fromUtf8("btnComenzarPlay"))
        self.gridLayout_3.addWidget(self.btnComenzarPlay, 3, 0, 1, 1)
        self.btnGenValAleatorios = QtGui.QPushButton(self.groupBox_2)
        self.btnGenValAleatorios.setObjectName(_fromUtf8("btnGenValAleatorios"))
        self.gridLayout_3.addWidget(self.btnGenValAleatorios, 0, 0, 1, 1)
        self.btnTerminarProceso = QtGui.QPushButton(self.groupBox_2)
        self.btnTerminarProceso.setObjectName(_fromUtf8("btnTerminarProceso"))
        self.gridLayout_3.addWidget(self.btnTerminarProceso, 4, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.tblGridWorld = QtGui.QTableWidget(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblGridWorld.sizePolicy().hasHeightForWidth())
        self.tblGridWorld.setSizePolicy(sizePolicy)
        self.tblGridWorld.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tblGridWorld.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblGridWorld.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblGridWorld.setAutoScroll(False)
        self.tblGridWorld.setTabKeyNavigation(False)
        self.tblGridWorld.setProperty("showDropIndicator", False)
        self.tblGridWorld.setDragDropOverwriteMode(False)
        self.tblGridWorld.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tblGridWorld.setCornerButtonEnabled(False)
        self.tblGridWorld.setObjectName(_fromUtf8("tblGridWorld"))
        self.tblGridWorld.setColumnCount(0)
        self.tblGridWorld.setRowCount(0)
        self.gridLayout_2.addWidget(self.tblGridWorld, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 505, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuArchivo = QtGui.QMenu(self.menuBar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuEdicion = QtGui.QMenu(self.menuBar)
        self.menuEdicion.setObjectName(_fromUtf8("menuEdicion"))
        self.menuAyuda = QtGui.QMenu(self.menuBar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        self.menuOperaciones = QtGui.QMenu(self.menuBar)
        self.menuOperaciones.setObjectName(_fromUtf8("menuOperaciones"))
        self.menu_Configuraci_n = QtGui.QMenu(self.menuBar)
        self.menu_Configuraci_n.setObjectName(_fromUtf8("menu_Configuraci_n"))
        self.menuGridWorld = QtGui.QMenu(self.menu_Configuraci_n)
        self.menuGridWorld.setObjectName(_fromUtf8("menuGridWorld"))
        self.menuDimension = QtGui.QMenu(self.menuGridWorld)
        self.menuDimension.setObjectName(_fromUtf8("menuDimension"))
        self.menuTecnicas = QtGui.QMenu(self.menu_Configuraci_n)
        self.menuTecnicas.setObjectName(_fromUtf8("menuTecnicas"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionAppSalir = QtGui.QAction(MainWindow)
        self.actionAppSalir.setObjectName(_fromUtf8("actionAppSalir"))
        self.actionAcercaDe = QtGui.QAction(MainWindow)
        self.actionAcercaDe.setObjectName(_fromUtf8("actionAcercaDe"))
        self.actionGenValAleatorios = QtGui.QAction(MainWindow)
        self.actionGenValAleatorios.setObjectName(_fromUtf8("actionGenValAleatorios"))
        self.actionEntrenar = QtGui.QAction(MainWindow)
        self.actionEntrenar.setObjectName(_fromUtf8("actionEntrenar"))
        self.actionComenzarPlay = QtGui.QAction(MainWindow)
        self.actionComenzarPlay.setObjectName(_fromUtf8("actionComenzarPlay"))
        self.actionTerminarProceso = QtGui.QAction(MainWindow)
        self.actionTerminarProceso.setObjectName(_fromUtf8("actionTerminarProceso"))
        self.actionSoftmax = QtGui.QAction(MainWindow)
        self.actionSoftmax.setObjectName(_fromUtf8("actionSoftmax"))
        self.actionE_Greedy = QtGui.QAction(MainWindow)
        self.actionE_Greedy.setObjectName(_fromUtf8("actionE_Greedy"))
        self.menuArchivo.addAction(self.actionAppSalir)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menuOperaciones.addAction(self.actionGenValAleatorios)
        self.menuOperaciones.addAction(self.actionEntrenar)
        self.menuOperaciones.addAction(self.actionComenzarPlay)
        self.menuOperaciones.addAction(self.actionTerminarProceso)
        self.menuGridWorld.addAction(self.menuDimension.menuAction())
        self.menu_Configuraci_n.addAction(self.menuGridWorld.menuAction())
        self.menu_Configuraci_n.addAction(self.menuTecnicas.menuAction())
        self.menuBar.addAction(self.menuArchivo.menuAction())
        self.menuBar.addAction(self.menuEdicion.menuAction())
        self.menuBar.addAction(self.menu_Configuraci_n.menuAction())
        self.menuBar.addAction(self.menuOperaciones.menuAction())
        self.menuBar.addAction(self.menuAyuda.menuAction())
        self.label.setBuddy(self.cbGWDimension)
        self.lblGamma.setBuddy(self.sbQLGamma)
        self.lblTecnica.setBuddy(self.cbQLTecnicas)
        self.lblEpsilon.setBuddy(self.sbQLEpsilon)
        self.lblTau.setBuddy(self.sbQLTau)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Grid World", None))
        self.label.setText(_translate("MainWindow", "Dimensión:", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Q-Learning", None))
        self.lblGamma.setText(_translate("MainWindow", "Gamma (Ɣ):", None))
        self.lblTecnica.setText(_translate("MainWindow", "Técnica de aprendizaje:", None))
        self.lblEpsilon.setText(_translate("MainWindow", "Epsilon (ɛ):", None))
        self.lblTau.setText(_translate("MainWindow", "Tau (τ):", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Operaciones", None))
        self.btnEntrenar.setText(_translate("MainWindow", "Entrenar", None))
        self.btnComenzarPlay.setText(_translate("MainWindow", "Comenzar", None))
        self.btnGenValAleatorios.setText(_translate("MainWindow", "Generar valores aleatorios...", None))
        self.btnTerminarProceso.setText(_translate("MainWindow", "Terminar", None))
        self.menuArchivo.setTitle(_translate("MainWindow", "&Archivo", None))
        self.menuEdicion.setTitle(_translate("MainWindow", "&Edición", None))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ay&uda", None))
        self.menuOperaciones.setTitle(_translate("MainWindow", "&Operaciones", None))
        self.menu_Configuraci_n.setTitle(_translate("MainWindow", "&Configuración", None))
        self.menuGridWorld.setTitle(_translate("MainWindow", "Grid World", None))
        self.menuDimension.setTitle(_translate("MainWindow", "Dimensión", None))
        self.menuTecnicas.setTitle(_translate("MainWindow", "Técnicas", None))
        self.actionAppSalir.setText(_translate("MainWindow", "Salir", None))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de...", None))
        self.actionGenValAleatorios.setText(_translate("MainWindow", "Generar valores aleatorios...", None))
        self.actionEntrenar.setText(_translate("MainWindow", "Entrenar", None))
        self.actionComenzarPlay.setText(_translate("MainWindow", "Comenzar", None))
        self.actionTerminarProceso.setText(_translate("MainWindow", "Terminar", None))
        self.actionSoftmax.setText(_translate("MainWindow", "Softmax", None))
        self.actionE_Greedy.setText(_translate("MainWindow", "E-Greedy", None))

