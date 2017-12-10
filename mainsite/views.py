from django.shortcuts import render
from .models import BlogArticles

def mainsite_title(request):
	mainsite_set = BlogArticles.objects.all()
	return render(request,"mainsite/titles.html",{"mainsite_set":mainsite_set})

def mainsite_article(request,article_id):
	article = BlogArticles.objects.get(id=article_id)
	pub = article.publish
	return render(request,"mainsite/content.html",{"article":article,"publish":pub})
