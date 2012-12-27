#coding=utf-8
__author__ = 'Johnny'


from custom_admin.dashboard import *
from blog.models import *
from django.contrib.auth.models import *
from django.db.models.query import *
from datetime import date,datetime



blog_dash = AppDashboard(title='Blog')

blog_dash.app_label = Artigo._meta.app_label

blog_dash.infos.append(
    DashboardInfo(
        name='Artigos escritos',
        query_set=Artigo.objects.all()))

blog_dash.infos.append(
    DashboardInfo(
        name='Artigos publicados',
        query_set=Artigo.objects.order_by('-data_pub')
                                .filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now()))
                                .exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now()))))

blog_dash.infos.append(
    DashboardInfo(
        name='Ultima publicação',
        query_set=Artigo.objects.order_by('-data_pub')
                                .filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now()))
                                .exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now())),operation='first'))


blog_dash.infos.append(
    DashboardInfo(
        name='Categorias',
        query_set=Categoria.objects.all())
    )

blog_dash.infos.append(
    DashboardInfo(
        name='Autores',
        query_set=Artigo.objects.select_related('usuario')))


blog_dash.add_report(ListReport(title='Ultimas do blog',
                                query_set=Artigo.objects.order_by('-data_pub').exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now())),list_size=10,
                                display_fields=['titulo','categoria','data_pub']))


dash.register(blog_dash)