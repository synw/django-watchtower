# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class Hit(models.Model):
    created = CreationDateTimeField(editable=False)
    edited = ModificationDateTimeField(editable=False)
    path = models.CharField(
        db_index=True, max_length=255, verbose_name=_("Path"))
    method = models.CharField(max_length=6, verbose_name=_("Method"))
    ip = models.CharField(max_length=12, verbose_name=_("Ip"))
    user_agent = models.CharField(max_length=255, verbose_name=_("User agent"))
    authenticated = models.BooleanField(
        verbose_name=_("Authenticated user"), default=False)
    staff = models.BooleanField(verbose_name=_("Staff user"), default=False)
    superuser = models.BooleanField(
        verbose_name=_("Superuser"), default=False)
    username = models.CharField(
        db_index=True, max_length=120, verbose_name=_("Username"))
    referer = models.CharField(
        max_length=255, blank=True, verbose_name=_("Referer"))
    view = models.CharField(max_length=120, blank=True, verbose_name=_("View"))
    module = models.CharField(
        max_length=120, blank=True, verbose_name=_("Module"))
    status_code = models.PositiveSmallIntegerField(
        verbose_name=_("Status code"))
    reason_phrase = models.CharField(
        max_length=120, blank=True, verbose_name=_("Reason phrase"))
    request_time = models.PositiveIntegerField(verbose_name=_("Request time"))
    doc_size = models.PositiveIntegerField(verbose_name=_("Document size"))
    num_queries = models.PositiveIntegerField(
        verbose_name=_("Number of queries"))
    queries_time = models.PositiveIntegerField(verbose_name=_("Queries time"))
    is_tablet = models.BooleanField(default=False, verbose_name=_("Tablet"))
    is_pc = models.BooleanField(default=False, verbose_name=_("PC"))
    is_bot = models.BooleanField(default=False, verbose_name=_("Bot"))
    os = models.CharField(max_length=120, verbose_name=_("Operating system"))
    os_version = models.CharField(
        max_length=120, verbose_name=_("Operating system version"))
    is_tablet = models.BooleanField(default=False, verbose_name=_("Tablet"))
    is_mobile = models.BooleanField(default=False, verbose_name=_("Mobile"))
    is_touch = models.BooleanField(
        default=False, verbose_name=_("Has touch capabilities"))
    browser = models.CharField(max_length=255, verbose_name=_("Browser"))
    device = models.CharField(max_length=255, verbose_name=_("Device"))
    country = models.CharField(max_length=120, verbose_name=_("Country"))
    city = models.CharField(max_length=120, verbose_name=_("City"))
    latitude = models.CharField(max_length=24, verbose_name=_("Latitude"))
    longitude = models.CharField(max_length=25, verbose_name=_("Longitude"))
    region = models.CharField(max_length=120, verbose_name=_("Region"))
    city = models.CharField(max_length=120, verbose_name=_("City"))

    class Meta:
        app_label = 'watchtower'
        verbose_name = _(u'Hit')
        verbose_name_plural = _(u'Hits')
        ordering = ['-created']

    def __str__(self):
        return self.path + ' - ' + str(self.created)
