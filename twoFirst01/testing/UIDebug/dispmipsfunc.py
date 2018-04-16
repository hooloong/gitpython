__author__ = 'hooloongge'

import ctypes as C
from pdb import set_trace
proper_digit="0123456789ABCDEFabcdef"
low_digit="abcdef"


def isproperdigit(strinput):
    if len(strinput) == 0 or len(strinput) > 8:
        return False
    for c in strinput:
        if c not in proper_digit:
            return False
    return True


def islowerdigit(strinput):
    for c in strinput:
        if c in low_digit:
            return True
    return False

import two01 as TFC


DWORD = C.c_uint32




mmapPToVDispMips = (
    (0x00000000, 0x10000000, 1), #region 1
    (0x10000000, 0x50000000, 2), # region 2
    (0x80000000, 0xC0000000, 3), # region 3
    )
mmapVToPDispMips = (
    (0x00000000, 0x40000000, 1), #region 1
    (0x40000000, 0x80000000, 2), # region 2
    (0x80000000, 0x90000000, 3), # region 3
    (0xA0000000, 0xB0000000, 4), # region 4
    )
def VToPFun1(vaddr):
    return vaddr+0x10000000
def VToPFun2(vaddr):
    return vaddr+0x40000000
def VToPFun3(vaddr):
    return vaddr & 0x1FFFFFFF
def mmap_V2P( vaddr ):
    """
    Calculate physical memory address from virtual memory address,
    using memory map 'mmap'
    """
    paddr = 0
    for i, (virtstart,virtend,N) in enumerate(mmapVToPDispMips):
        if vaddr >= virtstart and vaddr < virtend:
            if N == 1:
                paddr = VToPFun1(vaddr)
            if N == 2:
                paddr = VToPFun2(vaddr)
            if N == 3 or N ==4:
                paddr = VToPFun3(vaddr)
            break
    return paddr




if __name__ == "__main__":

    r = TFC.TFCConnect2Chip()
    print("tfcConnInit returns ",r)

    if r:
        TFC.tfcConnTerm()
