#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-07 21:12:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^$', views.mainsite_title, name="mainsite_title"),
	url(r'^(?P<article_id>\d)/$',views.mainsite_article,name="mainsite_detail")
]