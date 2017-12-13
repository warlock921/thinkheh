from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import UserInfo,UserProfile 
from .forms import LoginForm,RegistrationForm,UserProfileForm,UserInfoForm,UserForm
from django.contrib.auth.models import User

def register(request):
	if request.method == "POST":
		user_form = RegistrationForm(request.POST)
		userprofile_form = UserProfileForm(request.POST)
		
		if user_form.is_valid()*userprofile_form.is_valid():
			#读取用户输入的email地址
			is_new_email = request.POST.get('email','')
			#判断邮件是否重复注册
			if User.objects.filter(email=is_new_email):
				#如果邮件重复，不允许注册，中断注册流程
				return render(request, "account/register.html", {'msg': '邮件重复，请更换其他邮件地址!', 'form':user_form, 'profile':userprofile_form})
			#如果不重复，存入数据库
			else:
				new_user = user_form.save(commit=False)
				new_user.set_password(user_form.cleaned_data['password'])
				new_user.save()

				new_userprofile = userprofile_form.save(commit=False)
				new_userprofile.user = new_user 
				new_userprofile.save()
				UserInfo.objects.create(user=new_user)
				return render(request, "registration/login.html", { 'form':user_form })
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

@login_required(login_url='/account/login')
def myself(request):
	user = User.objects.get(username=request.user.username)
	userprofile = UserProfile.objects.get(user=user)
	userinfo = UserInfo.objects.get(user=user)
	return render(request, "account/myself.html", {"user":user, "userinfo":userinfo, "userprofile":userprofile})

@login_required(login_url='/account/login')
def myself_edit(request):
	user = User.objects.get(username=request.user.username)
	userprofile = UserProfile.objects.get(user=request.user)
	userinfo = UserInfo.objects.get(user=request.user)

	if request.method == "POST":
		user_form = UserForm(request.POST)
		userprofile_form = UserProfileForm(request.POST)
		userinfo_form = UserInfoForm(request.POST)
		if user_form.is_valid()*userprofile_form.is_valid()*userinfo_form.is_valid():
			user_cd = user_form.cleaned_data
			userprofile_cd = userprofile_form.cleaned_data
			userinfo_cd = userinfo_form.cleaned_data
			#print(user_cd["email"])
			user.email = user_cd['email']
			userprofile.birth = userprofile_cd['birth']
			userprofile.phone = userprofile_cd['phone']
			userinfo.company = userinfo_cd['company']
			userinfo.SUC_code = userinfo_cd['SUC_code']
			userinfo.profession = userinfo_cd['profession']
			userinfo.address = userinfo_cd['address']
			userinfo.aboutme = userinfo_cd['aboutme']
			user.save()
			userprofile.save()
			userinfo.save()
		return HttpResponseRedirect('/account/my-info/')
	else:
		user_form = UserForm(instance=request.user)
		userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
		userinfo_form = UserInfoForm(initial={"company":userinfo.company,"SUC_code":userinfo.SUC_code,"profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
		return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})
