import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageLoadForm,ImageLoadFileForm
from .models import ImageLoad
from slugify import slugify
from actions.utils import create_action

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#通过网址获取图片视图
@login_required(login_url='/account/login')
@csrf_exempt
@require_POST       #这里表示只接受POST事件
def upload_image(request):
	form = ImageLoadForm(data=request.POST)
	image_count = ImageLoad.objects.filter(user_id=request.user.id)
	#print(image_count.count())
	if form.is_valid():
		try:
			if image_count.count() >= 10:
				return JsonResponse({'status':"2"})
			else:
				new_item = form.save(commit=False)
				new_item.user = request.user
				new_item.save()
				#记录用户动作
				create_action(request.user, '上传了图片', new_item)
				return JsonResponse({'status':"1"})
		except Exception as e:
			return JsonResponse({'status':"0"})

#通过本地文件上传获取图片
@login_required(login_url='/account/login')
@csrf_exempt
def upload_image_from_file(request):
	form = ImageLoadFileForm(data=request.POST)
	#从request请求中获得上传的图片文件
	image_file = request.FILES.get('imgfile')
	#组装图片的新名称
	new_filename = "{0}.{1}".format(slugify((image_file.name).rsplit('.',1)[0]),(image_file.name).rsplit('.',1)[1].lower())
	#将组装好的新图片名称，赋值给当前上传的图片，修改名称
	image_file.name = new_filename

	image_count = ImageLoad.objects.filter(user_id=request.user.id)
	#print(image_count.count())
	if form.is_valid():
		try:
			if image_count.count() >= 10:
				return JsonResponse({'status':"2"})
			else:
				# print("进来了")
				new_item = form.save(commit=False)
				new_item.image = image_file
				# new_item.image.url = "{0}.{1}".format(slugify((new_item.image.url).rsplit('.',1)[0]),(new_item.image.url).rsplit('.',1)[1].lower())
				new_item.user = request.user
				new_item.save()
				#记录用户动作
				create_action(request.user, '上传了图片', new_item)
				return JsonResponse({'status':"1"})
		except Exception as e:
			return JsonResponse({'status':"0"})
	
#呈现上传后的图片列表
@login_required(login_url='/account/login')
def list_images(request):
	images = ImageLoad.objects.filter(user=request.user)
	paginator = Paginator(images,5)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
		image_list = current_page.object_list
	except PageNotAnInteger:
		current_page = paginator.page(1)
		image_list = current_page.object_list
	except EmptyPage:
		current_page = paginator.page(paginator.num_pages)
		image_list = current_page.object_list
	return render(request,'imageload/list_images.html',{"image_list":image_list,"page":current_page})

#删除已有图片
@login_required(login_url='/account/login')
@csrf_exempt
@require_POST       #这里表示只接受POST事件
def del_image(request):
	image_id = request.POST['image_id']
	try:
		image = ImageLoad.objects.get(id=image_id)
		image.delete()
		#记录用户动作
		create_action(request.user, '删除了图片', image)
		return JsonResponse({'status':"1"})
	except Exception as e:
		print(e)
		return JsonResponse({'status':"2"})