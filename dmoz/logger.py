# -*- coding: utf-8 -*-
import logging

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('logs.txt')
fh.setLevel(logging.DEBUG)


# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
  