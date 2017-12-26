#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-26 14:47:21
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$

from django import template

register = template.Library()

from article.models import AriticlePost
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

@register.simple_tag
def total_articles():
	return AriticlePost.objects.count()

@register.simple_tag
def author_total_article(user):
	return user.article.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
	latest_articles = AriticlePost.objects.order_by("-created")[:n]
	return {"latest_articles":latest_articles}

@register.assignment_tag
def most_commented_articles(n=5):
	return AriticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]


@register.filter(name='markdown')
def markdown_filter(text):
	return mark_safe(markdown.markdown(text))


