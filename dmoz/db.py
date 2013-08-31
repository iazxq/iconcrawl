# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import pymongo
conn = pymongo.Connection()
db=conn.icons
collection = db.icons

def save(item):
    collection.save(item)

def exists(link):
    return collection.find_one({'link':link})