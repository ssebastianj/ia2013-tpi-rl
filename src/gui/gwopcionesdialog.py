#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtCore, QtGui

from core.estado.estado import TipoEstado, TIPOESTADO
from gui.qtgen.gwopcionesdialog import Ui_GWOpcionesDialog

try:
    _tr = QtCore.QString.fromUtf8
except AttributeError:
    _tr = lambda s: s


class GWOpcionesDialog(QtGui.QDialog):
    u"""
    Clase de diálogo 'Opciones' heredada de QDialog.
    """
    def __init__(self, parent=None, opciones=None):
        u"""
        Constructor de la clase.

        :param parent: Widget padre.
        """
        super(GWOpcionesDialog, self).__init__(parent)

        self.GWOpcionesD = Ui_GWOpcionesDialog()
        self.GWOpcionesD.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Dialog |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowTitleHint)

        self._opciones = opciones
        self._init_vars()
        self.initialize_dialog()

    def _init_vars(self):
        u"""
        Inicializa atributos de la instancia.
        """
        self.estado_size = None
        self.pared_bloqueante = None
        self.recomp_final = None
        self.recomp_excelente = None
        self.recomp_bueno = None
        self.recomp_malo = None
        self.recomp_pared = None
        self.recomp_max = None
        self.rec_state_bg = "#000000"
        self.ent_state_bg = "#000000"
        self.tipos_estados = None

    def initialize_dialog(self):
        u"""
        Configura y establece estado de los widgets en el cuadro de diálogo.
        """
        self._set_dialog_signals()

        # Estado Excelente
        self.GWOpcionesD.sbExcelenteRecompensa.setMinimum(-1000000000)
        self.GWOpcionesD.sbExcelenteRecompensa.setMaximum(1000000000)

        estado_excelente = self._opciones["tipos_estados"][TIPOESTADO.EXCELENTE]
        self.GWOpcionesD.sbExcelenteRecompensa.setValue(estado_excelente.recompensa)
        self.GWOpcionesD.txtExcelenteNombre.setText(_tr(estado_excelente.nombre))
        self.GWOpcionesD.txtExcelenteLetra.setText(_tr(estado_excelente.letra))
        self.GWOpcionesD.txtExcelenteColor.setText(estado_excelente.color)
        # --------------------------------------------------------------------

        # Estado Bueno
        self.GWOpcionesD.sbBuenoRecompensa.setMinimum(-1000000000)
        self.GWOpcionesD.sbBuenoRecompensa.setMaximum(1000000000)

        estado_bueno = self._opciones["tipos_estados"][TIPOESTADO.BUENO]
        self.GWOpcionesD.sbBuenoRecompensa.setValue(estado_bueno.recompensa)
        self.GWOpcionesD.txtBuenoNombre.setText(_tr(estado_bueno.nombre))
        self.GWOpcionesD.txtBuenoLetra.setText(_tr(estado_bueno.letra))
        self.GWOpcionesD.txtBuenoColor.setText(estado_bueno.color)
        # --------------------------------------------------------------------

        # Estado Malo
        self.GWOpcionesD.sbMaloRecompensa.setMinimum(-1000000000)
        self.GWOpcionesD.sbMaloRecompensa.setMaximum(1000000000)

        estado_malo = self._opciones["tipos_estados"][TIPOESTADO.MALO]
        self.GWOpcionesD.sbMaloRecompensa.setValue(estado_malo.recompensa)
        self.GWOpcionesD.txtMaloNombre.setText(_tr(estado_malo.nombre))
        self.GWOpcionesD.txtMaloLetra.setText(_tr(estado_malo.letra))
        self.GWOpcionesD.txtMaloColor.setText(estado_malo.color)
        # --------------------------------------------------------------------

        # Estado Neutro
        self.GWOpcionesD.sbNeutroRecompensa.setMinimum(-1000000000)
        self.GWOpcionesD.sbNeutroRecompensa.setMaximum(1000000000)

        estado_neutro = self._opciones["tipos_estados"][TIPOESTADO.NEUTRO]
        self.GWOpcionesD.sbNeutroRecompensa.setValue(estado_neutro.recompensa)
        self.GWOpcionesD.txtNeutroNombre.setText(_tr(estado_neutro.nombre))
        self.GWOpcionesD.txtNeutroLetra.setText(_tr(estado_neutro.letra))
        self.GWOpcionesD.txtNeutroColor.setText(estado_neutro.color)
        # --------------------------------------------------------------------

        # Estado Pared
        estado_pared = self._opciones["tipos_estados"][TIPOESTADO.PARED]
        self.GWOpcionesD.txtParedNombre.setText(_tr(estado_pared.nombre))
        self.GWOpcionesD.txtParedLetra.setText(_tr(estado_pared.letra))
        self.GWOpcionesD.txtParedColor.setText(estado_pared.color)
        # --------------------------------------------------------------------

        # Estado Agente
        estado_agente = self._opciones["tipos_estados"][TIPOESTADO.AGENTE]
        self.GWOpcionesD.txtAgenteNombre.setText(_tr(estado_agente.nombre))
        self.GWOpcionesD.txtAgenteLetra.setText(_tr(estado_agente.letra))
        self.GWOpcionesD.txtAgenteColor.setText(estado_agente.color)
        # --------------------------------------------------------------------

        # Estado Final
        estado_final = self._opciones["tipos_estados"][TIPOESTADO.FINAL]
        self.GWOpcionesD.txtFinalNombre.setText(_tr(estado_final.nombre))
        self.GWOpcionesD.txtFinalLetra.setText(_tr(estado_final.letra))
        self.GWOpcionesD.txtFinalColor.setText(estado_final.color)
        # --------------------------------------------------------------------

        # Estado Inicial
        estado_inicial = self._opciones["tipos_estados"][TIPOESTADO.INICIAL]
        self.GWOpcionesD.txtInicialNombre.setText(_tr(estado_inicial.nombre))
        self.GWOpcionesD.txtInicialLetra.setText(_tr(estado_inicial.letra))
        self.GWOpcionesD.txtInicialColor.setText(estado_inicial.color)
        # --------------------------------------------------------------------

        self.update_recom_final()

        self.GWOpcionesD.sbFinalRecompensa.setValue(estado_final.recompensa)

        estado_size = self._opciones["item"]["size"]
        self.GWOpcionesD.sbGWEstadoSize.setValue(estado_size)

        ent_show_state = self._opciones["gw"]["entrenamiento"]["actual_state"]["show"]
        rec_show_state = self._opciones["gw"]["recorrido"]["actual_state"]["show"]
        self.GWOpcionesD.gbEntShowActualState.setChecked(ent_show_state)
        self.GWOpcionesD.gbRecShowActualState.setChecked(rec_show_state)

        ent_icono = self._opciones["gw"]["entrenamiento"]["actual_state"]["icono"]
        rec_icono = self._opciones["gw"]["recorrido"]["actual_state"]["icono"]

        if ent_icono is None:
            self.GWOpcionesD.optEntMostrarColorFondo.setChecked(True)
        else:
            self.GWOpcionesD.optEntMostrarIcono.setChecked(True)

        if rec_icono is None:
            self.GWOpcionesD.optRecMostrarColorFondo.setChecked(True)
        else:
            self.GWOpcionesD.optRecMostrarIcono.setChecked(True)

    def _set_dialog_signals(self):
        u"""
        Establece y conecta las señales de Qt entre los diversos widgets.
        """
        self.GWOpcionesD.sbExcelenteRecompensa.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbBuenoRecompensa.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbMaloRecompensa.valueChanged.connect(self.update_recom_final)
        self.GWOpcionesD.sbNeutroRecompensa.valueChanged.connect(self.update_recom_final)

        clr_agente = lambda: self.set_color_estado(self.GWOpcionesD.txtAgenteColor)
        clr_bueno = lambda: self.set_color_estado(self.GWOpcionesD.txtBuenoColor)
        clr_excelente = lambda: self.set_color_estado(self.GWOpcionesD.txtExcelenteColor)
        clr_malo = lambda: self.set_color_estado(self.GWOpcionesD.txtMaloColor)
        clr_inicial = lambda: self.set_color_estado(self.GWOpcionesD.txtInicialColor)
        clr_final = lambda: self.set_color_estado(self.GWOpcionesD.txtFinalColor)
        clr_pared = lambda: self.set_color_estado(self.GWOpcionesD.txtParedColor)
        clr_neutro = lambda: self.set_color_estado(self.GWOpcionesD.txtNeutroColor)

        self.GWOpcionesD.btnElegirColorAgente.clicked.connect(clr_agente)
        self.GWOpcionesD.btnElegirColorBueno.clicked.connect(clr_bueno)
        self.GWOpcionesD.btnElegirColorExcelente.clicked.connect(clr_excelente)
        self.GWOpcionesD.btnElegirColorFinal.clicked.connect(clr_final)
        self.GWOpcionesD.btnElegirColorInicial.clicked.connect(clr_inicial)
        self.GWOpcionesD.btnElegirColorMalo.clicked.connect(clr_malo)
        self.GWOpcionesD.btnElegirColorNeutro.clicked.connect(clr_neutro)
        self.GWOpcionesD.btnElegirColorPared.clicked.connect(clr_pared)

    def update_recom_final(self, valor=None):
        u"""
        Calcula la recompensa del Estado Final en función de las recompensas
        del resto de los tipos de estados.

        :param valor: Valor númerico del control seleccionado.
        """
        self.recomp_max = max([self.GWOpcionesD.sbExcelenteRecompensa.value(),
                               self.GWOpcionesD.sbBuenoRecompensa.value(),
                               self.GWOpcionesD.sbMaloRecompensa.value(),
                               self.GWOpcionesD.sbNeutroRecompensa.value()])
        self.recomp_max += 100

        if self._opciones["gw"]["entrenamiento"]["recompfinalauto"]:
            estado = self._opciones["tipos_estados"][TIPOESTADO.FINAL]
            self.GWOpcionesD.sbFinalRecompensa.setMinimum(estado.recompensa)
        else:
            self.GWOpcionesD.sbFinalRecompensa.setMinimum(self.recomp_max)

    def set_color_estado(self, widget):
        u"""
        Selecciona y establece el nombre del color para un tipo de estado dado.

        :param widget: Widget en el cual se mostrará el nombre del color.
        """
        qcolordiag = QtGui.QColorDialog(self)
        qcolordiag.setOption(QtGui.QColorDialog.ShowAlphaChannel)
        state_color = qcolordiag.getColor()

        if state_color.isValid():
            try:
                widget.setText(str(state_color.name()).upper())
            except AttributeError:
                pass

    def accept(self):
        u"""
        Aceptar y enviar los cambios producidos en el diálogo.
        """
        self.estado_size = self.GWOpcionesD.sbGWEstadoSize.value()
        self.recomp_final = self.GWOpcionesD.sbFinalRecompensa.value()
        self.recomp_excelente = self.GWOpcionesD.sbExcelenteRecompensa.value()
        self.recomp_bueno = self.GWOpcionesD.sbBuenoRecompensa.value()
        self.recomp_malo = self.GWOpcionesD.sbMaloRecompensa.value()
        self.recomp_neutro = self.GWOpcionesD.sbNeutroRecompensa.value()
        self.ent_show_state = self.GWOpcionesD.gbEntShowActualState.isChecked()
        self.ent_usar_color_fondo = self.GWOpcionesD.optEntMostrarColorFondo.isChecked()
        self.ent_usar_icono = self.GWOpcionesD.optEntMostrarIcono.isChecked()
        self.rec_show_state = self.GWOpcionesD.gbRecShowActualState.isChecked()
        self.rec_usar_color_fondo = self.GWOpcionesD.optRecMostrarColorFondo.isChecked()
        self.rec_usar_icono = self.GWOpcionesD.optRecMostrarIcono.isChecked()

        tipos_estados = {}

        # Estado Agente
        recompensa_agente = None
        nombre_agente = self.GWOpcionesD.txtAgenteNombre.text()
        letra_agente = self.GWOpcionesD.txtAgenteLetra.text()
        color_agente = self.GWOpcionesD.txtAgenteColor.text()
        icono_agente = QtGui.QIcon(QtGui.QPixmap(":/iconos/Agente_1.png"))

        tipos_estados[TIPOESTADO.AGENTE] = TipoEstado(TIPOESTADO.AGENTE,
                                                      recompensa_agente,
                                                      nombre_agente,
                                                      letra_agente,
                                                      color_agente,
                                                      icono_agente)

        # Estado Excelente
        recompensa_excelente = self.GWOpcionesD.sbExcelenteRecompensa.value()
        nombre_excelente = self.GWOpcionesD.txtExcelenteNombre.text()
        letra_excelente = self.GWOpcionesD.txtExcelenteLetra.text()
        color_excelente = self.GWOpcionesD.txtExcelenteColor.text()
        icono_excelente = None

        tipos_estados[TIPOESTADO.EXCELENTE] = TipoEstado(TIPOESTADO.EXCELENTE,
                                                         recompensa_excelente,
                                                         nombre_excelente,
                                                         letra_excelente,
                                                         color_excelente,
                                                         icono_excelente)

        # Estado Bueno
        recompensa_bueno = self.GWOpcionesD.sbBuenoRecompensa.value()
        nombre_bueno = self.GWOpcionesD.txtBuenoNombre.text()
        letra_bueno = self.GWOpcionesD.txtBuenoLetra.text()
        color_bueno = self.GWOpcionesD.txtBuenoColor.text()
        icono_bueno = None

        tipos_estados[TIPOESTADO.BUENO] = TipoEstado(TIPOESTADO.BUENO,
                                                    recompensa_bueno,
                                                    nombre_bueno,
                                                    letra_bueno,
                                                    color_bueno,
                                                    icono_bueno)

        # Estado Malo
        recompensa_malo = self.GWOpcionesD.sbMaloRecompensa.value()
        nombre_malo = self.GWOpcionesD.txtMaloNombre.text()
        letra_malo = self.GWOpcionesD.txtMaloLetra.text()
        color_malo = self.GWOpcionesD.txtMaloColor.text()
        icono_malo = None

        tipos_estados[TIPOESTADO.MALO] = TipoEstado(TIPOESTADO.MALO,
                                                    recompensa_malo,
                                                    nombre_malo,
                                                    letra_malo,
                                                    color_malo,
                                                    icono_malo)

        # Estado Neutro
        recompensa_neutro = self.GWOpcionesD.sbNeutroRecompensa.value()
        nombre_neutro = self.GWOpcionesD.txtNeutroNombre.text()
        letra_neutro = self.GWOpcionesD.txtNeutroLetra.text()
        color_neutro = self.GWOpcionesD.txtNeutroColor.text()
        icono_neutro = None

        tipos_estados[TIPOESTADO.NEUTRO] = TipoEstado(TIPOESTADO.NEUTRO,
                                                      recompensa_neutro,
                                                      nombre_neutro,
                                                      letra_neutro,
                                                      color_neutro,
                                                      icono_neutro)

        # Estado Pared
        recompensa_pared = None
        nombre_pared = self.GWOpcionesD.txtParedNombre.text()
        letra_pared = self.GWOpcionesD.txtParedLetra.text()
        color_pared = self.GWOpcionesD.txtParedColor.text()
        icono_pared = None

        tipos_estados[TIPOESTADO.PARED] = TipoEstado(TIPOESTADO.PARED,
                                                           recompensa_pared,
                                                           nombre_pared,
                                                           letra_pared,
                                                           color_pared,
                                                           icono_pared)

        # Estado Inicial
        recompensa_inicial = None
        nombre_inicial = self.GWOpcionesD.txtInicialNombre.text()
        letra_inicial = self.GWOpcionesD.txtInicialLetra.text()
        color_inicial = self.GWOpcionesD.txtInicialColor.text()
        icono_inicial = None

        tipos_estados[TIPOESTADO.INICIAL] = TipoEstado(TIPOESTADO.INICIAL,
                                                       recompensa_inicial,
                                                       nombre_inicial,
                                                       letra_inicial,
                                                       color_inicial,
                                                       icono_inicial)

        # Estado Final
        recompensa_final = self.GWOpcionesD.sbFinalRecompensa.value()
        nombre_final = self.GWOpcionesD.txtFinalNombre.text()
        letra_final = self.GWOpcionesD.txtFinalLetra.text()
        color_final = self.GWOpcionesD.txtFinalColor.text()
        icono_final = None

        tipos_estados[TIPOESTADO.FINAL] = TipoEstado(TIPOESTADO.FINAL,
                                                           recompensa_final,
                                                           nombre_final,
                                                           letra_final,
                                                           color_final,
                                                           icono_final)

        self.tipos_estados = tipos_estados

        # Guardar valores y cerrar cuadro de diálogo
        super(GWOpcionesDialog, self).accept()

    def reject(self):
        u"""
        Cancelar cambios del diálogo.
        """
        super(GWOpcionesDialog, self).reject()

    def get_opciones(self):
        return self._opciones

    def set_opciones(self, opciones):
        self._opciones = opciones

    opciones = property(get_opciones, set_opciones, None, "Opciones de la aplicación")
