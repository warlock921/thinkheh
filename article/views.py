from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .forms import AriticleColumnForm,AriticlePostForm
from .models import AriticleColumn,AriticlePost

#文章列表视图
@login_required(login_url='/account/login')
@csrf_exempt
def article_column(request):
	if request.method == "GET":
		columns = AriticleColumn.objects.filter(user=request.user)
		column_form = AriticleColumnForm()
		return render(request, "article/column/article_column.html", {"columns":columns,'column_form':column_form})

	if request.method == "POST":
		column_name = request.POST['column']
		columns = AriticleColumn.objects.filter(user_id=request.user.id,column=column_name)
		columns_re = AriticleColumn.objects.filter(user=request.user)
		if columns:
			return HttpResponse('2')
		#判断是否超过5个(含5个)标签
		elif(columns_re.count()>=5):
			return HttpResponse('3')
		else:
			AriticleColumn.objects.create(user=request.user, column=column_name)
			return HttpResponse("1")

#重命名文章列表名称视图
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
	column_name = request.POST["column_name"]
	column_id = request.POST['column_id']
	try:
		line = AriticleColumn.objects.get(id=column_id)
		line.column = column_name
		line.save()
		return HttpResponse("1")
	except:
		return HttpResponse("0")

#删除文章别表名称视图
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
	column_id = request.POST['column_id']
	try:
		line = AriticleColumn.objects.get(id=column_id)
		line.delete()
		return HttpResponse("1")
	except:
		return HttpResponse("2")

#发表文章视图
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
	if request.method == "POST":
		article_post_form = AriticlePostForm(data=request.POST)
		if article_post_form.is_valid():
			cd = article_post_form.cleaned_data
			try:
				new_article = article_post_form.save(commit=False)
				new_article.author = request.user
				new_article.column = request.user.article_column.get(id=request.POST['column_id'])
				new_article.save()
				return HttpResponse("1")
			except Exception as e:
				return HttpResponse("2")
		else:
			return HttpResponse("3")
	else:
		article_post_form = AriticlePostForm()
		article_columns = request.user.article_column.all()
		return render(request, "article/column/article_post.html", {"article_post_form":article_post_form, "article_columns":article_columns})

#文章列表视图
@login_required(login_url='/account/login')
def article_list(request):
	articles = AriticlePost.objects.filter(author=request.user)
	return render(request, "article/column/article_list.html", {"articles":articles})

#显示文章视图
@login_required(login_url='/account/login')
def article_detail(request,id,slug):
	article = get_object_or_404(AriticlePost, id=id, slug=slug)
	return render(request, "article/column/article_detail.html", {"article":article})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
	article_id = request.POST['article_id']
	try:
		article = AriticlePost.objects.get(id=article_id)
		article.delete()
		return HttpResponse("1")
	except Exception as e:
		return HttpResponse("2")





