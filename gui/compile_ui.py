#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Sebastián J. Seba

import os
from PyQt4 import uic


def main():
    # Directorio desde donde se leerán los archivos .ui generados por QtDesigner
    uiDir = os.path.abspath(os.path.join(os.curdir, 'qt', 'IA-2013-TPI-RL-GUI'))
    # Directorio donde serán almacenados los archivos generados por pyuic
    uiPyDir = os.path.abspath(os.path.join('..', 'src', 'gui', 'qt'))

    def map_dir(py_dir, py_file):
        return (uiPyDir, py_file)

    try:
        print 'Compilando archivos de interfaz gráfica...'
        uic.compileUiDir(uiDir, recurse=True, map=map_dir)
    except Exception as e:
        print 'ERROR: ' + e
    finally:
        print 'Compilación finalizada.'

if __name__ == '__main__':
    main()
