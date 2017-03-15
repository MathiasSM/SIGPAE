from django.conf.urls import url

from . import views

app_name = 'ocr'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^borradores$', views.listar_borradores, name='borradores'),
    url(r'^borradores/new$', views.try_keep, name='borradores-new'),
    url(r'^borradores/(?P<draft_id>\d+)/$', views.editar_borrador, name='borrador'),
]
