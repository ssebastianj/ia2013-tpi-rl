#-------------------------------------------------
#
# Project created by QtCreator 2013-03-28T16:02:52
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = IA2013TPIRLGUI
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    genrndvalsdialog.cpp \
    aboutdialog.cpp \
    gwgenrndestadosdialog.cpp \
    gwopcionesdialog.cpp \
    matrizdialog.cpp \
    codetailsdialog.cpp

HEADERS  += mainwindow.h \
    genrndvalsdialog.h \
    aboutdialog.h \
    gwgenrndestadosdialog.h \
    gwopcionesdialog.h \
    matrizdialog.h \
    codetailsdialog.h

FORMS    += mainwindow.ui \
    aboutdialog.ui \
    gwgenrndestadosdialog.ui \
    gwopcionesdialog.ui \
    matrizdialog.ui \
    codetailsdialog.ui

TRANSLATIONS += EN-US

RESOURCES += \
    recursos.qrc
