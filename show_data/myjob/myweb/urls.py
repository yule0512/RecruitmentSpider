from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<pIndex>[0-9]*)$', views.pos_index,name='pos_index'),#首页
    url(r'^list/(?P<pIndex>[0-9]+)$', views.pos_list, name="pos_list"), #带参数检索列表页
    url(r'^detail/(?P<gd>[0-9]+)$', views.pos_detail, name="pos_detail"), #详情页
]
