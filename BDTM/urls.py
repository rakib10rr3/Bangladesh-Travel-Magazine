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
from app1 import views
from django.contrib.auth import views as auth_views

# changged
urlpatterns = [
    # url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    # url(r'^upload/', include('fileupload.urls')),

    url(r'^admin/', admin.site.urls),
    # url(r'^$', include('app1.urls')),
    # url(r'^Home/', include('app1.urls')),

    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^about/$', views.about, name='about'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_ques/$', views.search_ques, name='search_ques'),
    url(r'^forum/$', views.forum, name='forum'),
    url(r'^notifications/$', views.notifications, name='notifications'),

    url(r'^$', views.index, name='index'),  # Replace

    # -------

    url(r'^save_question/$', views.save_question, name='save_question'),

    url(r'^follow_unfollow/$', views.follow_unfollow, name='follow_unfollow'),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
    url(r'^save_answer/$', views.save_answer, name='save_answer'),

    url(r'^like/$', views.like, name='like'),

    url(r'^update_userprofile/(?P<user_id>\d+)/$', views.update_userprofile, name='update_userprofile'),  # New! New!

    url(r'^profile/(?P<user_name>[\w\-]+)/$', views.view_profile, name='user_profile'),  # New! New!

    url(r'^story_edit/(?P<story_id>\d+)/$', views.story_edit, name='story_edit'),

    url(r'^story_delete/(?P<story_id>\d+)/$', views.story_delete, name='story_delete'),

    url(r'^api/story/add/$', views.ajax_add_story, name='ajax_add_story'),

    url(r'^api/place/suggestion/$', views.ajax_get_place_names, name='ajax_get_place_names'),

    url(r'^api/share/$', views.ajax_notify_followers, name='ajax_notify_followers'),

    url(r'^ques_delete/(?P<ques_id>\d+)/$', views.delete_ques, name='ques_delete'),

    # url(r'^ques_edit/(?P<ques_id>\d+)/$', views.edit_ques, name='ques_edit'),

    url(r'^del_comment/$', views.comment_delete, name='comment_delete'),

    url(r'^answer_delete/$', views.answer_delete, name='answer_delete'),
    url(r'^ownreport/$', views.Own_report, name='own_report'),  # s29
    url(r'^edit_answer/$', views.answer_edit, name='answer_edit'),

    url(r'^edit_question/$', views.question_edit, name='edit_question'),
    url(r'^reported_story/$', views.reported_story, name='reported_story'),  # S29
    url(r'^add_comment/$', views.add_comment, name='add_comment'),

    # Source: https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^story_share/$', views.story_share, name='story_share'),

    url(r'^update_follow_list/$', views.update_follow_list, name='update_follow_list'),

    url(r'^story_detail/(?P<story_id>\d+)/$', views.story_detail, name='story_detail'),  # New!
    url(r'^ques_detail/(?P<ques_id>\d+)/$', views.ques_detail, name='ques_detail'),  # New!
    url(r'^(?P<division_name_slug>[\w\-]+)/$', views.division_detail, name='division_detail'),  # New!

    url(r'^division/add_page/$', views.add_page, name='add_page'),

    url(r'^(?P<division_name_slug>[\w\-]+)/(?P<page_id>\d+)/$', views.story, name='story'),  # New!


    # New!
    url(r'^story/(?P<story_id>\d+)/image_share/$', views.image_share, name='image_share'),  # New!

    url(r'^story/(?P<story_id>\d+)/image_share_jquery/$', views.image_share_jquery, name='image_share_jquery'),  # New!

    url(r'^story/(?P<story_id>\d+)/image_delete/(?P<value_id>\d+)$', views.image_delete, name='delete_pic'),
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
# if debug is true,then anything starting with the static/ should be passed to static root,same fo
