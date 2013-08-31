# -*- coding: utf-8 -*-
# Scrapy settings for dmoz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/0.12/topics/settings.html#std:setting-RANDOMIZE_DOWNLOAD_DELAY
#
from scrapy.settings.default_settings import DOWNLOAD_DELAY

BOT_NAME = 'ppt'
BOT_VERSION = '1.2'

SPIDER_MODULES = ['dmoz.spiders']
NEWSPIDER_MODULE = 'dmoz.spiders'
DEFAULT_ITEM_CLASS = 'dmoz.items.DmozItem'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
ITEM_PIPELINES = [
'dmoz.pipelines.DmozPipeline',
]

#下载延迟
DOWNLOAD_DELAY = 20
#下载延迟采用随机数， between 0.5 and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
#不允许转向
REDIRECT_MAX_TIMES=5
#同时放出的蜘蛛数
CONCURRENT_SPIDERS=1 #默认8
#每个蜘蛛最大同时发出的request数
CONCURRENT_REQUESTS_PER_SPIDER=1#默认8
COOKIES_DEBUG=True


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'dmoz.middlewares.ProxyMiddleware': 100,
}


