from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from fluid.views import index, note, notations, references, data_papers, links

def get():
    return patterns('',
        url(r'^fluid/$', index),
        url(r'^fluid/note/(?P<num>\d+)/$', note),
        url(r'^fluid/help/notations/$', notations),
        url(r'^fluid/help/references/$', references),
        url(r'^fluid/help/data/$', data_papers),
        url(r'^fluid/help/links/$', links),
        url(r'^fluid/peng_robinson.html$', RedirectView.as_view(url='note/3/', permanent=False)),
        url(r'^fluid/vapor_liquid_equilibrium.html$', RedirectView.as_view(url='note/5/', permanent=False)),
        url(r'^fluid/sonic_speed.html$', RedirectView.as_view(url='note/4/', permanent=False)),
        url(r'^fluid/heat_capacities.html$', RedirectView.as_view(url='note/1/', permanent=False)),
        url(r'^fluid/liquid_volume.html$', RedirectView.as_view(url='note/2/', permanent=False)),
    )
