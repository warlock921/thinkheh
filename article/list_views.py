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
import redis
from django.conf import settings

from .models import AriticleColumn,AriticlePost,Comment
from .forms import CommentForm
from account.models import UserProfile

#redis服务器连接设置，具体参数在settings文件配置
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

#list_views视图开始

#问题标题视图
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

#问题显示页面视图,含问题被浏览次数、最热问题排序（使用redis技术）
@login_required(login_url='/account/login')
@csrf_exempt
def article_detail(request,id,slug):
	userprofile = UserProfile.objects.get(user=request.user)
	user_ip = request.META['REMOTE_ADDR']
	comment_set = Comment.objects.filter(article_id=id)

	#判断用户登录IP是否为同一地址的标志
	user_ip_flag = False

	#判断用户登录IP是否为同一地址
	if user_ip == userprofile.user_ip:
		user_ip_flag = True

	article = get_object_or_404(AriticlePost,id=id,slug=slug)
	# print("本篇文章的ID：%d"%article.id)
	# print("用户最后一次阅读文章的ID：%d"%userprofile.last_article_id)

	#通过IP标志判断是否自增浏览人数
	if user_ip_flag and (userprofile.last_article_id == article.id):	
		total_views = r.incr("article:{}:views".format(article.id))
		total_views = r.decr("article:{}:views".format(article.id))
	else:
		total_views = r.incr("article:{}:views".format(article.id)) #redis对于键的命名没有强制的要求，比较好的用法：“对象类型：对象ID：对象属性”
		userprofile.user_ip = user_ip
		userprofile.last_article_id = article.id
		userprofile.save()

	# print("本篇文章的ID：%d"%article.id)
	# print("用户最后一次阅读文章的ID：%d"%userprofile.last_article_id)

	#重新装配用户IP地址，用*遮掩第三位和第四位
	list_user_ip = user_ip.split(".")
	new_user_ip = list_user_ip[0]+' . '+list_user_ip[1]+' . '+list_user_ip[2]+' . '+' * '

	# #判断是否为同IP，防止刷问题热度
	# if user_ip_flag and (userprofile.last_article_id == article.id):
	# 	r.zincrby('article_ranking', article.id, 0)
	# 	#提取最热问题并进行排序
	# 	article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
	# 	article_ranking_ids = [int(id) for id in article_ranking]
	# 	most_viewed = list(AriticlePost.objects.filter(id__in=article_ranking_ids))
	# 	most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
	# else:
	r.zincrby('article_ranking', article.id, 1)
	#提取最热问题并进行排序
	article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:5]
	article_ranking_ids = [int(id) for id in article_ranking]
	most_viewed = list(AriticlePost.objects.filter(id__in=article_ranking_ids))
	most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

	#取得当前问题答案comment的数量
	comment_count = comment_set.count()
	comment_num_list = []
	while comment_count >= 1:
		comment_count -= 1
		comment_num_list.append(comment_count)
	
	#问题评论处理视图
	if request.method == "POST":
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			cd = comment_form.cleaned_data
			try:
				new_comment = comment_form.save(commit=False)
				new_comment.commentator = request.user
				# print(new_comment.commentator)
				new_comment.article = article
				new_comment.save()
				return HttpResponse("1")
			except Exception as e:
				return HttpResponse("2")
		else:
			return HttpResponse("3")
	else:
		comment_form = CommentForm()

	#答案分页视图语法
	paginator = Paginator(comment_set,5)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
		answers = current_page.object_list
	except PageNotAnInteger:
		current_page = paginator.page(1)
		answers = current_page.object_list
	except EmptyPage:
		current_page = paginator.page(paginator.num_pages)
		answers = current_page.object_list
	#return render(request, "article/list/article_titles.html", {"answers":answers, "page":current_page})

	return render(request, "article/list/article_detail.html", {"article":article, "total_views":total_views, "most_viewed":most_viewed, "new_user_ip":new_user_ip, "comment_num_list":comment_num_list, "comment_form":comment_form, "answers":answers, "page":current_page})

#指定问题点赞视图
@csrf_exempt
@require_POST       #这里表示只接受POST事件
@login_required(login_url='/account/login')
def like_article(request):
	article_id = request.POST.get("id")
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