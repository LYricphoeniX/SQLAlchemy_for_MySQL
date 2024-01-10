# -*- coding: utf-8 -*-
"""创建引擎，连接数据库，创建ORM模型并映射到数据库"""
from .basic import Traffic, OD, session
from config import id_max
import numpy as np


class OrmOpearator:
    def __init__(self) -> None:
        pass

    def __del__(self):
        pass

    # 快速增加：在某日期时段，某站的进站、出站、换乘人数
    def addtraffic(self, date, time, name, enter, out, trans):
        session.add(Traffic(date=date, time=time, name=name, enter=enter, out=out, trans=trans))
        session.commit()

    def addod(self, date, time, enter, out, value):
        session.add(OD(date=date, time=time, enter=enter, out=out, value=value))
        session.commit()

    # 给定日期、起始时刻和站点id，打印并返回某站某时段的进站、出站、换乘人数的list链表
    def gettraffic(self, date, time, name):
        item_list = session.query(Traffic.enter, Traffic.out, Traffic.trans).filter(
            Traffic.date == date, Traffic.time == time, Traffic.name == name
        )
        for item in item_list:
            return item.enter, item.out, item.trans

    # 给定日期、起始时刻，打印并返回某时段的OD矩阵，行号为进站id，列号为出站id
    def getod(self, date, time):
        matrix = np.zeros((id_max, id_max), dtype=int)
        item_list = session.query(OD.enter, OD.out, OD.value).filter(
            OD.date == date, OD.time == time
        )
        for item in item_list:
            matrix[item.enter, item.out] = item.value
        return matrix

    # 给定日期、起始时刻、修改的项目和数据，并更新该条记录
    def changetraffic(self, date, time, name, enter=None, out=None, trans=None):
        if enter is not None:
            session.query(Traffic).filter(
                Traffic.date == date,
                Traffic.time == time,
                Traffic.name == name
            ).update({
                "enter": enter,
            })
        if out is not None:
            session.query(Traffic).filter(
                Traffic.date == date,
                Traffic.time == time,
                Traffic.name == name
            ).update({
                "out": out,
            })
        if trans is not None:
            session.query(Traffic).filter(
                Traffic.date == date,
                Traffic.time == time,
                Traffic.name == name
            ).update({
                "trans": trans,
            })
            session.commit()

    # 给定日期、时刻、进站id、出站id，新的OD值，会更新新的OD矩阵值
    def changeod(self, date, time, enter, out, value=None):
        if value is not None:
            session.query(OD).filter(
                OD.date == date,
                OD.time == time,
                OD.enter == enter,
                OD.out == out,
            ).update({
                "value": value,
            })
        session.commit()

    # 给定日期、起始时刻和站点id，打印、删除某站某时段的进站、出站、换乘人数
    def ridtraffic(self, date, time, name):
        session.query(Traffic).filter(
            Traffic.date == date, Traffic.time == time, Traffic.name == name
        ).delete()
        session.commit()

    def ridod(self, date, time, enter, out):
        session.query(OD).filter(
            OD.date == date, OD.time == time, OD.enter == enter, OD.out == out
        ).delete()
        session.commit()
