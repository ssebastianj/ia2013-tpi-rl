# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\mainwindow.ui'
#
# Created: Sun May 12 17:40:22 2013
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
        MainWindow.resize(559, 704)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/:iconos/LogoUTN")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout_6 = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.tblGridWorld = QtGui.QTableWidget(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblGridWorld.sizePolicy().hasHeightForWidth())
        self.tblGridWorld.setSizePolicy(sizePolicy)
        self.tblGridWorld.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblGridWorld.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblGridWorld.setAutoScroll(False)
        self.tblGridWorld.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tblGridWorld.setTabKeyNavigation(False)
        self.tblGridWorld.setProperty("showDropIndicator", False)
        self.tblGridWorld.setDragDropOverwriteMode(False)
        self.tblGridWorld.setAlternatingRowColors(False)
        self.tblGridWorld.setCornerButtonEnabled(False)
        self.tblGridWorld.setObjectName(_fromUtf8("tblGridWorld"))
        self.tblGridWorld.setColumnCount(0)
        self.tblGridWorld.setRowCount(0)
        self.gridLayout_6.addWidget(self.tblGridWorld, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 559, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuArchivo = QtGui.QMenu(self.menuBar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuEdicion = QtGui.QMenu(self.menuBar)
        self.menuEdicion.setObjectName(_fromUtf8("menuEdicion"))
        self.menuAyuda = QtGui.QMenu(self.menuBar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        self.menuOperaciones = QtGui.QMenu(self.menuBar)
        self.menuOperaciones.setObjectName(_fromUtf8("menuOperaciones"))
        self.menuConfiguracion = QtGui.QMenu(self.menuBar)
        self.menuConfiguracion.setObjectName(_fromUtf8("menuConfiguracion"))
        self.menuGridWorld = QtGui.QMenu(self.menuConfiguracion)
        self.menuGridWorld.setObjectName(_fromUtf8("menuGridWorld"))
        self.menuQLearning = QtGui.QMenu(self.menuConfiguracion)
        self.menuQLearning.setObjectName(_fromUtf8("menuQLearning"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_5 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gbGridWorld = QtGui.QGroupBox(self.dockWidgetContents)
        self.gbGridWorld.setObjectName(_fromUtf8("gbGridWorld"))
        self.gridLayout = QtGui.QGridLayout(self.gbGridWorld)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_5 = QtGui.QGroupBox(self.gbGridWorld)
        self.groupBox_5.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_11 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_11.setContentsMargins(-1, 4, -1, 2)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.btnInicializarGW = QtGui.QPushButton(self.groupBox_5)
        self.btnInicializarGW.setMaximumSize(QtCore.QSize(90, 22))
        self.btnInicializarGW.setObjectName(_fromUtf8("btnInicializarGW"))
        self.gridLayout_10.addWidget(self.btnInicializarGW, 0, 0, 1, 1)
        self.btnGWGenerarEstados = QtGui.QPushButton(self.groupBox_5)
        self.btnGWGenerarEstados.setMaximumSize(QtCore.QSize(16777215, 22))
        self.btnGWGenerarEstados.setObjectName(_fromUtf8("btnGWGenerarEstados"))
        self.gridLayout_10.addWidget(self.btnGWGenerarEstados, 0, 1, 1, 1)
        self.btnGWOpciones = QtGui.QToolButton(self.groupBox_5)
        self.btnGWOpciones.setMinimumSize(QtCore.QSize(25, 0))
        self.btnGWOpciones.setMaximumSize(QtCore.QSize(16777215, 22))
        self.btnGWOpciones.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/:iconos/Configurar")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnGWOpciones.setIcon(icon1)
        self.btnGWOpciones.setObjectName(_fromUtf8("btnGWOpciones"))
        self.gridLayout_10.addWidget(self.btnGWOpciones, 0, 2, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.gbGridWorld)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cbGWDimension = QtGui.QComboBox(self.gbGridWorld)
        self.cbGWDimension.setObjectName(_fromUtf8("cbGWDimension"))
        self.horizontalLayout.addWidget(self.cbGWDimension)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.gbGridWorld, 0, 0, 1, 1)
        self.gbQLearning = QtGui.QGroupBox(self.dockWidgetContents)
        self.gbQLearning.setObjectName(_fromUtf8("gbQLearning"))
        self.gridLayout_8 = QtGui.QGridLayout(self.gbQLearning)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.lblGamma = QtGui.QLabel(self.gbQLearning)
        self.lblGamma.setMaximumSize(QtCore.QSize(115, 16777215))
        self.lblGamma.setObjectName(_fromUtf8("lblGamma"))
        self.gridLayout_7.addWidget(self.lblGamma, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gbQLearning)
        self.label_2.setMaximumSize(QtCore.QSize(115, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_7.addWidget(self.label_2, 1, 0, 1, 1)
        self.sbCantidadEpisodios = QtGui.QSpinBox(self.gbQLearning)
        self.sbCantidadEpisodios.setMinimum(1)
        self.sbCantidadEpisodios.setMaximum(1000000000)
        self.sbCantidadEpisodios.setObjectName(_fromUtf8("sbCantidadEpisodios"))
        self.gridLayout_7.addWidget(self.sbCantidadEpisodios, 1, 1, 1, 2)
        self.sbQLGamma = QtGui.QDoubleSpinBox(self.gbQLearning)
        self.sbQLGamma.setMaximum(0.99)
        self.sbQLGamma.setSingleStep(0.01)
        self.sbQLGamma.setObjectName(_fromUtf8("sbQLGamma"))
        self.gridLayout_7.addWidget(self.sbQLGamma, 0, 1, 1, 2)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(self.gbQLearning)
        self.groupBox_6.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_6.setFlat(True)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_12 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblTau = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTau.sizePolicy().hasHeightForWidth())
        self.lblTau.setSizePolicy(sizePolicy)
        self.lblTau.setMaximumSize(QtCore.QSize(125, 16777215))
        self.lblTau.setObjectName(_fromUtf8("lblTau"))
        self.gridLayout_4.addWidget(self.lblTau, 2, 0, 1, 2)
        self.cbQLTecnicas = QtGui.QComboBox(self.groupBox_6)
        self.cbQLTecnicas.setObjectName(_fromUtf8("cbQLTecnicas"))
        self.gridLayout_4.addWidget(self.cbQLTecnicas, 0, 2, 1, 2)
        self.lblEpsilon = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEpsilon.sizePolicy().hasHeightForWidth())
        self.lblEpsilon.setSizePolicy(sizePolicy)
        self.lblEpsilon.setMaximumSize(QtCore.QSize(125, 16777215))
        self.lblEpsilon.setObjectName(_fromUtf8("lblEpsilon"))
        self.gridLayout_4.addWidget(self.lblEpsilon, 1, 0, 1, 2)
        self.lblTecnica = QtGui.QLabel(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTecnica.sizePolicy().hasHeightForWidth())
        self.lblTecnica.setSizePolicy(sizePolicy)
        self.lblTecnica.setMaximumSize(QtCore.QSize(125, 16777215))
        self.lblTecnica.setObjectName(_fromUtf8("lblTecnica"))
        self.gridLayout_4.addWidget(self.lblTecnica, 0, 0, 1, 2)
        self.sbQLEpsilon = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.sbQLEpsilon.setMaximum(0.99)
        self.sbQLEpsilon.setSingleStep(0.01)
        self.sbQLEpsilon.setObjectName(_fromUtf8("sbQLEpsilon"))
        self.gridLayout_4.addWidget(self.sbQLEpsilon, 1, 2, 1, 2)
        self.sbQLTau = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.sbQLTau.setMaximum(0.99)
        self.sbQLTau.setSingleStep(0.01)
        self.sbQLTau.setObjectName(_fromUtf8("sbQLTau"))
        self.gridLayout_4.addWidget(self.sbQLTau, 2, 2, 1, 2)
        self.gridLayout_12.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(-1, 4, -1, -1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_6)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.sbCantEpisodiosDec = QtGui.QSpinBox(self.groupBox_6)
        self.sbCantEpisodiosDec.setEnabled(False)
        self.sbCantEpisodiosDec.setMinimum(1)
        self.sbCantEpisodiosDec.setMaximum(1000000000)
        self.sbCantEpisodiosDec.setObjectName(_fromUtf8("sbCantEpisodiosDec"))
        self.gridLayout_2.addWidget(self.sbCantEpisodiosDec, 1, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_6)
        self.label_5.setEnabled(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.sbDecrementoVal = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.sbDecrementoVal.setEnabled(False)
        self.sbDecrementoVal.setMinimumSize(QtCore.QSize(50, 0))
        self.sbDecrementoVal.setMinimum(0.01)
        self.sbDecrementoVal.setMaximum(0.99)
        self.sbDecrementoVal.setSingleStep(0.01)
        self.sbDecrementoVal.setProperty("value", 0.01)
        self.sbDecrementoVal.setObjectName(_fromUtf8("sbDecrementoVal"))
        self.horizontalLayout_3.addWidget(self.sbDecrementoVal)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 2, 1, 1)
        self.chkDecrementarParam = QtGui.QCheckBox(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkDecrementarParam.sizePolicy().hasHeightForWidth())
        self.chkDecrementarParam.setSizePolicy(sizePolicy)
        self.chkDecrementarParam.setObjectName(_fromUtf8("chkDecrementarParam"))
        self.gridLayout_2.addWidget(self.chkDecrementarParam, 0, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_6, 1, 0, 1, 1)
        self.groupBox_7 = QtGui.QGroupBox(self.gbQLearning)
        self.groupBox_7.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_7.setFlat(True)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_13 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_13.setContentsMargins(-1, 4, -1, 2)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.btnInicializarValoresQL = QtGui.QPushButton(self.groupBox_7)
        self.btnInicializarValoresQL.setMaximumSize(QtCore.QSize(130, 22))
        self.btnInicializarValoresQL.setObjectName(_fromUtf8("btnInicializarValoresQL"))
        self.gridLayout_13.addWidget(self.btnInicializarValoresQL, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.gbQLearning, 1, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 4, 0, 1, 1)
        self.gbGeneral = QtGui.QGroupBox(self.dockWidgetContents)
        self.gbGeneral.setObjectName(_fromUtf8("gbGeneral"))
        self.gridLayout_9 = QtGui.QGridLayout(self.gbGeneral)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.btnInicializarTodo = QtGui.QPushButton(self.gbGeneral)
        self.btnInicializarTodo.setMaximumSize(QtCore.QSize(130, 16777215))
        self.btnInicializarTodo.setObjectName(_fromUtf8("btnInicializarTodo"))
        self.gridLayout_9.addWidget(self.btnInicializarTodo, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.gbGeneral, 3, 0, 1, 1)
        self.gbAgente = QtGui.QGroupBox(self.dockWidgetContents)
        self.gbAgente.setObjectName(_fromUtf8("gbAgente"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gbAgente)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.btnEntrenar = QtGui.QPushButton(self.gbAgente)
        self.btnEntrenar.setMaximumSize(QtCore.QSize(130, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/:iconos/Aprender")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEntrenar.setIcon(icon2)
        self.btnEntrenar.setObjectName(_fromUtf8("btnEntrenar"))
        self.gridLayout_3.addWidget(self.btnEntrenar, 2, 1, 1, 1)
        self.btnRecorrer = QtGui.QPushButton(self.gbAgente)
        self.btnRecorrer.setMaximumSize(QtCore.QSize(130, 16777215))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/:iconos/Recorrer")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRecorrer.setIcon(icon3)
        self.btnRecorrer.setObjectName(_fromUtf8("btnRecorrer"))
        self.gridLayout_3.addWidget(self.btnRecorrer, 3, 1, 1, 1)
        self.btnTerminarProceso = QtGui.QPushButton(self.gbAgente)
        self.btnTerminarProceso.setMaximumSize(QtCore.QSize(130, 16777215))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/:iconos/Cancelar")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTerminarProceso.setIcon(icon4)
        self.btnTerminarProceso.setObjectName(_fromUtf8("btnTerminarProceso"))
        self.gridLayout_3.addWidget(self.btnTerminarProceso, 4, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(35, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 3, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(35, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 3, 2, 1, 1)
        self.gridLayout_5.addWidget(self.gbAgente, 2, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionAppSalir = QtGui.QAction(MainWindow)
        self.actionAppSalir.setObjectName(_fromUtf8("actionAppSalir"))
        self.actionAcercaDe = QtGui.QAction(MainWindow)
        self.actionAcercaDe.setObjectName(_fromUtf8("actionAcercaDe"))
        self.actionAgenteEntrenar = QtGui.QAction(MainWindow)
        self.actionAgenteEntrenar.setIcon(icon2)
        self.actionAgenteEntrenar.setObjectName(_fromUtf8("actionAgenteEntrenar"))
        self.actionAgenteRecorrer = QtGui.QAction(MainWindow)
        self.actionAgenteRecorrer.setIcon(icon3)
        self.actionAgenteRecorrer.setObjectName(_fromUtf8("actionAgenteRecorrer"))
        self.actionAgenteCancelar = QtGui.QAction(MainWindow)
        self.actionAgenteCancelar.setIcon(icon4)
        self.actionAgenteCancelar.setObjectName(_fromUtf8("actionAgenteCancelar"))
        self.actionInicializarTodo = QtGui.QAction(MainWindow)
        self.actionInicializarTodo.setObjectName(_fromUtf8("actionInicializarTodo"))
        self.menuArchivo.addAction(self.actionAppSalir)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.menuOperaciones.addAction(self.actionAgenteEntrenar)
        self.menuOperaciones.addAction(self.actionAgenteRecorrer)
        self.menuOperaciones.addAction(self.actionAgenteCancelar)
        self.menuConfiguracion.addAction(self.menuGridWorld.menuAction())
        self.menuConfiguracion.addAction(self.menuQLearning.menuAction())
        self.menuConfiguracion.addSeparator()
        self.menuConfiguracion.addAction(self.actionInicializarTodo)
        self.menuBar.addAction(self.menuArchivo.menuAction())
        self.menuBar.addAction(self.menuEdicion.menuAction())
        self.menuBar.addAction(self.menuConfiguracion.menuAction())
        self.menuBar.addAction(self.menuOperaciones.menuAction())
        self.menuBar.addAction(self.menuAyuda.menuAction())
        self.label.setBuddy(self.cbGWDimension)
        self.lblGamma.setBuddy(self.sbQLGamma)
        self.lblTau.setBuddy(self.sbQLTau)
        self.lblEpsilon.setBuddy(self.sbQLEpsilon)
        self.lblTecnica.setBuddy(self.cbQLTecnicas)
        self.label_3.setBuddy(self.sbCantEpisodiosDec)
        self.label_5.setBuddy(self.sbDecrementoVal)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.chkDecrementarParam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_3.setEnabled)
        QtCore.QObject.connect(self.chkDecrementarParam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_5.setEnabled)
        QtCore.QObject.connect(self.chkDecrementarParam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.sbCantEpisodiosDec.setEnabled)
        QtCore.QObject.connect(self.chkDecrementarParam, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.sbDecrementoVal.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.cbGWDimension, self.btnInicializarGW)
        MainWindow.setTabOrder(self.btnInicializarGW, self.btnGWGenerarEstados)
        MainWindow.setTabOrder(self.btnGWGenerarEstados, self.btnGWOpciones)
        MainWindow.setTabOrder(self.btnGWOpciones, self.sbQLGamma)
        MainWindow.setTabOrder(self.sbQLGamma, self.sbCantidadEpisodios)
        MainWindow.setTabOrder(self.sbCantidadEpisodios, self.cbQLTecnicas)
        MainWindow.setTabOrder(self.cbQLTecnicas, self.sbQLEpsilon)
        MainWindow.setTabOrder(self.sbQLEpsilon, self.sbQLTau)
        MainWindow.setTabOrder(self.sbQLTau, self.chkDecrementarParam)
        MainWindow.setTabOrder(self.chkDecrementarParam, self.sbCantEpisodiosDec)
        MainWindow.setTabOrder(self.sbCantEpisodiosDec, self.sbDecrementoVal)
        MainWindow.setTabOrder(self.sbDecrementoVal, self.btnInicializarValoresQL)
        MainWindow.setTabOrder(self.btnInicializarValoresQL, self.tblGridWorld)
        MainWindow.setTabOrder(self.tblGridWorld, self.btnEntrenar)
        MainWindow.setTabOrder(self.btnEntrenar, self.btnRecorrer)
        MainWindow.setTabOrder(self.btnRecorrer, self.btnTerminarProceso)
        MainWindow.setTabOrder(self.btnTerminarProceso, self.btnInicializarTodo)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Grupo Nº 1 - Inteligencia Artificial 2013 - Aprendizaje por Refuerzo", None))
        self.menuArchivo.setTitle(_translate("MainWindow", "&Archivo", None))
        self.menuEdicion.setTitle(_translate("MainWindow", "&Edición", None))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ay&uda", None))
        self.menuOperaciones.setTitle(_translate("MainWindow", "Agente", None))
        self.menuConfiguracion.setTitle(_translate("MainWindow", "&Configuración", None))
        self.menuGridWorld.setTitle(_translate("MainWindow", "Grid World", None))
        self.menuQLearning.setTitle(_translate("MainWindow", "Q-Learning", None))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Herramientas", None))
        self.gbGridWorld.setTitle(_translate("MainWindow", "Grid World", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Acciones", None))
        self.btnInicializarGW.setText(_translate("MainWindow", "Inicializar GW", None))
        self.btnGWGenerarEstados.setText(_translate("MainWindow", "Generar estados...", None))
        self.btnGWOpciones.setToolTip(_translate("MainWindow", "<html><head/><body><p>Configurar Grid World</p></body></html>", None))
        self.label.setText(_translate("MainWindow", "Dimensión:", None))
        self.gbQLearning.setTitle(_translate("MainWindow", "Q-Learning", None))
        self.lblGamma.setText(_translate("MainWindow", "Gamma (Ɣ):", None))
        self.label_2.setText(_translate("MainWindow", "Cantidad de episodios:", None))
        self.sbCantidadEpisodios.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; font-style:italic;\">Cantidad de Episodios</span></p><p>Número de Episodios (Plays) a realizar durante la fase de aprendizaje (entrenamiento). Un episodio es un recorrido desde un estado dado hasta el estado <span style=\" font-style:italic;\">final.</span></p></body></html>", None))
        self.sbQLGamma.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; font-style:italic;\">Factor de descuento</span></p><p>Cuanto más cerca de 1 se encuentre este valor mayor será el <span style=\" font-style:italic;\">peso</span> asignado a los refuerzos futuros.</p></body></html>", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Técnica", None))
        self.lblTau.setText(_translate("MainWindow", "Tau (τ):", None))
        self.lblEpsilon.setText(_translate("MainWindow", "Epsilon (ɛ):", None))
        self.lblTecnica.setText(_translate("MainWindow", "Técnica de aprendizaje:", None))
        self.sbQLEpsilon.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; font-style:italic;\">Epsilon (</span><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">ɛ</span><span style=\" font-weight:600; font-style:italic;\">)</span></p><p>Parámetro que establece la probabilidad de seleccionar una <span style=\" font-style:italic;\">acción</span> aleatoria por sobre la política óptima. Rango de valores: 0 ≤ <span style=\" font-size:9pt;\">ɛ</span> &lt; 1.</p></body></html>", None))
        self.sbQLTau.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; font-style:italic;\">Tau (</span><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">τ</span><span style=\" font-weight:600; font-style:italic;\">)</span></p><p>Parámetro que establece la <span style=\" font-style:italic;\">temperatura</span>. Una <span style=\" font-style:italic;\">temperatura alta</span> causa que todas las acciones sean (casi) equiprobables. Una <span style=\" font-style:italic;\">temperatura baja</span> causa una mayor diferencia en la probabilidad de selección para las acciones que difieran en las estimaciones de sus valores.</p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "Cada:", None))
        self.sbCantEpisodiosDec.setToolTip(_translate("MainWindow", "<html><head/><body><p>Intervalo de episodios entre las cuales el parámetro será decrementado.</p></body></html>", None))
        self.label_5.setText(_translate("MainWindow", "Decremento:", None))
        self.sbDecrementoVal.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-style:italic;\">Paso</span> o valor de decremento. En cada intervalo el parámetro será decrementado en un <span style=\" font-style:italic;\">paso.</span></p></body></html>", None))
        self.chkDecrementarParam.setToolTip(_translate("MainWindow", "<html><head/><body><p>Decrementar el parámetro que se esté utilizando.</p></body></html>", None))
        self.chkDecrementarParam.setText(_translate("MainWindow", "Decrementar parámetro", None))
        self.groupBox_7.setTitle(_translate("MainWindow", "Acciones", None))
        self.btnInicializarValoresQL.setText(_translate("MainWindow", "Inicializar valores", None))
        self.gbGeneral.setTitle(_translate("MainWindow", "General", None))
        self.btnInicializarTodo.setText(_translate("MainWindow", "Inicializar valores", None))
        self.gbAgente.setTitle(_translate("MainWindow", "Agente", None))
        self.btnEntrenar.setText(_translate("MainWindow", "Entrenar", None))
        self.btnRecorrer.setText(_translate("MainWindow", "Recorrer", None))
        self.btnTerminarProceso.setText(_translate("MainWindow", "Cancelar", None))
        self.actionAppSalir.setText(_translate("MainWindow", "Salir", None))
        self.actionAcercaDe.setText(_translate("MainWindow", "Acerca de...", None))
        self.actionAgenteEntrenar.setText(_translate("MainWindow", "Entrenar", None))
        self.actionAgenteRecorrer.setText(_translate("MainWindow", "Recorrer", None))
        self.actionAgenteCancelar.setText(_translate("MainWindow", "Cancelar", None))
        self.actionInicializarTodo.setText(_translate("MainWindow", "Inicializar todo", None))

import recursos_rc
