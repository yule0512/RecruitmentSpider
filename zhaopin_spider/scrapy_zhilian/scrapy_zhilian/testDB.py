#coding:utf8
import MySQLdb
'''
    数据库连接操作
'''
class Mydb:
    def __init__(self):
        try:

            #self.conn = MySQLdb.connect('192.168.2.120','root','123456','mytest',charset='utf8')
            # 连接XAMPP Control中的mysql
            #self.conn = MySQLdb.connect('127.0.0.1','root','','mytest',charset='utf8')
            self.conn = MySQLdb.connect('192.168.2.120','root','123456','zhilian',charset='utf8')
            # 创建数据库操作游标
            self.cursor = self.conn.cursor()
            print '连接成功'
        except Exception,e:
            print str(e)
            exit()
    # 查询全部
    def query(self):
        try:
            sql = "select * from myweb_stu"
            sql = '''insert into job values(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")on duplicate key update ''' \
                  '''area=values(area),salary=values(salary),exp=values(exp),edu=values(edu),num=values(num),time=values(time),otherq=values(otherq),welfare=values(welfare)''' \
                  ''',info=values(info),local=values(local),co_url=values(co_url),co_type=values(co_type)''' % \
                  '''(item['name'], item['co_name'], item['area'], item['salary'],item['exp'],item['edu'], item['num'], item['time'],item['otherq'],item['welfare'],item['info'], item['local'], item['co_url'], item['co_type'],'job51')'''



            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            print res
            return res
        except Exception,e:
            print str(e)

mydb = Mydb()
mydb.query()