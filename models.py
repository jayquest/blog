#coding=utf-8
from django.core.urlresolvers import reverse

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
#    imagem = models.ImageField(upload_to='categorias')
    slug = models.SlugField(max_length=100)
    def __unicode__(self):
        return self.nome

class Artigo(models.Model):
    titulo = models.CharField(max_length=100)
    intro = models.TextField()
    texto = models.TextField()
    imagem = models.ImageField(upload_to='artigos')
    video = models.CharField(max_length=450,null=True,blank=True)
    data_pub = models.DateTimeField('Publicado em',null=True,blank=True)
    data_fim_pub = models.DateTimeField('Publicado até',null=True,blank=True)
    usuario = models.ForeignKey(User)
    categoria = models.ForeignKey(Categoria)
#    permitir_comentarios = models.BooleanField()
    slug = models.SlugField(max_length=200)
    tags = TaggableManager()
    def __unicode__(self):
        return self.titulo + ' - ' + self.usuario.first_name

    def get_absolute_url(self):
        return reverse('blog.views.ler',args=[self.slug])

class Parceiro(models.Model):
    descricao = models.CharField(max_length=60)
    link = models.URLField()

#SIGNALS

from django.db.models import signals
from django.template.defaultfilters import slugify

def categoria_pre_save(signal,instance,sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    artigo com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""
    slug = slugify(instance.nome)
    novo_slug = slug
    contador = 0

    while Categoria.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def artigo_pre_save(signal,instance,sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    artigo com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""

    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Artigo.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

signals.pre_save.connect(categoria_pre_save,sender=Categoria)
signals.pre_save.connect(artigo_pre_save,sender=Artigo)
