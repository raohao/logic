# -*- coding: utf-8 -*-
from django.contrib import admin
from centre.models import (RiskClosure, UserComments)


# Register your models here.
@admin.register(RiskClosure)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author_user_id', 'rank', 'publish_time', 'status')
    list_filter = ('status', 'publish_time', 'rank')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author_user_id',)
    date_hierarchy = 'publish_time'
    ordering = ['status', 'publish_time']
    list_per_page = 15


@admin.register(UserComments)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'comment_user_id',)
    raw_id_fields = ('comment_user_id',)
    date_hierarchy = 'create_time'
    ordering = ['create_time',]
    list_per_page = 15

