#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-19 15:53:02
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import AriticleColumn,AriticlePost

def article_titles(request, username=None):

	#判断是否选择了查看某用户的全部问题
	if username:
		user = User.objects.get(username=username)
		articles_title = AriticlePost.objects.filter(author=user)
	else:
		articles_title = AriticlePost.objects.all() #默认选择全部用户的问题

	# articles_title = AriticlePost.objects.all()

	#分页视图语法
	paginator = Paginator(articles_title,5)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
		articles = current_page.object_list
	except PageNotAnInteger:
		current_page = paginator.page(1)
		articles = current_page.object_list
	except EmptyPage:
		current_page = paginator.page(paginator.num_pages)
		articles = current_page.object_list
	return render(request, "article/list/article_titles.html", {"articles":articles, "page":current_page})

def article_detail(request,id,slug):
	article = get_object_or_404(AriticlePost,id=id,slug=slug)
	return render(request, "article/list/article_detail.html", {"article":article})

@login_required(login_url='/account/login')
@require_POST       #这里表示只接受POST事件
@csrf_exempt
def like_article(request):
	article_id = request.POST.get("id")
	# username = request.POST.get("username")
	# print(username)
	action = request.POST.get("action")
	if article_id and action:
		try:
			article = AriticlePost.objects.get(id=article_id)
			if action == "like":
				article.users_like.add(request.user)
				return HttpResponse("1")
			else:
				article.users_like.remove(request.user)
				return HttpResponse("2")
		except Exception as e:
			return HttpResponse("no")