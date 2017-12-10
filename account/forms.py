#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 19:19:19
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django import forms

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
