from django.apps import AppConfig
from django.conf import settings


class WhatsFreshAPIConfig(AppConfig):
    name = 'whats_fresh.whats_fresh_api'
    verbose_name = settings.SITE_TITLE
