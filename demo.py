# -*- coding: utf-8 -*-
"""创建引擎，连接数据库，创建ORM模型并映射到数据库"""
import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, text
from config import DB_URI, gap, id_max
import numpy as np

engine = create_engine(DB_URI)
Base = sqlalchemy.orm.declarative_base()  # SQL.ORM基类
session = sqlalchemy.orm.sessionmaker(engine)()  # 构建session对象


class Traffic(Base):
    __tablename__ = 'traffic'  # 流量数据表
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)  # 日期
    time = Column(Integer)  # 起始时刻
    #    name = Column(String(60))   # 站点名，可选
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


# 快速增加：在某日期时段，某站的进站、出站、换乘人数
def addtraffic(date, time, name, enter, out, trans):
    session.add(Traffic(date=date, time=time, name=name, enter=enter, out=out, trans=trans))
    session.commit()
    # print(f'输入数据已添加')


def addod(date, time, enter, out, value):
    session.add(OD(date=date, time=time, enter=enter, out=out, value=value))
    session.commit()
    # print(f'输入数据已添加')


# 给定日期、起始时刻和站点id，打印并返回某站某时段的进站、出站、换乘人数的list链表
def gettraffic(date, time, name):
    item_list = session.query(Traffic.enter, Traffic.out, Traffic.trans).filter(
        Traffic.date == date, Traffic.time == time, Traffic.name == name
    )
    for item in item_list:
        # print(f'从{date} {time}起{gap}分钟内，站点 {name} 的进站、出站、换乘人次分别为{item.enter} {item.out} {item.trans}')
        return item.enter, item.out, item.trans


# 给定日期、起始时刻，打印并返回某时段的OD矩阵，行号为进站id，列号为出站id
def getod(date, time):
    matrix = np.zeros((id_max, id_max), dtype=int)
    item_list = session.query(OD.enter, OD.out, OD.value).filter(
        OD.date == date, OD.time == time
    )
    for item in item_list:
        matrix[item.enter, item.out] = item.value
        # print(f'{item.enter}, {item.out} = {item.value}')
    return matrix


# 给定日期、起始时刻、修改的项目和数据，并更新该条记录
def changetraffic(date, time, name, enter=None, out=None, trans=None):
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
    # print(f'从{date} {time}起{gap}分钟内，站点 {name} 的进站、出站、换乘人次更新为{enter} {out} {trans}')


# 给定日期、时刻、进站id、出站id，新的OD值，会更新新的OD矩阵值
def changeod(date, time, enter, out, value=None):
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
def ridtraffic(date, time, name):
    '''
    item_list = session.query(Traffic.enter, Traffic.out, Traffic.trans).filter(
        Traffic.date == date, Traffic.time == time, Traffic.name == name
    )
    for item in item_list:
        print(
            f'从{date} {time}起{gap}分钟内，站点 {name} 的进站、出站、换乘人次分别为{item.enter} {item.out} {item.trans}'
            f', 数据将被删除'
        )
    '''
    session.query(Traffic).filter(
        Traffic.date == date, Traffic.time == time, Traffic.name == name
    ).delete()
    session.commit()


# 给定日期、时刻、进站id、出站id，删除对应时段进出站的OD矩阵元素值
def ridod(date, time, enter, out):
    '''
    item_list = session.query(OD.value).filter(
        OD.date == date, OD.time == time, OD.enter == enter, OD.out == out
    )
    for item in item_list:
        print(f'删除{date} {time}起{gap}分钟内，从{enter}到{out}的OD矩阵值{item.value}')
    '''
    session.query(OD).filter(
        OD.date == date, OD.time == time, OD.enter == enter, OD.out == out
    ).delete()
    session.commit()


print(f'添加数据测试')
addtraffic(20240108, 1900, 0, 100, 100, 100)
addtraffic(20240108, 1900, 1, 500, 500, 500)
addtraffic(20240108, 1900, 2, 2000, 2000, 2000)

addod(20240108, 1900, 0, 1, 10)
addod(20240108, 1900, 0, 2, 20)
addod(20240108, 1900, 1, 0, 5)
addod(20240108, 1900, 1, 2, 15)
addod(20240108, 1900, 2, 1, 1)

print(f'查询数据测试')
gettraffic(20240108, 1900, 0)
gettraffic(20240108, 1900, 1)
gettraffic(20240108, 1900, 2)
getod(20240108, 1900)

