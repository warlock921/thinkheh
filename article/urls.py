#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 22:28:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url 
from . import views 

urlpatterns = [
	url(r'^article-column/$', views.article_column, name='article_column'),
	url(r'^rename-column/$', views.rename_article_column, name='rename_article_column'),
	url(r'^del-column/$', views.del_article_column, name='del_article_column'),
	url(r'^article-post/$', views.article_post, name='article_post'),
	url(r'^article-list/$', views.article_list, name='article_list'),
	url(r'^article_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
]
