from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,RegistrationForm,UserProfileForm

def register(request):
	if request.method == "POST":
		user_form = RegistrationForm(request.POST)
		userprofile_form = UserProfileForm(request.POST)
		if user_form.is_valid()*userprofile_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()

			new_userprofile = userprofile_form.save(commit=False)
			new_userprofile.user = new_user 
			new_userprofile.save()
			return HttpResponse("操作成功")
		else:
			return HttpResponse("对不起，您不能注册！")
	else:
		user_form = RegistrationForm()
		userprofile_form = UserProfileForm()
		return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})

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

