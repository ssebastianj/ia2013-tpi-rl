#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

try:
    import comtypes.gen.TaskbarLib as tbl
except ImportError:
    pass


class WindowsTaskBar(object):
    def __init__(self):
        if not is_windows7_or_later():
            raise RuntimeError('Windows Taskbar requires Windows 7 or later')

        # Flags for Setting Taskbar Progress state
        self.TBPF_NOPROGRESS = 0
        self.TBPF_INDETERMINATE = 0x1
        self.TBPF_NORMAL = 0x2
        self.TBPF_ERROR = 0x4
        self.TBPF_PAUSED = 0x8

        # Flags for SetTabActive
        self.TBATF_USEMDITHUMBNAIL = 0x1,
        self.TBATF_USEMDILIVEPREVIEW = 0x2,

        import comtypes.client as cc
        cc.GetModule("TaskbarLib.tlb")

        self._taskbar = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}",
                                        interface=tbl.ITaskbarList3)

    def HrInit(self):
        self._taskbar.HrInit()

    def AddTab(self, hwnd):
        self._taskbar.AddTab(hwnd)

    def DeleteTab(self, hwnd):
        self._taskbar.DeleteTab(hwnd)

    def ActivateTab(self, hwnd):
        self._taskbar.ActivateTab(hwnd)

    def SetActivateAlt(self, hwnd):
        self._taskbar.SetActivateAlt(hwnd)

    def MarkFullscreenWindow(self, hwnd, fullscreen):
        self._taskbar.MarkFullscreenWindow(hwnd, fullscreen)

    def SetProgressValue(self, hwnd, completed, total):
        self._taskbar.SetProgressValue(hwnd, completed, total)

    def SetProgressState(self, hwnd, flags):
        self._taskbar.SetProgressState(hwnd, flags)

    def RegisterTab(self, hwnd_tab, hwnd_mdi):
        self._taskbar.RegisterTab(hwnd_tab, hwnd_mdi)

    def UnregisterTab(self, hwnd_tab):
        self._taskbar.UnregisterTab(hwnd_tab)

    def SetTabOrder(self, hwnd_tab, hwnd_insert_before):
        self._taskbar.SetTabOrder(hwnd_tab, hwnd_insert_before)

    def SetTabActive(self, hwnd_tab, hwnd_mdi, flags):
        self._taskbar.SetTabActive(hwnd_tab, hwnd_mdi, flags)

    def ThumbBarAddButtons(self, hwnd, buttons, button):
        self._taskbar.ThumbBarAddButtons(hwnd, buttons, button)

    def ThumbBarUpdateButtons(self, hwnd, buttons, button):
        self._taskbar.ThumbBarUpdateButtons(hwnd, buttons, button)

    def ThumbBarSetImageList(self, hwnd, h_iml):
        self._taskbar.ThumbBarSetImageList(hwnd, h_iml)

    def SetOverlayIcon(self, hwnd, h_icon, description):
        self._taskbar.SetOverlayIcon(hwnd, h_icon, description)

    def SetThumbnailTooltip(self, hwnd, tip):
        self._taskbar.SetThumbnailTooltip(hwnd, tip)

    def SetThumbnailClip(self, hwnd, clip):
        self._taskbar.SetThumbnailClip(hwnd, clip)


def is_windows7_or_later():
    if sys.platform == 'win32':
        version_info = sys.getwindowsversion()
        return version_info[0] >= 6 and version_info[1] >= 1
    else:
        return False
