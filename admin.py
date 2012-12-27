#coding=utf-8
'''
Created on 19/07/2012

@author: Johnny


'''
from django.contrib import admin
from blog.models import Artigo, Categoria, Parceiro
from ckeditor.widgets import CKEditorWidget
from django import forms
from custom_admin.custom_model_admin import CustomModelAdmin
from custom_admin import custom_admin
from datetime import date,datetime

class ArtigoForm(forms.ModelForm):
    texto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Artigo


class CategoriasAdmin(CustomModelAdmin):
    list_display = ('nome','descricao','slug')
    search_fields = ['nome','descricao']
    exclude = ['slug']

def publicar_agora(modeladmin,request,queryset):
    queryset.update(data_pub=datetime.now())
publicar_agora.short_description='Publicar artigos selecionados'

class ArtigoAdmin(CustomModelAdmin):
    exclude = ['slug']
    list_display = ('titulo','categoria','usuario','data_pub','data_fim_pub')
    list_filter = ['data_pub']
    search_fields = ['titulo']
    date_hierarchy = 'data_pub'
    form = ArtigoForm
    actions = [publicar_agora]


class ParceirosAdmin(CustomModelAdmin):
    list_display = ('descricao','link')
    search_fields = ['descricao','link']


custom_admin.custom_site.register(Artigo,ArtigoAdmin)
custom_admin.custom_site.register(Categoria,CategoriasAdmin)
custom_admin.custom_site.register(Parceiro,ParceirosAdmin)
