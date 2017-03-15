#! /bin/env python

import ctypes as C
try:
    # bin_SX7
    print "SX7"
    BASIC_PAGE = 0x19A00400
    SREG_LOG_DEBUG = 0x19A005C0
    SBIT_LOG_DEBUG = 0x00000003
    SREG_MEM_ADDR = 0x19A005C4
    SREG_MEM_WRITEINDEX = 0x19A005C8 # [15:0] count; [31:16] size, unit byte;
    #TFC = C.WinDLL( r"D:\HiDTV\SVP_FUSION\Bin_SX7\TFCAPI.dll" )
    TFC = C.WinDLL( r"..\TFCAPI.dll" )
except:
    # bin_FRCXB
    print "FRCXB"
    BASIC_PAGE = 0x198A0000

    SREG_LOG_DEBUG = 0x19B0028C
    SBIT_LOG_DEBUG = 0x00000200
    SREG_MEM_ADDR = 0x19D00284
    SREG_MEM_WRITEINDEX = 0x19D0028C  # [15:0] count; [31:16] size, unit byte;
    TFC = C.WinDLL( r"TFCAPI.dll" )


def Cfunc(fcn, argin, argout=None):
    ret = fcn
    ret.argtypes = argin
    if argout != None:
        ret.restype = argout
    return ret

BYTE_P = C.c_char_p
VOID_P = C.c_void_p

BYTE = C.c_byte
WORD = C.c_uint16
DWORD = C.c_uint32

TFCConnect2Chip = Cfunc(TFC.tfcConnInit,None,C.c_bool)
tfcConnTerm = Cfunc(TFC.tfcConnTerm, None, None)
tfcConnReinit = Cfunc(TFC.tfcConnReinit,None,C.c_bool)
TFC.tfcGetVersion = Cfunc(TFC.tfcGetVersion,(C.POINTER(C.c_int32),C.POINTER(C.c_int32)))
TFCReadDwordP =  Cfunc(TFC.tfcReadDword,(C.c_uint32 , C.c_byte),C.c_uint32)
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
    TFC.tfcWriteDword(page,reg,val)

def tfc2ddWriteDword(reg,val):
    """

    :rtype: object
    """
    TFC.tfcWriteDword(BASIC_PAGE,reg,val)

TFC.tfcWriteDwordMask = Cfunc(TFC.tfcWriteDwordMask,(DWORD,BYTE,DWORD,DWORD))

def tfcWriteDwordMask(page,reg,mask,val):
    TFC.tfcWriteDwordMask(page,reg,mask,val)

TFC.tfcReadDword = Cfunc(TFC.tfcReadDword,(DWORD,BYTE),(DWORD))
def tfcReadDword(page,reg):
    return TFC.tfcReadDword(DWORD(page),BYTE(reg))
def tfc2ddReadDword(reg):
    return TFC.tfcReadDword(BASIC_PAGE,BYTE(reg))

TFC.tfcReadFB = Cfunc(TFC.tfcReadFB, (DWORD, WORD, BYTE_P))
def tfcReadFB(addr, cnt, pVal):
    TFC.tfcReadFB(DWORD(addr), WORD(cnt),pVal)

TFC.tfcReadMemDword = Cfunc(TFC.tfcReadMemDword, (DWORD, ), (DWORD))
def tfcReadMemDword(addr):
    return TFC.tfcReadMemDword(DWORD(addr))

if __name__ == "__main__":
    print("Version: %s" % tfcGetVersion())

    r =TFCConnect2Chip()
    if r:
        print("connect to chip")
        a = TFC.tfcReadDword(BASIC_PAGE,0xC0);
        print("c0: %x" % a)
