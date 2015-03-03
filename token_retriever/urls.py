from django.conf.urls import patterns, include, url
from token_retriever import views

urlpatterns = patterns('',
    url(r'^url_constructor/', views.url_constructor, name = 'url_constructor'),
    )
