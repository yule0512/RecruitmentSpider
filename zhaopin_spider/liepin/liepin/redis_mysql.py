#coding:utf8
import json
import redis
import MySQLdb

def main():
    # 指定redis数据库信息
    try:
        print '正在连接redis'
        rediscli = redis.StrictRedis(host='192.168.2.101', port=6379, db=1)
        print 'redis连接成功'
        # 指定mysql数据库
        print '正在连接mysql'
        mysqlcli = MySQLdb.connect('192.168.2.180', 'root', '123456', 'spider', charset='utf8')
        print 'mysql连接成功'
    except Exception,e:
        print '数据库连接失败'
        print str(e)
        exit()

    while True:
        source, data = rediscli.blpop(["lie_pin:items"])
        # print source # redis里的键
        # print data # 返回的数据
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            sql = '''insert into job values(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")on duplicate key update ''' \
                  '''area=values(area),salary=values(salary),exp=values(exp),edu=values(edu),num=values(num),time=values(time),otherq=values(otherq),welfare=values(welfare)''' \
                  ''',info=values(info),local=values(local),co_url=values(co_url),co_type=values(co_type)''' % \
                  (item['name'], item['co_name'], item['area'], item['salary'],item['exp'],item['edu'], item['num'], item['time'],
                   item['otherq'],item['welfare'],item['info'], item['local'], item['co_url'], item['co_type'],'liepin')

            cur.execute(sql)
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print "inserted %s" % item['name']
        except Exception,e:
            print '插入失败'
            print str(e)

if __name__ == '__main__':
    main()