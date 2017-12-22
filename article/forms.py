#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 22:13:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django import forms 
from .models import AriticleColumn,AriticlePost,Comment

#问题标签表单
class AriticleColumnForm(forms.ModelForm):
	class Meta:
		model = AriticleColumn 
		fields = ("column",)

#问题提交表单
class AriticlePostForm(forms.ModelForm):
	class Meta:
		model = AriticlePost
		fields = ("title", "body")

#评论提交表单
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment 
		fields = ("body",)

		
		
