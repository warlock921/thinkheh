#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 19:19:19
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
	# email = forms.EmailField(label="Email", widget=forms.EmailInput)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username","email")

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password']!=cd['password2']:
			raise forms.ValidationError("两次输入的密码不匹配！")
		return cd['password2']

class UserProfileForm(forms.ModelForm):
	birth = forms.DateField(widget=forms.TextInput(attrs={'class':'input'}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'input'}))
	class Meta:
		model = UserProfile
		fields = ("birth","phone","sex","company_or_person")

class UserInfoForm(forms.ModelForm):
	class Meta:
		model = UserInfo
		fields = ("SUC_code","company","profession","address","aboutme","photo")

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ("email",)
		

		
