#coding=utf-8
from datetime import date,datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.datetime_safe import date
from blog.models import Artigo, Categoria, Parceiro
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse

def last_posts(request):
    post_list = Artigo.objects.order_by('-data_pub').filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now())).exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now()))[:4]
    return {'last_posts':post_list}

def parceiros_list(request):
    parceiros = Parceiro.objects.all()[:5]
    return {'blogroll':parceiros}

def index(request,pagina):
    post_list = Artigo.objects.order_by('-data_pub').filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now())).exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now()))
    paginator = Paginator(post_list,2)

    try:
        posts = paginator.page(pagina)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categorias = Categoria.objects.all()[:4]
    categorias_count = Categoria.objects.count()

    tags = list()

    for p in posts.object_list:
        for t in p.tags.all():
            if not tags.__contains__(t):
                tags.append(t)

    return render_to_response('blog.html',{'pagina':pagina,'posts':posts,'categorias':categorias,'categorias_count':categorias_count,'tags':tags,'current':'blog'},context_instance=RequestContext(request))

def listar(request,categoria,pagina):

    categorias = Categoria.objects.all()[:4]
    categorias_count = Categoria.objects.count()
    try:
        categoria = Categoria.objects.get(slug=categoria)
    except ObjectDoesNotExist:
        raise Http404

    posts_list = Artigo.objects.order_by('-data_pub').filter(categoria__id=categoria.id).filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now())).exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now()))
    paginator = Paginator(posts_list,2)
    
    try:
        posts = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    tags = list()

    for p in posts.object_list:
        for t in p.tags.all():
            if not tags.__contains__(t):
                tags.append(t)

    return render_to_response('blog.html',{'pagina':pagina,'posts':posts,'categorias':categorias,'categoria':categoria,'tags':tags,'current':'blog'},context_instance=RequestContext(request))

def ler(request,slug):
    categorias = Categoria.objects.all()[:4]

    try:
        post = Artigo.objects.get(slug=slug)

    except ObjectDoesNotExist:
        raise Http404

    return render_to_response('post.html',{'post':post,'categorias':categorias,'tags':post.tags.all(),'current':'blog'},context_instance=RequestContext(request))

class UltimosPosts(Feed):
    title = "JWG Soluções para Internet : Ultimos Posts"
    link = "/"
    description = "Ultimas publicações feitas no site JWG Soluções para Internet sobre assuntos relacionados a Investimentos na internet, Desenvolvimento Web, Redes sociais, e muito mais!"

    def items(self):
        return Artigo.objects.order_by('-data_pub').filter(Q(data_fim_pub__isnull=True)| Q(data_fim_pub__gte=datetime.now())).exclude(Q(data_pub__isnull=True) | Q(data_pub__gte=datetime.now()))[:5]

    def item_title(self,item):
        return item.titulo

    def item_description(self, item):
        return strip_tags(item.texto)

    def item_link(self, item):
        return reverse('ler',args=(item.slug,))