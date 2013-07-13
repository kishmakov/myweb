import settings
from django.conf.urls import patterns, include, url
from common.views import welcome
from django.contrib import admin
from vle.application import vle_urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', welcome), # welcome
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/favicon.ico'}), # favicon
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += vle_urls()