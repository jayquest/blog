#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('blog.views',
    url(r'^ler/(?P<slug>[a-zA-Z0-9_.-]+)'                                   , 'ler'   ,  name='ler'),
    url(r'^categoria/(?P<categoria>[a-zA-Z0-9_.-]+)(/(?P<pagina>\d{1,2}))?' , 'listar',  name='listar'),
    url(r'^(?P<pagina>\d{1,2})?'                                     , 'index' ,  name='artigos'),
)


