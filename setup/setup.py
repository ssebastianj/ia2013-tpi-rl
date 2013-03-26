#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import subprocess
import sys
import os

def main():
    # Compile UI files
    print '\n---------------------- Compile IU Files ---------------------'
    compile_ui_path = os.path.join(os.pardir, 'compile_ui.py')
    comp_ui_args = [sys.executable, compile_ui_path]
    subprocess.call(comp_ui_args)

    # Generate Version Info
    print '\n------------------- Generate Version Info -------------------'
    vi_gen_path = os.path.abspath(os.path.join(os.curdir, 'version_info.py'))
    vi_gen_args = [sys.executable, vi_gen_path]
    subprocess.call(vi_gen_args)

    vi_txt_path = os.path.abspath(os.path.join(os.path.curdir, 'version_info.txt'))
    main_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'ia.pyw'))
    spec_path = os.path.abspath(os.path.join(os.path.curdir, 'spec'))
    icon_path = os.path.abspath(os.path.join(os.path.pardir, 'src', 'img', 'app.ico'))

    # Build EXE
    print '\n--------------------- Build Executable ---------------------'
    args = [sys.executable,
            "C:\\PyInstaller\\pyinstaller.py",
            "--noconfirm",
            "--log-level=DEBUG",
            "--onefile",
            "--onedir",
            "--out=" + spec_path,
            "--name=ia",
            "--windowed",
            "--version-file=" + vi_txt_path,
            "--icon=" + icon_path,
            main_path]

    subprocess.call(args)

    print '\n---------------------- Building Finished ----------------------'

if __name__ == '__main__':
    main()
