from django.conf.urls import patterns, url
from notes.views import metaphysics, mp_note
from notes.views import technology

def get():
    return patterns('',
        url(r'^notes/mp/$', metaphysics),
        url(r'^notes/mp/(?P<num>\d+)/$', mp_note),
        url(r'^notes/th/$', technology)
    )
