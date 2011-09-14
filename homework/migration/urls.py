from django.conf.urls.defaults import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^migrate/(?P<id>[-\w]+)/$', 'migration.views.migrate'),
)
