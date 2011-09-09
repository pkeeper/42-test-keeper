#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^requests/$', 'requests.views.requests_list', name='requests_list'),
)
