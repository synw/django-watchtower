# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Hit


@admin.register(Hit)
class HitAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'path',
        'method',
        'ip',
        'username',
        'device',
        'city',
    )
    list_filter = (
        'created',
        'edited',
        'authenticated',
        'staff',
        'superuser',
        'is_pc',
        'is_bot',
        'is_tablet',
        'is_mobile',
        'is_touch',
    )