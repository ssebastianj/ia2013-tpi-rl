#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import subprocess
import sys
import os

def main():
    # Build documentation
    msg_1 = u'\n---------------------- Generar Documentación ---------------------'
    msg_1 = msg_1.encode('ascii', 'ignore')
    print msg_1

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
    msg_2 = msg_2.encode('ascii', 'ignore')
    print msg_2

    compile_ui_path = os.path.join('..', 'gui', 'compile_ui.py')
    comp_ui_args = [sys.executable, compile_ui_path]
    subprocess.call(comp_ui_args)

    # Generate Version Info
    msg_3 = u'\n------------------- Generar informacion de version -------------------'
    msg_3 = msg_3.encode('ascii', 'ignore')
    print msg_3

    vi_gen_path = os.path.abspath(os.path.join(os.curdir, 'version_info.py'))
    vi_gen_args = [sys.executable, vi_gen_path]
    subprocess.call(vi_gen_args)

    vi_txt_path = os.path.abspath(os.path.join(os.path.curdir, 'version_info.txt'))
    main_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'ia.pyw'))
    spec_path = os.path.abspath(os.path.join(os.path.curdir, 'spec'))
    icon_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'img', 'app.ico'))
    dist_path = os.path.abspath(os.path.join(os.path.curdir, 'dist'))

    # Build EXE
    msg_4 = u'\n--------------------- Generar archivo ejecutable ---------------------'
    msg_4 = msg_4.encode('ascii', 'ignore')
    print msg_4

    args = [sys.executable,
            "C:\\PyInstaller\\pyinstaller.py",
            "--noconfirm",
            "--clean",
            "--log-level=DEBUG",
           # "--onefile",
           # "--noupx",
            "--onedir",
            "--distpath=" + dist_path,
            "--specpath=" + spec_path,
            "--name=ia",
            "--windowed",
            "--version-file=" + vi_txt_path,
            "--icon=" + icon_path,
            main_path]
    subprocess.call(args)

    msg_5 = u'\n---------------------- Generacion de componentes finalizada ----------------------'
    msg_5 = msg_5.encode('ascii', 'ignore')
    print msg_5

if __name__ == '__main__':
    main()
