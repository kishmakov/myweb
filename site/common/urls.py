import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from common.views import welcome
import notes.urls as notes_urls
import fluid.urls as fluid_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', welcome), # welcome
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += notes_urls.get()
urlpatterns += fluid_urls.get()