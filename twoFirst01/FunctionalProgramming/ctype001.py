from ctypes import c_int, WINFUNCTYPE, windll
from ctypes.wintypes import HWND, LPCSTR, UINT
prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
paramflags = (1, 'hwnd', 0), (1, 'text', 'Hi'), (1, 'caption', None), (1, 'flags', 0)
MessageBox = prototype(('MessageBoxA', windll.user32), paramflags)
MessageBox(text='Hello world',flags=2)