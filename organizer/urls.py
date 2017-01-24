# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from organizer import settings
from organizer import views

from organizer.tools import IsLinux

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^meetings/', include('meetings.urls')),
    url(r'^accounts/login/$', views.account_login, name='login'),
    url(r'^accounts/logged_in/$', views.account_logged_in, name='logged_in'),
    url(r'^accounts/logout/$', views.account_logout, name='logout'),
    url(r'^accounts/logged_out/$', views.account_logged_out, name='logged_out'),
    url(r'^accounts/create/$', views.account_create, name='create'),
    url(r'^accounts/created/$', views.account_created, name='created'),
    url(r'^admin/', admin.site.urls),
]

if not IsLinux():
    favicon_view = RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')
    robots_view = RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt')
    urlpatterns.append(url(r'^favicon\.ico$', favicon_view))
    urlpatterns.append(url(r'^robots\.txt$', robots_view))
