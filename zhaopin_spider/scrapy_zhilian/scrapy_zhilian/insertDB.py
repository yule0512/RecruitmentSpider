#coding:utf8
import MySQLdb
import redis
import json
def main():
    try:
        rediscli = redis.StrictRedis(host='192.168.2.120', port=6379, db=0)
        # 本地mysql数据库
        mysqlcli = MySQLdb.connect('192.168.2.120','root','123456','zhilian',charset='utf8')
        #mysqlcli = MySQLdb.connect('192.168.2.218','centos4','123456','mydb',charset='utf8')
        #mysqlcli = MySQLdb.connect('192.168.2.180','root','123456','spider',charset='utf8')
        print '连接成功'
    except Exception,e:
        print '连接失败'
        print e
    while True:
        source,data = rediscli.blpop(['zhilian:items'])
        # print source
        # print data
        item = json.loads(data)
        # print item['info']
        try:
            # 创建mysql游标
            cur = mysqlcli.cursor()

            mysql = "insert into zhaopintb values (null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') on duplicate key update " \
            "name=values(name),co_name=values(co_name),area=values(area),salary=values(salary),exp=values(exp),edu=values(edu),num=values(num),time=values(time),welfare=values(welfare),info=values(info),local=values(local),co_url=values(co_url),co_type=values(co_type),spider_name=values(spider_name) " % (item['name'],item['co_name'],item['area'],item['salary'],item['exp'],item['edu'],item['num'],item['time'],item['welfare'],item['info'],item['local'],item['co_url'],item['co_type'],item['spider_name'])


            sql = '''insert into job values(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")on duplicate key update ''' \
          '''area=values(area),salary=values(salary),exp=values(exp),edu=values(edu),num=values(num),time=values(time),otherq=values(otherq),welfare=values(welfare)''' \
          ''',info=values(info),local=values(local),co_url=values(co_url),co_type=values(co_type)''' % \
          (item['name'], item['co_name'], item['area'], item['salary'],item['exp'],item['edu'], item['num'], item['time'],'',item['welfare'],item['info'], item['local'], item['co_url'], item['co_type'],item['spider_name'])
            cur.execute(mysql)
            mysqlcli.commit()
            print "inserted %s " % item['name']
            # sql = "select * from myweb_stu"
            cur.close()
        except Exception,e:
            print e


if __name__ == '__main__':
    main()