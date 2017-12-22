import json
import os
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
#from slugify import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import AriticleColumnForm,AriticlePostForm
from .models import AriticleColumn,AriticlePost

#话题标签视图
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

#重命名话题标签视图
@login_required(login_url='/account/login')
@require_POST       #这里表示只接受POST事件
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

#删除话题标签视图
@login_required(login_url='/account/login')
@require_POST       #这里表示只接受POST事件
@csrf_exempt
def del_article_column(request):
	column_id = request.POST['column_id']
	try:
		line = AriticleColumn.objects.get(id=column_id)
		line.delete()
		return HttpResponse("1")
	except:
		return HttpResponse("2")

#发布话题视图
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

#已发布话题列表视图
@login_required(login_url='/account/login')
def article_list(request):
	articles_list = AriticlePost.objects.filter(author=request.user)
	paginator = Paginator(articles_list,5)
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
	return render(request, "article/column/article_list.html", {"articles":articles, "page":current_page})

#显示话题正文视图
@login_required(login_url='/account/login')
def article_detail(request,id,slug):
	article = get_object_or_404(AriticlePost, id=id, slug=slug)
	return render(request, "article/column/article_detail.html", {"article":article})

#删除话题视图
@login_required(login_url='/account/login')
@require_POST   #这里表示只接受POST事件
@csrf_exempt
def del_article(request):
	article_id = request.POST['article_id']
	try:
		article = AriticlePost.objects.get(id=article_id)
		article.delete()
		return HttpResponse("1")
	except Exception as e:
		return HttpResponse("2")

#编辑话题视图
@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request,article_id):
	if request.method == "GET":
		article_columns = request.user.article_column.all()
		article = AriticlePost.objects.get(id=article_id)
		this_article_form = AriticlePostForm(initial={"title":article.title})
		this_article_column = article_column
		return render(request, "article/column/redit_article.html", {"article":article, "article_columns":article_columns, "this_article_column":this_article_column, "this_article_form":this_article_form})

	else:
		redit_article = AriticlePost.objects.get(id=article_id)
		try:
			redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
			redit_article.title = request.POST['title']
			redit_article.body = request.POST['body']
			redit_article.save()
			return HttpResponse("1")
		except Exception as e:
			return HttpResponse("2")

#富文本编辑器图片上传处理
@login_required(login_url='/account/login')
@require_POST   #这里表示只接受POST事件
@csrf_exempt
def editor_image_upload(request):
	response_data = {}
	if request.method == "POST":
		upload_image_file = request.FILES.get('editormd-image-file')
		#print(upload_image_file.name,upload_image_file.size)
		#取文件的扩展名
		file_ext = os.path.splitext(upload_image_file.name)[1]
		new_upload_image_file = timezone.now().strftime('%Y%m%d%H%M%S') + file_ext
		print(new_upload_image_file)
		if not upload_image_file:
			response_data['success'] = 0
			response_data['message'] = u'图片格式异常'
			return HttpResponse(json.dumps(response_data),content_type="application/json")
		else:
			if upload_image_file.size < 5242880 :
				#按年和按日期建立图片文件夹，文件夹不存在，会自动创建
				up_year = timezone.now().strftime('%Y')
				up_date = timezone.now().strftime('%m')+"-"+timezone.now().strftime('%d')
				#组装图片路径并上传图片至服务器
				img_url = default_storage.save("editor_images"+"/"+request.user.username+"/"+up_year+"/"+up_date+"/"+new_upload_image_file,ContentFile(upload_image_file.read()))
				# tmp_file = os.path.join(settings.MEDIA_ROOT,img_url).replace('\\','/')	  #调试信息
				# upload_image_file.save(os.path.join(settings.BASE_DIR,'static/editor_up_load/%Y/%m/%d',new_upload_image_file))
				# print(img_url)  #调试信息
				# print(tmp_file)  #调试信息
				response_data['success'] = 1
				response_data['message'] = u'上传成功'
				#这里非常重要，路径一定不能修改，否则无法正常显示图片
				response_data['url'] = '/static/image_upload/'+img_url
				#response_data = {'success':1,'message':"上传成功",'url':'http://www.thinkheh.cn'}  ----样例
				return HttpResponse(json.dumps(response_data),content_type="application/json")
			else:
				response_data['success'] = 0
				response_data['message'] = u'图片大小超过 5 Mb'
				return HttpResponse(json.dumps(response_data),content_type="application/json")