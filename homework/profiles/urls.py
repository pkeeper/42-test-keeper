#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('homework',
    url(r'^$', 'profiles.views.show_profile', name='show_profile'),
)