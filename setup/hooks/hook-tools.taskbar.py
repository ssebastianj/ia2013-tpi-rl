# /usr/bin/env python


import os
import sys


if sys.platform == "win32":
    datas = [
        (
            os.path.abspath(
                os.path.join(
                    os.curdir, "..", "src", "tools", "taskbar", "TaskbarLib.dll"
                )
            ),
            "",
        ),
        (
            os.path.abspath(
                os.path.join(
                    os.curdir, "..", "src", "tools", "taskbar", "TaskbarLib.tlb"
                )
            ),
            "",
        ),
        (
            os.path.abspath(
                os.path.join(
                    os.curdir, "..", "src", "tools", "taskbar", "TaskbarLib.idl"
                )
            ),
            "",
        ),
    ]
