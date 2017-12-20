#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 22:28:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url 
from . import views,list_views

urlpatterns = [
	url(r'^article-column/$', views.article_column, name='article_column'),
	url(r'^rename-column/$', views.rename_article_column, name='rename_article_column'),
	url(r'^del-column/$', views.del_article_column, name='del_article_column'),
	url(r'^article-post/$', views.article_post, name='article_post'),
	url(r'^image-upload/$', views.editor_image_upload, name='editor_image_upload'),
	url(r'^article-list/$', views.article_list, name='article_list'),
	url(r'^article_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
	url(r'^del-article/$', views.del_article, name="del_article"),
	url(r'^redit-article/(?P<article_id>\d+)/$', views.redit_article, name="redit_article"),
	url(r'^list-article-titles/$', list_views.article_titles, name="article_titles"),
	url(r'^list-article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', list_views.article_detail, name="list_article_detail"),
	url(r'^list-article-titles/(?P<username>[-\w]+)/$', list_views.article_titles, name="author_articles"),
] 
