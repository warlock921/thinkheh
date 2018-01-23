#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-23 16:40:41
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django.conf.urls import url
from .views import AboutView

urlpatterns = [
	url(r'about/$',AboutView.as_view(),name="about"),
]
