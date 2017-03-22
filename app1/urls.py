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
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^like/$', views.like, name='like'),
    url(r'^profile/(?P<user_name>[\w\-]+)/$', views.view_profile, name='user_profile'),  # New! New!

    # Source: https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/story/(?P<story_id>\d+)/comment/$', views.add_comment_to_story,
        name='add_comment_to_story'),

    url(r'^(?P<division_name_slug>[\w\-]+)/$', views.division_detail, name='division_detail'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/$', views.story, name='story'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/share/$', views.story_share, name='story_share'),
    # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/share/(?P<story_id>\d+)$', views.image_share,
        name='image_share'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/share/(?P<story_id>\d+)/(?P<value_id>\d+)$',
        views.image_delete, name='delete_pic'),

    # New!
    # url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/view/$',views.story_view, name='story_view'),  # New!
]
