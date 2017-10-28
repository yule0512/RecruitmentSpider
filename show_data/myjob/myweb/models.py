from django.db import models

# Create your models here.
#工作信息类
class Jobs(models.Model):
    name = models.CharField(max_length=250)
    co_name = models.CharField(max_length=250)
    area = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    exp = models.CharField(max_length=250)
    edu = models.CharField(max_length=250)
    num = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    welfare = models.CharField(max_length=250)
    info = models.TextField()
    local = models.CharField(max_length=250)
    co_url = models.CharField(max_length=250)
    co_type = models.CharField(max_length=250)
    spider_name = models.CharField(max_length=250)

    def dicts(self):
        return {'id':self.id,'name':self.name,'co_name':self.co_name,'area':self.area,'salary':self.salary,'exp':self.exp,'edu':self.edu,'num':self.num,'time':self.time,'welfare':self.welfare,'info':self.info,'local':self.local,'co_url':self.co_url,'co_type':self.co_type,'spider_name':self.spider_name}

    class Meta:
        db_table = "job"