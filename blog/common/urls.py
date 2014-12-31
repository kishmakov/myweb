import common.settings

from common.views import list_view, entry_view

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': common.settings.STATIC_ROOT}),
    url(r'^entry/(?P<name>\d{8}(_\w+)+)/$', entry_view),
    url(r'^$', list_view),
    url(r'^(?P<section>\d+)/$', list_view),
    url(r'^(?P<tag>\w+(_\w+)*)/$', list_view),
    url(r'^(?P<tag>\w+(_\w+)*)/(?P<section>\d+)/$', list_view),
)
