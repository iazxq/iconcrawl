# -*- coding: utf-8 -*-
import win32com
from win32com.client import Dispatch, constants
from dmoz import func
import os
from multiprocessing import Pool, Process, cpu_count,Queue
import time


def TestPPT():
    ppt = win32com.client.Dispatch('PowerPoint.Application')

    pptSel = ppt.Presentations.Open('c:/1.ppt',ReadOnly=1, Untitled=0, WithWindow=0)
    win32com.client.gencache.EnsureDispatch('PowerPoint.Application')
    slide_count = pptSel.Slides.Count
    ppt.Quit()
    print(slide_count)

    #ppt.Visible = False
    print("end")



def GetInfo(pptFile,upDir):
    content = ''
    pics = list()
    ppt = win32com.client.Dispatch('PowerPoint.Application')
    try:

        ppt.WindowState = 2
        #ppt.Visible = True
        pptSel = ppt.Presentations.Open(pptFile,ReadOnly=1, Untitled=0, WithWindow=0)
        win32com.client.gencache.EnsureDispatch('PowerPoint.Application')
        slide_count = pptSel.Slides.Count

        #创建图片目录
        if not os.path.exists(upDir):
            os.makedirs(upDir)

        for i in range(1,slide_count + 1):
            shape_count = pptSel.Slides(i).Shapes.Count
            picFile = os.path.join(upDir,func.get_new_filename('test.jpg')).replace('\\','/')
            realFile = os.path.join(os.getcwd(),picFile).replace('\\','/')
            pptSel.Slides(i).Export(realFile, "JPG", 800, 600)
            pics.append(picFile)
            for j in range(1,shape_count + 1):
                if pptSel.Slides(i).Shapes(j).HasTextFrame:
                    s = pptSel.Slides(i).Shapes(j).TextFrame.TextRange.Text
                    content = ''.join((content,s+"\n"))
    finally:
        ppt.Quit()

    return (content,pics)



def GetInfoP(pptFile,upDir,q):
    try:
        ppool = Pool(processes=cpu_count() )
        info = ppool.apply_async(GetInfo, [pptFile,upDir])
        q.put(info.get(timeout=300))
    except:
        q.put(('',[]))
        
def GetInfoWrap(pptFile,upDir):
    q=Queue()
    p = Process(target=GetInfoP, args=(pptFile,upDir,q))
    p.start()
    p.join()
    result = q.get()
    print(result)
    return q.get()

if __name__=='__main__':
    print(GetInfoWrap('c:/1.ppt','c:/temp'))