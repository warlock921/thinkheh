from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageLoadForm
from .models import ImageLoad
from slugify import slugify
from actions.utils import create_action

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

@login_required(login_url='/account/login')
@csrf_exempt
def upload_image_from_file(request):
	#image_count = ImageLoad.objects.filter(user_id=request.user.id)
	images = ImageLoad.objects.filter(user=request.user)
	if request.method == 'POST':
		try:
			if images.count() >= 10:
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
				return JsonResponse({'status':"2"})
			else:
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
				new_img = ImageLoad(
					user = request.user,
					title = request.POST.get('phototitle'),
					description = request.POST.get('photodescription'),
					image = request.FILES.get('img_file')
				)
				new_img.save()
				#记录用户动作
				create_action(request.user, '上传了图片', new_img)
				return JsonResponse({'status':"1"})
		except Exception as e:
			print(e)
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
			return JsonResponse({'status':"0"})
	else:
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