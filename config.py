# -*- coding: utf-8 -*-
"""MySQL配置信息"""
USERNAME = 'root'   # MySQL用户名
PASSWORD = '123456'     # MySQL用户密码
HOST = 'localhost'  # MySQL数据库IP地址
PORT = 3306     # 端口号
DB = 'demo'     # MySQL数据库名
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'    # 调用DBAPI
# gap = 15    # 每份数据时间长度，以分钟为单位
id_max = 3    # 数据包含地铁站总数
