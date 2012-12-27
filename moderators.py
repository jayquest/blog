#coding=utf-8
'''
Created on 21/07/2012

@author: Johnny
'''
from django.contrib.comments.moderation import CommentModerator, moderator
from blog.models import Artigo

class ArtigoModerator(CommentModerator):
    email_notification = True
    enable_field = 'permitir_comentarios'

moderator.register(Artigo, ArtigoModerator)