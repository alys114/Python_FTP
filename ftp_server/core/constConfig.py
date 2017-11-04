# Author: Vincent.chan
# Blog: http://blog.alys114.com

import os

##获取当前根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 数据库相关
DB_PATH = BASE_DIR + os.sep + "db" + os.sep
# DATA_BASE_DIR = BASE_DIR + os.sep + "data" + os.sep
USER_FILE_DIR = 'data'+os.sep

USER_DB = DB_PATH + "user.txt"

#
# info_width = 40
# menu_width = 20
# center_width = 90