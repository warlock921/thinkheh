from django.shortcuts import render
from .models import BlogArticles
from django.contrib.auth.decorators import login_required

#主页标题视图
# @login_required(login_url='/account/login')
def mainsite_title(request):
	mainsite_set = BlogArticles.objects.all()
	return render(request,"mainsite/titles.html",{"mainsite_set":mainsite_set})

#主页文章内容视图
@login_required(login_url='/account/login')
def mainsite_article(request,article_id):
	article = BlogArticles.objects.get(id=article_id)
	pub = article.publish
	return render(request,"mainsite/content.html",{"article":article,"publish":pub})
