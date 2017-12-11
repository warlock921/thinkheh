#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 19:15:54
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url 
from . import views
from django.conf import settings 
from django.contrib.auth import views as auth_views

urlpatterns = [
	#url(r'^login/$', views.user_login, name="user_login"),
	url(r'^login/$', auth_views.login, name="user_login"),
	#url(r'^new-login/$', auth_views.login, {"template_name":"account/login.html"}),
	url(r'^logout/$', auth_views.logout, {"template_name":"account/logout.html"}, name="user_logout"),
	url(r'^register/$',views.register,name="user_register"),
	url(r'^password-change/$', auth_views.password_change, {"post_change_redirect":"/account/password-change-done"}, name='password_change'),
	url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
]