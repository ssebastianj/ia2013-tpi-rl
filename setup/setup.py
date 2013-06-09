#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import platform
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))
from info import app_info

def main():
    # Build documentation
    msg_1 = u'\n---------------------- Generar Documentación ---------------------'
    print msg_1.encode('ascii', 'ignore')

    doc_builder = "make"
    doc_build_path = os.path.abspath(os.path.join('..', 'docs'))
    full_path = os.path.join(doc_build_path, doc_builder)
    # Clean
    args = [full_path, "clean"]
    process = subprocess.Popen(args, cwd=doc_build_path, shell=True)
    process.communicate()
    # Build
    args = [full_path, "html"]
    process = subprocess.Popen(args, cwd=doc_build_path, shell=True)
    process.communicate()

    # Compile UI files
    msg_2 = u'\n---------------------- Compilar archivos de interfaz grafica ---------------------'
    print msg_2.encode('ascii', 'ignore')

    compile_ui_path = os.path.join('..', 'gui', 'compile_ui.py')
    comp_ui_args = [sys.executable, compile_ui_path]
    subprocess.call(comp_ui_args)

    # Generate Version Info
    msg_3 = u'\n------------------- Generar informacion de version -------------------'
    print msg_3.encode('ascii', 'ignore')

    vi_gen_path = os.path.abspath(os.path.join(os.curdir, 'version_info.py'))
    vi_gen_args = [sys.executable, vi_gen_path]
    subprocess.call(vi_gen_args)

    vi_txt_path = os.path.abspath(os.path.join(os.path.curdir, 'version_info.txt'))
    main_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'ia.pyw'))
    spec_path = os.path.abspath(os.path.join(os.path.curdir, 'spec'))
    icon_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'img', 'UTN.ico'))

    folder_name = "IA-{0}-{1}".format(app_info.__version__, platform.machine())
    dist_path = os.path.abspath(os.path.join(os.path.curdir, 'dist', folder_name))
    hooks_dir = os.path.abspath(os.path.join(os.path.curdir, 'hooks'))

    # Build EXE
    msg_4 = u'\n--------------------- Generar archivo ejecutable ---------------------'
    print msg_4.encode('ascii', 'ignore')

    args = [sys.executable,
            "C:\\PyInstaller\\pyinstaller.py",
            "--noconfirm",
            "--clean",
            "--log-level=DEBUG",
           # "--onefile",
            "--noupx",
            "--onedir",
            "--additional-hooks-dir=" + hooks_dir,
            "--distpath=" + dist_path,
            "--specpath=" + spec_path,
            "--name=ia",
            "--windowed",
            "--version-file=" + vi_txt_path,
            "--icon=" + icon_path,
            main_path]
    subprocess.call(args)

    msg_5 = u'\n---------------------- Generacion de componentes finalizada ----------------------'
    print msg_5.encode('ascii', 'ignore')

    msg_6 = u'\n---------------------- Crear archivo comprimido ----------------------'
    print msg_6.encode('ascii', 'ignore')

if __name__ == '__main__':
    main()
