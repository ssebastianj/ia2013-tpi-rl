# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Sebastian\Mis documentos\Programacion\Proyectos\IA2013TPIRL\gui\qt\IA2013TPIRLGUI\gwopcionesdialog.ui'
#
# Created: Sun May 12 16:15:38 2013
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
        GWOpcionesDialog.resize(245, 309)
        GWOpcionesDialog.setMinimumSize(QtCore.QSize(201, 0))
        GWOpcionesDialog.setModal(True)
        self.gridLayout_5 = QtGui.QGridLayout(GWOpcionesDialog)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pushButton = QtGui.QPushButton(GWOpcionesDialog)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_4.addWidget(self.pushButton, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 3, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(GWOpcionesDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.sbGWEstadoSize = QtGui.QSpinBox(self.groupBox)
        self.sbGWEstadoSize.setMinimum(20)
        self.sbGWEstadoSize.setMaximum(100)
        self.sbGWEstadoSize.setProperty("value", 40)
        self.sbGWEstadoSize.setObjectName(_fromUtf8("sbGWEstadoSize"))
        self.horizontalLayout.addWidget(self.sbGWEstadoSize)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(GWOpcionesDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.sbRecomFinal = QtGui.QSpinBox(self.groupBox_2)
        self.sbRecomFinal.setEnabled(False)
        self.sbRecomFinal.setMinimum(-1000)
        self.sbRecomFinal.setMaximum(1000)
        self.sbRecomFinal.setObjectName(_fromUtf8("sbRecomFinal"))
        self.horizontalLayout_3.addWidget(self.sbRecomFinal)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(70, 0))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.sbRecomMalo = QtGui.QSpinBox(self.groupBox_2)
        self.sbRecomMalo.setMinimum(-1000)
        self.sbRecomMalo.setMaximum(1000)
        self.sbRecomMalo.setObjectName(_fromUtf8("sbRecomMalo"))
        self.horizontalLayout_6.addWidget(self.sbRecomMalo)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(70, 0))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cbRecomPared = QtGui.QComboBox(self.groupBox_2)
        self.cbRecomPared.setObjectName(_fromUtf8("cbRecomPared"))
        self.gridLayout_2.addWidget(self.cbRecomPared, 0, 1, 1, 1)
        self.sbRecomPared = QtGui.QSpinBox(self.groupBox_2)
        self.sbRecomPared.setMinimum(-1000)
        self.sbRecomPared.setMaximum(1000)
        self.sbRecomPared.setObjectName(_fromUtf8("sbRecomPared"))
        self.gridLayout_2.addWidget(self.sbRecomPared, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(70, 0))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.sbRecomBueno = QtGui.QSpinBox(self.groupBox_2)
        self.sbRecomBueno.setMinimum(-1000)
        self.sbRecomBueno.setMaximum(1000)
        self.sbRecomBueno.setObjectName(_fromUtf8("sbRecomBueno"))
        self.horizontalLayout_5.addWidget(self.sbRecomBueno)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(70, 0))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.sbRecomExcelente = QtGui.QSpinBox(self.groupBox_2)
        self.sbRecomExcelente.setMinimum(-1000)
        self.sbRecomExcelente.setMaximum(1000)
        self.sbRecomExcelente.setObjectName(_fromUtf8("sbRecomExcelente"))
        self.horizontalLayout_4.addWidget(self.sbRecomExcelente)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 2)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.label.setBuddy(self.sbGWEstadoSize)
        self.label_3.setBuddy(self.sbRecomFinal)
        self.label_6.setBuddy(self.sbRecomMalo)
        self.label_7.setBuddy(self.cbRecomPared)
        self.label_5.setBuddy(self.sbRecomBueno)
        self.label_4.setBuddy(self.sbRecomExcelente)

        self.retranslateUi(GWOpcionesDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), GWOpcionesDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(GWOpcionesDialog)
        GWOpcionesDialog.setTabOrder(self.sbGWEstadoSize, self.sbRecomFinal)
        GWOpcionesDialog.setTabOrder(self.sbRecomFinal, self.sbRecomExcelente)
        GWOpcionesDialog.setTabOrder(self.sbRecomExcelente, self.sbRecomBueno)
        GWOpcionesDialog.setTabOrder(self.sbRecomBueno, self.sbRecomMalo)
        GWOpcionesDialog.setTabOrder(self.sbRecomMalo, self.cbRecomPared)
        GWOpcionesDialog.setTabOrder(self.cbRecomPared, self.sbRecomPared)
        GWOpcionesDialog.setTabOrder(self.sbRecomPared, self.pushButton)

    def retranslateUi(self, GWOpcionesDialog):
        GWOpcionesDialog.setWindowTitle(_translate("GWOpcionesDialog", "Configurar Grid World", None))
        self.pushButton.setText(_translate("GWOpcionesDialog", "&Aceptar", None))
        self.groupBox.setTitle(_translate("GWOpcionesDialog", "Formato", None))
        self.label.setText(_translate("GWOpcionesDialog", "Tamaño:", None))
        self.groupBox_2.setTitle(_translate("GWOpcionesDialog", "Recompensas", None))
        self.label_3.setText(_translate("GWOpcionesDialog", "Final:", None))
        self.label_6.setText(_translate("GWOpcionesDialog", "Malo:", None))
        self.label_7.setText(_translate("GWOpcionesDialog", "Pared:", None))
        self.label_5.setText(_translate("GWOpcionesDialog", "Bueno:", None))
        self.label_4.setText(_translate("GWOpcionesDialog", "Excelente:", None))

