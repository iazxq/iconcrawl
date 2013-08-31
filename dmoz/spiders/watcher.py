# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import threading
import time
import datetime
import g

class WatcherThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        print('start watcher powerpoint...')
        while True:
            seconds =(datetime.datetime.now()-g.LastActiveTime).seconds
            if seconds >300:
                print('ppt open over %s seconds,kill it!'%seconds)
                g.LastActiveTime = datetime.datetime.now()
                import os
                command = 'taskkill /F /IM POWERPNT.EXE' #比如杀死QQ进程
                os.system(command)
            time.sleep(5)


if __name__=='__main__':
    thread = WatcherThread()

    thread.start()