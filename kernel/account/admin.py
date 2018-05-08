# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import (get_user_model)
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from account.forms import (UserCreationForm, UserChangeForm)
from account.models import (AdminUser, HeadUser, BranchUser)

UserModel = get_user_model()

# Register your models here.


class CustomUser(UserAdmin):
    # The forms to add and change user instances

    form = UserChangeForm
    add_form = UserCreationForm

# The fields to be used in displaying the User model.
# These override the definitions on the base UserAdmin
# that reference specific fields on auth.User.

    fieldsets = (
        ('基本', {'fields': ('user_id', 'password')}),
        (_('Personal info'), {'fields': ('institution',)}),
        (_('Permissions'), {'fields': ('power_level', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
# overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'password1', 'password2'),
        }),
    )

    list_per_page = 50
    list_display = ("user_id", "institution", "power_level", "start_from", "end_to",)
    list_filter = ("power_level",)
    search_fields = ("user_id", )
    ordering = ("institution",)
    data_hierarch = "end_to"


@admin.register(AdminUser)
class MyUserAdmin(CustomUser):
    class Meta:
        verbose_name = '管理员用户'
        verbose_name_plural = verbose_name


@admin.register(HeadUser)
class MyUserHead(CustomUser):
    class Meta:
        verbose_name = '总行用户'
        verbose_name_plural = verbose_name


@admin.register(BranchUser)
class MyUserBranch(CustomUser):
    class Meta:
        verbose_name = '分行用户'
        verbose_name_plural = verbose_name