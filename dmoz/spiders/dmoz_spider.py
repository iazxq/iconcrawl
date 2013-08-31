# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.item import Item
from scrapy.http import Request
from dmoz.items import DmozItem
from urlparse import urljoin
import re
import time
from dmoz import func
import os
import simplejson
import urllib
import os
import ppt
from dmoz import db

from dmoz.logger import logger
import socket
import traceback
import random
import datetime

import g
from watcher import WatcherThread
from bson.objectid import ObjectId
import Image


def signal_handler(signum, frame):
    raise Exception("Timed out!")


class DmozSpider(CrawlSpider):
    handle_httpstatus_list = [404]
    name="icon"
    login_page = 'http://findicons.com/accounts/signin'
    #allowed_domains = ['www.sjbz.org']
    start_urls = [login_page]




    def readfile(self):
        url = ''
        if os.path.exists('lasturl.txt'):
            f = open('lasturl.txt','r')
            url = f.read()
            f.close()
        return url

    def writefile(self,url):
        f = open('lasturl.txt','w')
        f.write(url)
        f.close()




    #抓取列表页
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        csrf_name = hxs.select('//input[@name="csrfmiddlewaretoken"]/@value').extract()[0]
        print(csrf_name)
        formdata = {'username': 'iazxq', 'password': 'kkkkkk','csrfmiddlewaretoken':csrf_name,'readed':'on','remember':'on','fromurl':'/'}
        print(formdata)
        return [FormRequest.from_response(response,
                formdata=formdata,
                callback=self.after_login)]

    def after_login(self,response):
        print(response.body[:3000])
        for i in range(1,2):
            url = 'http://findicons.com/pack/%s'%i
            yield Request(url, callback=self.parse_list)




    def parse_list(self,response):
        print(response.body)
        hxs = HtmlXPathSelector(response)
        urlList = hxs.select('//div[@class="pack_pic"]//a/@href').extract()

        for url in urlList:
            item = DmozItem()
            item['_id'] =ObjectId()

            url = 'http://findicons.com%s'%url
            meta = {'item':item}
            yield Request(url, callback=self.parse_items,meta=meta)



    #抓取列表页
    def parse_items(self,response):
        print(response.body)
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        detailUrlList = hxs.select('//div[@class="icon_list"]/ul/li/dl/dd/a/@href').extract()
        meta = {'item':item}
        for url in detailUrlList:
            url =  'http://findicons.com%s'%url
            yield Request(url, callback=self.parse_detail,meta=meta)
        #查看是否有下一页
        nextUrlList= hxs.select('//a[contains(text(),"Next")]/@href').extract()
        if nextUrlList:
            nextUrl = nextUrlList[-1]
            nextUrl = 'http://findicons.com%s'%nextUrl
            yield Request(nextUrl, callback=self.parse_items,meta=meta)

    def parse_detail(self,response):

        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        iconUrls = hxs.select('//ul[@class="other-size"]/li/a/img/@src').extract()

        if iconUrls:
            iconUrl = iconUrls[0]
            print('iconUrl=%s'%iconUrl)
            upDir =  'up/' + func.get_new_upload_dir()
            if not os.path.exists(upDir):
                os.makedirs(upDir)
            newFile = upDir + func.get_new_filename(iconUrl)
            urllib.urlretrieve(iconUrl,newFile)
            image = Image.open(newFile)
            size = image.size
            tags = hxs.select('//p[@class="tag_btn"]/a/@title').extract()
            if not item.has_key('pics'):
                item['pics'] = []
            item['pics'].append({'url':newFile,'size':size,'tags':tags})
            pack = hxs.select('//ul[@class="detial_list left"]/li[1]/span/a/text()').extract()[0]
            author = hxs.select('//ul[@class="detial_list left"]/li[2]/span/a/text()').extract()[0]
            authorLink = hxs.select('//ul[@class="detial_list left"]/li[2]/span/a/@href').extract()[0]
            item['pack'] = pack
            item['author'] = {'name':author,'link':authorLink}
            yield item






SPIDER = DmozSpider()


