from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('homework.profiles.urls')),
    url(r'^', include('homework.requests.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
