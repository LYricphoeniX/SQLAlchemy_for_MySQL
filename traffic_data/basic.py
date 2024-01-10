# -*- coding: utf-8 -*-
import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, text
from config import DB_URI

engine = create_engine(DB_URI)  # 一个只为特定数据库服务器创建一次的全局对象，充当连接到特定数据库的中心源，提供数据库连接
Base = sqlalchemy.orm.declarative_base()  # SQL.ORM基类，所有的映射类（所有的数据表）都要继承该基类
session = sqlalchemy.orm.sessionmaker(engine)()  # 构建session对象

class Traffic(Base):
    __tablename__ = 'traffic'  # 流量数据表
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)  # 日期
    time = Column(Integer)  # 起始时刻
    name = Column(Integer)  # 站点id
    enter = Column(Integer)  # 进站人数
    out = Column(Integer)  # 出站人数
    trans = Column(Integer)  # 换乘人数


class OD(Base):
    __tablename__ = 'od'  # OD矩阵数据表
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)  # 日期
    time = Column(Integer)  # 起始时刻
    enter = Column(Integer)  # 进站id
    out = Column(Integer)  # 出站id
    value = Column(Integer)  # OD矩阵元素值


Base.metadata.create_all(bind=engine)  # 将模型映射到数据库中，建表
