# /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys


if sys.platform == 'win32':
    datas = [
             (os.path.abspath(os.path.join(os.curdir, '..', 'src', 'tools', 'taskbar', 'TaskbarLib.dll')), ''),
             (os.path.abspath(os.path.join(os.curdir, '..', 'src', 'tools', 'taskbar', 'TaskbarLib.tlb')), ''),
             (os.path.abspath(os.path.join(os.curdir, '..', 'src', 'tools', 'taskbar', 'TaskbarLib.idl')), ''),
             ]
