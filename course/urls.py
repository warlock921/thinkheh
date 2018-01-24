#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-23 16:40:41
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django.conf.urls import url
from .views import AboutView,CourseListView,ManageCourseListView,CreateCourseView

urlpatterns = [
	url(r'about/$',AboutView.as_view(),name="about"),
	url(r'course-list/$',CourseListView.as_view(),name="course_list"),
	url(r'manage-course/$',ManageCourseListView.as_view(),name="manage_course"),
	url(r'create-course/$', CreateCourseView.as_view(), name="create_course"),
]
