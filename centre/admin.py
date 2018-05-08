# -*- coding: utf-8 -*-
from django.contrib import admin
from centre.models import RiskClosure


# Register your models here.
@admin.register(RiskClosure)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'rank', 'p_time', 'status')
    list_filter = ('status', 'p_time', 'rank')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'p_time'
    ordering = ['status', 'p_time']
    list_per_page = 15

    class Meta:
        verbose_name = '风险提示'
        verbose_name_plural = verbose_name
