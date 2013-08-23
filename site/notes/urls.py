from django.conf.urls import patterns, url
from notes.views import four_colors
from notes.views import metaphysics, mp_note
from notes.views import technology, th_note

def get():
    return patterns('',
        url(r'^notes/mp/$', metaphysics),
        url(r'^notes/four_colors/$', four_colors),
        url(r'^notes/mp/(?P<num>\d+)/$', mp_note),
        url(r'^notes/th/$', technology),
        url(r'^notes/th/(?P<num>\d+)/$', th_note)
    )
