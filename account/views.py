from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import UserInfo,UserProfile,FollowUser
from .forms import LoginForm,RegistrationForm,UserProfileForm,UserInfoForm,UserForm
from django.contrib.auth.models import User
from slugify import slugify
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from actions.utils import create_action

from imageload.models import ImageLoad

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
				new_userprofile.user_ip = request.META['REMOTE_ADDR']
				new_userprofile.save()
				UserInfo.objects.create(user=new_user)
				#记录用户动作
				create_action(new_user, '创建了账户')
				return render(request, "registration/login.html", { 'form':user_form })
		else:
			return HttpResponse("对不起，您不能注册！")
	else:
		user_form = RegistrationForm()
		userprofile_form = UserProfileForm()
		return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})

#此方法已经被django框架的自有方法替代，不起作用了
def user_login(request):
	userprofile = UserProfile.objects.get(user=request.user)
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user =authenticate(username=cd['username'], password=cd['password'])
			user_ip = request.META['REMOTE_ADDR']
			print(user_ip)
			if user:
				login(request,user)
				userprofile.user_ip =user_ip
				userprofile.save()
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
			# if UserInfo.objects.filter(SUC_code=request.POST.get('SUC_code','')):
			# 	return render(request, "account/myself_edit.html", {"msg": "统一社会信用代码不可以重复!", "user":user, "user_form":user_form,"userinfo_form":userinfo_form, "userprofile_form":userprofile_form})
			# else:
			user_cd = user_form.cleaned_data
			userprofile_cd = userprofile_form.cleaned_data
			userinfo_cd = userinfo_form.cleaned_data
			#print(user_cd["email"])
			user.email = user_cd['email']
			userprofile.birth = userprofile_cd['birth']
			userprofile.phone = userprofile_cd['phone']
			userprofile.sex = userprofile_cd['sex']
			userprofile.company_or_person = userprofile_cd['company_or_person']
			userinfo.SUC_code = userinfo_cd['SUC_code']
			userinfo.company = userinfo_cd['company']
			userinfo.profession = userinfo_cd['profession']
			userinfo.address = userinfo_cd['address']
			userinfo.aboutme = userinfo_cd['aboutme']
			user.save()
			userprofile.save()
			userinfo.save()
			#记录用户动作
			create_action(user, '修改了用户信息')
		return HttpResponseRedirect('/account/my-info/')
	else:
		user_form = UserForm(instance=request.user)
		userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone,"sex":userprofile.sex,"company_or_person":userprofile.company_or_person})
		userinfo_form = UserInfoForm(initial={"company":userinfo.company,"SUC_code":userinfo.SUC_code,"profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
		return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})

#用户列表视图
@login_required(login_url='/account/login')
def user_list(request):
	users = User.objects.filter(is_active=True)
	userinfos = UserInfo.objects.all()
	return render(request,"account/list.html",{"users":users,"userinfos":userinfos})

#用户头像视图
@login_required(login_url='/account/login')
def my_image(request):
	if request.method == 'POST':
		#img = request.POST['img']
		image_file = request.FILES.get('imgfile')
		print(image_file)
		new_filename = "{0}.{1}".format(slugify((image_file.name).rsplit('.',1)[0]),(image_file.name).rsplit('.',1)[1].lower())
		# #将组装好的新图片名称，赋值给当前上传的图片，修改名称
		image_file.name = new_filename
		print(image_file)
		userinfo = UserInfo.objects.get(user=request.user.id)
		userinfo.photo = image_file
		userinfo.save()
		return HttpResponse("1")
	else:
		return render(request,'account/imagecrop.html')

#用户关注视图函数
@csrf_exempt
@require_POST
@login_required(login_url='/account/login')
def user_follow(request):
	user_id = request.POST.get('id')
	action = request.POST.get('action')
	print(user_id,action)
	if user_id and action:
		try:
			user = User.objects.get(id=user_id)
			if action == 'follow':
				FollowUser.objects.get_or_create(user_from=request.user,user_to=user)
				#记录用户动作
				create_action(request.user, ' 关注了 ', user)
			else:
				FollowUser.objects.filter(user_from=request.user,user_to=user).delete()
				#记录用户动作
				create_action(request.user, ' 取消关注 ', user)
			return JsonResponse({'status':'ok'})
		except User.DoesNotExist:
			return JsonResponse({'status':'ko'})
	return JsonResponse({'status':'ko'})

@login_required(login_url='/account/login')
def user_detail(request,username):
	user_obj = get_object_or_404(User,username=username,is_active=True)
	userprofile = UserProfile.objects.get(user=user_obj)
	userinfo = UserInfo.objects.get(user=user_obj)
	image_list = ImageLoad.objects.filter(user=user_obj)
	return render(request,"account/detail.html",{"user_obj":user_obj,"userprofile":userprofile,"userinfo":userinfo,"image_list":image_list})



