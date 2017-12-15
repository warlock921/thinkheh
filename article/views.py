from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .forms import AriticleColumnForm
from .models import AriticleColumn

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
		if columns:
			return HttpResponse('2')
		else:
			AriticleColumn.objects.create(user=request.user, column=column_name)
			return HttpResponse("1")

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