print(f'修改数据测试')
changetraffic(20240108, 1900, 100, 500, 500, 500)
gettraffic(20240108, 1900, 100)
changetraffic(20240108, 1900, 100, 100, 100, 100)
gettraffic(20240108, 1900, 100)
changeod(20240108, 1900, 0, 1, 100)
getod(20240108, 1900)
changeod(20240108, 1900, 0, 1, 10)
getod(20240108, 1900)

print(f'删除数据测试')
ridtraffic(20240108, 1900, 0)
ridtraffic(20240108, 1900, 1)
ridtraffic(20240108, 1900, 2)
ridod(20240108, 1900, 0, 1)
ridod(20240108, 1900, 0, 2)
ridod(20240108, 1900, 1, 0)
ridod(20240108, 1900, 1, 2)
ridod(20240108, 1900, 2, 1)

# 删除临时测试用的数据表，方便下次测试
session.execute(text("drop table traffic"))
session.execute(text("drop table od"))
session.close()
print(f'测试结束')

'''
item_list = session.query(Traffic).all()  # 获取数据表
print(item_list, f'------------------------------------------------------------------------------\n', f'\n查询数据')
print(f'日期  时刻  站点  进站  出站  换乘')
for item in item_list:
    print(item.date, item.time, item.name, item.enter, item.out, item.trans)
'''
'''
# .query(属性)获取数据表某列
item_list = session.query(Traffic.station_name).all()
print(f'某列', item_list)

# .all改.first()获取数据表某列第一个元素
item = session.query(Traffic.station_name).first()
print(f'头元素', item)

# .filter(条件)筛选过滤获取数据
item_list = session.query(Traffic.station_name).filter(Traffic.num_enter >= 1000).all()
print(f'条件过滤', item_list)

# .order_by(属性)按某列排序，desc()表示倒序
item_list = session.query(Traffic.station_name, Traffic.num_enter).order_by(Traffic.num_enter.desc()).all()
print(f'排序', item_list)

# 默认为and, 在.filter(条件)中用,分隔多个条件表示and
item_list = session.query(Traffic.station_name, Traffic.num_enter, Traffic.num_out).filter(
    Traffic.num_enter >= 1000, Traffic.num_out >= 10000
).all()
print(f'and条件', item_list)

# 使用or_连接多个条件
item_list = session.query(Traffic.station_name, Traffic.num_enter, Traffic.num_out).filter(
    or_(Traffic.num_enter >= 1000, Traffic.num_out >= 10000)
).all()
print(f'or条件', item_list)

# 条件也支持：等于
item_list = session.query(Traffic.station_name, Traffic.num_enter).filter(
    Traffic.station_name == '骑龙'
).all()
print(f'==条件', item_list)

# 条件也支持：不等于
item_list = session.query(Traffic.station_name, Traffic.num_enter).filter(
    Traffic.station_name != '骑龙'
).all()
print(f'!=条件', item_list)

# 条件也支持：like（字符匹配）
item_list = session.query(Traffic.station_name, Traffic.num_enter).filter(
    Traffic.station_name.like('%川大%')
).all()
print(f'like条件', item_list)

# 条件也支持：in（区间匹配）
item_list = session.query(Traffic.station_name, Traffic.num_enter).filter(
    Traffic.num_enter.in_([1000, 10000])
).all()
print(f'in条件', item_list)

# .all改.count()获取数据表列长
count = session.query(Traffic).count()
print(f'共计', count, f'个站点')

# 后接[:]获取指定行数据
item_list = session.query(Traffic.station_name).all()[:2]
print(f'指定行', item_list)

# 修改骑龙的进站人数为2000
session.query(Traffic).filter(Traffic.station_name == '骑龙').update({'num_enter': 2000})
session.commit()
item = session.query(Traffic.station_name, Traffic.num_enter).filter(Traffic.station_name == '骑龙').first()
print(f'------------------------------------------------------------------------------\n', f'修改数据\n', item)

# 删除名称为顺风的数据
session.query(Traffic).filter(Traffic.station_name == '顺风').delete()
session.commit()
item_list = session.query(Traffic.station_name, Traffic.num_enter).all()
print(f'------------------------------------------------------------------------------\n', f'删除数据\n', item_list)
'''
