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


urlpatterns = [
    #url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    #url(r'^upload/', include('fileupload.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('app1.urls')),
    url(r'^Home/', include('app1.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),

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