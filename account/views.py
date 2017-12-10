from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm

def user_login(request):
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user =authenticate(username=cd['username'], password=cd['password'])
			if user:
				login(request,user)
				return HttpResponse("验证通过，欢迎登录红企家园！")
			else:
				return HttpResponse("对不起，您的用户名或密码不正确！")
		else:
			return HttpResponse("Invalid login")
	if request.method == "GET":
		login_form = LoginForm()
		return render(request, "account/login.html", {"form":login_form})

