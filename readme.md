# 2024.1.7  
做了一些简单的SQLAlchemy库使用例  
配置文件在config.py里  
main.py里是单表的建表链接、增删查改实现例  
目前缺少内容：  
多表模型建立与增删查改  
聚合分组、原生SQL  
预计在1~3天内全部补充完使用例  
  
P.S  
好像必须得先在MySQL建立数据库，之后才能做这些工作，还是无法完全绕开MySQL啊  

----------------------------
# 2024.1.8  

补充知识点，重新调整了数据表结构，写了一点更方便的增删查改函数

使用SQLAlchemy框架实现ORM技术的全过程：  
① 用户输入传给ORM对象  
② ORM对象提交SQLAlchemy核  
③ 用户输入由Schema/Types和SQL Expression Language转成SQL语句  
④ Engine匹配已有的engine，从链接池取链接  
⑤ 链接用Dialect调用DBAPI，SQL语句转交DBAPI执行  

对于存储所需要的站点-时间-进站-出站-换乘-OD的数据，  

除OD外的数据设计1张数据表如下：  
traffic  
int(id)，每1个id对应某站某时段的1份进站-出站-换乘数据  
int(日期)，如20240108表示2024年1月8日  
int(时刻)，如1900表示从19:00到19:15的时间段
int(站点id)  
int(进站人数)  
int(出站人数)  
int(换乘人数)

时间长度越短，OD矩阵越稀疏，考虑用三元组储存OD矩阵，  
每个OD矩阵1张数据表，用日期+时刻作为数据表名作为OD矩阵id  
如202401081900，  
表示2024年1月8日从19:00到19:15数据求得的OD矩阵  
int(进站站点id)   
int(出站站点id)  
int(OD矩阵元素值)   

站点id与站点名是一一对应的，  
可以写一个一对一表储存，  
当然也可以Excel表格形式本地存储  

对日期和时刻的数据类型，mysql有专门的数据类型，  
但感觉int型也完全可用，还方便点  

这样，想获取某站某时段的一份进站-出站-换乘-OD数据，  
确定时段和站点，可以通过条件查询获取进站-出站-换乘数据。  
确定时段，可以通过条件查询获取完整的OD矩阵。  
上述操作可以打包SQLAlchemy函数，  
写成更简单的函数或类，加强代码通用性。

现在，config.py文件仍然保存必要的环境配置信息;   
demo.py文件会通过配置信息连接数据库，创建数据表、增删查改数据;  
最后会删除这一数据库下跑demo创建的数据表，方便下次跑demo;

---
# 20240109

在数据库结构上，认为相关任务主要是：   
1. 设计数据库  
设计 日期-时段-站点-进站-出站-换乘-OD 的数据表结构   
   - traffic：日期-时段-站点-进人-出人-换人（）  
   - od：日期-时段-进点-出点-OD值（稀疏矩阵）
   - 后续功能实现依赖数据表结构，结构变动后要重构函数。


2. 增删查改功能实现  
    1. traffic数据表：  
    - 查询：输入日期、时段、站点，返回进+出+换人数
    - 增加：输入日期、时段、站点、进+出+换人数，增加记录
    - 更新：输入日期、时段、站点，新的进/出/换人数，更新记录
    - 删除：指定日期、时段、站点，删除该条记录
    2. od数据表：
    - 查询：输入日期、时段，返回OD矩阵
    - 增加：输入日期、时段、进+出点、OD值，增加记录
    - 更新：输入日期、时段、进+出点，新的OD值，更新记录
    - 删除：输入日期、时段，删除该条记录

目前算是基本实现以上任务了，  
在面对新的数据结构和新的功能需求时，  
应能较好地设计数据表，实现ORM需求。

# 未来目标：

1. 需要随时跟进组内需求，按需求更新数据表结构和重构功能代码  
2. 增删查改函数的功能实现还有优化和拓展的巨大空间
    - 使用SQLAlchemy1.X的函数，在2.0版本有更高效的新方法
    - 函数未考虑异常处理
    - 自定义功能代码还未打包，与测试代码混在一起

# 参考文献：

https://www.cnblogs.com/blueberry-mint/p/14277882.html  
https://zhuanlan.zhihu.com/p/444930067  
https://blog.csdn.net/zengbowengood/article/details/103580010