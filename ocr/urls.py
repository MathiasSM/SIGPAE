from django.conf.urls import url

from . import views

app_name = 'ocr'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^borradores$', views.borradores, name='borradores'),
    url(r'^borradores/(?P<draft_id>\d+)/$', views.borrador, name='borrador'),
]
