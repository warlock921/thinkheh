#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-10 15:52:11
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^list-images/$', views.list_images, name='list_images'),
	url(r'^upload-image/$', views.upload_image, name='upload_image'),
] 
