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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app1 import views

urlpatterns = [
    # url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    # url(r'^upload/', include('fileupload.urls')),

    url(r'^admin/', admin.site.urls),

    # url(r'^$', include('app1.urls')),
    # url(r'^Home/', include('app1.urls')),

    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^about/$', views.about, name='about'),

    url(r'^forum/$', views.forum, name='forum'),
    url(r'^$', views.index, name='index'),  # Replace

    # -------

    url(r'^save_question/$', views.save_question, name='save_question'),
    url(r'^save_answer/(?P<q_id>\d+)$', views.save_answer, name='save_answer'),
    url(r'^like/$', views.like, name='like'),
    url(r'^profile/(?P<user_name>[\w\-]+)/$', views.view_profile, name='user_profile'),  # New! New!

    url(r'^story_edit/(?P<story_id>\d+)/$', views.story_edit, name='story_edit'),
    url(r'^story_delete/(?P<story_id>\d+)/$', views.story_delete, name='story_delete'),
    url(r'^del_comment/$', views.comment_delete, name='comment_delete'),
    url(r'^add_comment/$', views.add_comment, name='add_comment'),

    # Source: https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^story_share/$', views.story_share, name='story_share'),

    url(r'^story_detail/(?P<story_id>\d+)/$', views.story_detail, name='story_detail'),  # New!

    url(r'^(?P<division_name_slug>[\w\-]+)/$', views.division_detail, name='division_detail'),  # New!

    url(r'^Division/add_page/$', views.add_page, name='add_page'),

    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_id>\d+)/$', views.story, name='story'),  # New!


    # New!
    url(r'^Story/(?P<story_id>\d+)/image_share/$', views.image_share, name='image_share'),  # New!
    url(r'^Story/(?P<story_id>\d+)/image_delete/(?P<value_id>\d+)$', views.image_delete, name='delete_pic'),

]

# urlpatterns = [
#     url(r'^register/closed/$',
#         TemplateView.as_view(template_name='registration/registration_closed.html'),
#         name='registration_disallowed'),
#     url(r'^register/complete/$',
#         TemplateView.as_view(template_name='registration/registration_complete.html'),
#         name='registration_complete'),
# ]
#
# if getattr(settings, 'INCLUDE_REGISTER_URL', True):
#     urlpatterns += [
#         url(r'^register/$',
#             RegistrationView.as_view(),
#             name='registration_register'),
#     ]
#
# if getattr(settings, 'INCLUDE_AUTH_URLS', True):
#     urlpatterns += [
#         url(r'', include('registration.auth_urls')),
#     ]

if settings.DEBUG:
            urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#if debug is true,then anything starting with the static/ should be passed to static root,same fo