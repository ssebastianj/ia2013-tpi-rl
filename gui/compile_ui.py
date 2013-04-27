#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Sebastián J. Seba

import os
import subprocess
from PyQt4 import uic


def main():
    # Directorio desde donde se leerán los archivos .ui generados por QtDesigner
    uiDir = os.path.abspath(os.path.join(os.curdir, 'qt', 'IA2013TPIRLGUI'))
    # Directorio donde serán almacenados los archivos generados por pyuic
    uiPyDir = os.path.abspath(os.path.join('..', 'src', 'gui', 'qtgen'))
    qrcDir = os.path.abspath(os.path.join(os.curdir, 'qt', 'IA2013TPIRLGUI'))
    qrcPyDir = uiPyDir

    def map_dir(py_dir, py_file):
        print py_file
        return (uiPyDir, py_file)

    try:
        print 'Compilando archivos de interfaz gráfica...'
        uic.compileUiDir(uiDir, recurse=True, map=map_dir)
    except Exception as e:
        print 'ERROR: ' + str(e)
    finally:
        print 'Compilación finalizada.'

    args = ["pyrcc4", os.path.join(qrcDir, "recursos.qrc"), "-o", os.path.join(qrcPyDir, "recursos_rc.py")]
    process = subprocess.Popen(args)
    process.communicate()

if __name__ == '__main__':
    main()
