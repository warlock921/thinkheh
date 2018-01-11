from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageLoadForm
from .models import ImageLoad

@login_required(login_url='/account/login')
@csrf_exempt
@require_POST       #这里表示只接受POST事件
def upload_image(request):
	form = ImageForm(data=request.POST)
	if form.is_valid():
		try:
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
			return JsonResponse({'status':"1"})
		except Exception as e:
			return JsonResponse({'status':"0"})

@login_required(login_url='/account/login')
def list_images(request):
	images = ImageLoad.objects.filter(user=request.user)
	return render(request,'imageload/list_images.html',{"images":images})
