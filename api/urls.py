from django.conf.urls import patterns, include, url
from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^callback/', views.callback, name = 'callback'),
    url(r'^query_api', views.query_api, name = 'query_api'),
    )