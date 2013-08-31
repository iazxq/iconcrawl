# -*- coding: utf-8 -*-
import win32com
from win32com.client import Dispatch, constants
import win32con
import win32gui
import os

def TestPPT():
    ppt = win32com.client.DispatchEx('PowerPoint.Application')
    ppt.WindowState = 2
    ppt.Visible =True
    hwnd = win32gui.FindWindow(None, "Microsoft PowerPoint")

    win32gui.ShowWindow(hwnd, win32con.SW_HIDE) # Hide via Win32Api

    Presentation = ppt.Presentations.Open('c:/1.ppt')
    Presentation.Slides[1].Export("C:/1.jpg", "JPG", 800, 600)

    #ppt.Visible = False
    print("end")

if __name__=='__main__':
    TestPPT()