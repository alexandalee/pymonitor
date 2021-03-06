#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
"通过调用API获取进程列表"
 
import sys;
import ctypes;
 
__metaclass__ = type;
 
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",ctypes.c_ulong),
        ("cntUsage",ctypes.c_ulong),
        ("th32ProcessID",ctypes.c_ulong),
        ("th32DefaultHeapID",ctypes.c_void_p),
        ("th32ModuleID",ctypes.c_ulong),
        ("cntThreads",ctypes.c_ulong),
        ("th32ParentProcessID",ctypes.c_ulong),
        ("pcPriClassBase",ctypes.c_long),
        ("dwFlags",ctypes.c_ulong),
        ("szExeFile",ctypes.c_char*260)
    ]
 
kernel32 = ctypes.windll.LoadLibrary("kernel32.dll");
pHandle = kernel32.CreateToolhelp32Snapshot(0x2,0x0);

if pHandle==-1:sys.exit()
 
proc = PROCESSENTRY32();
proc.dwSize = ctypes.sizeof(proc);
 
while kernel32.Process32Next(pHandle,ctypes.byref(proc)):
    print("ProcessName : %s - ProcessID : %d"%(ctypes.string_at(proc.szExeFile),proc.th32ProcessID));
kernel32.CloseHandle(pHandle);