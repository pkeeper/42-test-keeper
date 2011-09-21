#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^$', 'show_profile', name='show_profile'),
)
