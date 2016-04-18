#! /bin/env python

import ctypes as C
try:
    # bin_SX7
    TFC = C.WinDLL( r"D:\HiDTV\SVP_FUSION\Bin_SX7\TFCAPI.dll" )
except:
    # bin_FRCXB
    TFC = C.WinDLL( r"D:\HiDTV\SVP_FUSION\Bin_FRCXB\TFCAPI.dll" )


def Cfunc(fcn, argin, argout=None):
    ret = fcn
    ret.argtypes = argin
    if argout != None:
        ret.restype = argout
    return ret

BYTE = C.c_byte
WORD = C.c_uint16
DWORD = C.c_uint32

TFCConnect2Chip = Cfunc(TFC.tfcConnInit,None,C.c_bool)
tfcConnTerm = Cfunc(TFC.tfcConnTerm, None, None)
tfcConnReinit = Cfunc(TFC.tfcConnReinit,None,C.c_bool)
TFC.tfcGetVersion = Cfunc(TFC.tfcGetVersion,(C.POINTER(C.c_int32),C.POINTER(C.c_int32)))
def tfcGetVersion():
    ma = C.c_long();
    mi = C.c_long();
    if TFC.tfcGetVersion(ma,mi):
        ver = "%i.%i" % (ma.value,mi.value)
    else:
        ver = "error!"


#------TFCAPI basic function TFCReg.h-----------
TFC.tfcWriteByte = Cfunc(TFC.tfcWriteByte,(DWORD,BYTE,BYTE))
def tfcWriteByte(page,reg,val):
    TFC.tfcWriteByte(page,reg,val)

TFC.tfcWriteDword = Cfunc(TFC.tfcWriteDword,(DWORD,BYTE,DWORD))
def tfcWriteDword(page,reg,val):
    TFC.tfcWrigeDword(page,reg,val)

TFC.tfcWriteDwordMask = Cfunc(TFC.tfcWriteDwordMask,(DWORD,BYTE,DWORD,DWORD))
def tfcWriteDword(page,reg,mask,val):
    TFC.tfcWrigeDword(page,reg,mask,val)

TFC.tfcReadDword = Cfunc(TFC.tfcReadDword,(DWORD,BYTE),(DWORD))
def tfcReadDword(page,reg):
    return TFC.tfcWrigeDword(DWORD(page),BYTE(reg))

if __name__ == "__main__":
    print("Version: %s" % tfcGetVersion())

    r =TFCConnect2Chip()
    if r:
        print("connect to chip")
        a = TFC.tfcReadDword(0x198A0000,0xC0);
        print("c0: %x" % a)
