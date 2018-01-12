#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-10 14:47:48
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import ImageLoad

class ImageLoadForm(forms.ModelForm):
	class Meta:
		model = ImageLoad
		fields = ('title','url','description')
    
    #处理数据库url字段的值，此方法不接收self以外的参数
	def clean_url(self):
		url = self.cleaned_data['url']
		#print(url);
		valid_extensions = ['jpg','jpeg','png']
		extension = url.rsplit('.',1)[1].lower()

		if extension not in valid_extensions:
			raise forms.ValidationError("您所提供的url无法获取图片")
		return url
    #重写save方法
	def save(self,force_insert=False,force_update=False,commit=True):
		image = super(ImageLoadForm,self).save(commit=False)
		# print(image)
		image_url = self.cleaned_data['url']
		image_name = '{0}.{1}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
		response = request.urlopen(image_url)
		#第一个image是数据库的字段，第二个image是本方法定义的image
		image.image.save(image_name,ContentFile(response.read()),save=False)
		if commit:
			image.save()

		return image


