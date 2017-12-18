#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-14 22:13:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django import forms 
from .models import AriticleColumn,AriticlePost

class AriticleColumnForm(forms.ModelForm):
	class Meta:
		model = AriticleColumn 
		fields = ("column",)

class AriticlePostForm(forms.ModelForm):
	class Meta:
		model = AriticlePost
		fields = ("title", "body")
		
		
