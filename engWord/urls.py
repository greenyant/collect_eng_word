from django.conf.urls import patterns, include, url

from engWord.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
)