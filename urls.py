#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('blog.views',
    url(r'^ler/(?P<slug>[a-zA-Z0-9_.-]+)'                                   , 'ler'   ,  name='ler'),
    url(r'^categoria/(?P<categoria>[a-zA-Z0-9_.-]+)(/(?P<pagina>\d{1,3}))?' , 'listar',  name='listar'),
    url(r'^arquivo/(?P<ano>\d{4})/(?P<mes>\d{1,2})(/(?P<pagina>\d{1,3}))?' , 'arquivo',  name='blog_arquivo'),
    url(r'^(?P<pagina>\d{1,3})?'                                     , 'index' ,  name='artigos'),
)


