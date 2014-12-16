from common.views import welcome, entry

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', welcome),
    url(r'^entry/(?P<name>\d{8}(_\w+)+)/$', entry),
)
