# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sys
import json
import codecs
import pickle
import urllib
import os
import datetime

import imagefactory
from logger import logger
from scrapy import log

from gallary import Gallary
import func
import traceback
import pymongo
import db

class DmozPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        db.save(dict(item))
        return item
