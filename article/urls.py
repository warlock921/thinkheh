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
]
