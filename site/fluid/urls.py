from django.conf.urls import patterns, url
from fluid.views import index, note

def get():
    return patterns('',
        url(r'^fluid/$', index),
        url(r'^fluid/(?P<num>\d+)/$', note)
    )
