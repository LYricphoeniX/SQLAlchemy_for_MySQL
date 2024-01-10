from traffic_data.basic import *
from traffic_data.orm_operator import *


if __name__ == '__main__':
    op = OrmOpearator()
    print(f'添加数据测试')
    op.addtraffic(20240108, 1900, 0, 100, 100, 100)
    op.addtraffic(20240108, 1900, 1, 500, 500, 500)
    op.addtraffic(20240108, 1900, 2, 2000, 2000, 2000)

    op.addod(20240108, 1900, 0, 1, 10)
    op.addod(20240108, 1900, 0, 2, 20)
    op.addod(20240108, 1900, 1, 0, 5)
    op.addod(20240108, 1900, 1, 2, 15)
    op.addod(20240108, 1900, 2, 1, 1)

    print(f'查询数据测试')
    op.gettraffic(20240108, 1900, 0)
    op.gettraffic(20240108, 1900, 1)
    op.gettraffic(20240108, 1900, 2)
    op.getod(20240108, 1900)

    print(f'修改数据测试')
    op.changetraffic(20240108, 1900, 100, 500, 500, 500)
    op.gettraffic(20240108, 1900, 100)
    op.changetraffic(20240108, 1900, 100, 100, 100, 100)
    op.gettraffic(20240108, 1900, 100)
    op.changeod(20240108, 1900, 0, 1, 100)
    op.getod(20240108, 1900)
    op.changeod(20240108, 1900, 0, 1, 10)
    op.getod(20240108, 1900)

    print(f'删除数据测试')
    op.ridtraffic(20240108, 1900, 0)
    op.ridtraffic(20240108, 1900, 1)
    op.ridtraffic(20240108, 1900, 2)
    op.ridod(20240108, 1900, 0, 1)
    op.ridod(20240108, 1900, 0, 2)
    op.ridod(20240108, 1900, 1, 0)
    op.ridod(20240108, 1900, 1, 2)
    op.ridod(20240108, 1900, 2, 1)

    # 删除临时测试用的数据表，方便下次测试
    session.execute(text("drop table traffic"))
    session.execute(text("drop table od"))
    session.close()
    print(f'测试结束')