# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

if __name__ == '__main__':
    setup(
           options={
                "py2exe":{
                "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"]
            }},
          windows=[{'script':'main_widget.py'}])
