#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'profiles.views.show_profile', name='show_profile'),
)
