"""BDTM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from app1 import views


urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^(?P<division_name_slug>[\w\-]+)/$', views.division_detail, name='division_detail'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/add_page/$',views.add_page, name='add_page'),
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/$',views.story, name='story'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/share/$',views.story_share, name='story_share'),  # New!
    #url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/view/$',views.story_view, name='story_view'),  # New!
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^like/$', views.like, name='like'),
]
