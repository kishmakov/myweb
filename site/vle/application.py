from django.conf.urls import patterns, url
from vle.views import gui, data_base

def vle_urls():
    return patterns('',
        url(r'^vle/$', gui),
        url(r'^vle/db/$', data_base))
