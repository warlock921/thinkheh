from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User,unique=True)
	birth = models.DateField(blank=True,null=True)
	phone = models.CharField(max_length=20,null=True)
	# ID_card = models.CharField(max_length=18,null=True)
	# company_name = models.CharField(max_length=300,null=True,blank=True)

	class Meta:
		verbose_name = "用户管理"
		verbose_name_plural = "用户管理"

	def __str__(self):
		return 'user {}'.format(self.user.username)

class UserInfo(models.Model):
	user = models.OneToOneField(User,unique=True)
	#公司名称
	company = models.CharField(max_length=100,null=True)
	#社会统一信用代码
	SUC_code = models.CharField(max_length=18,null=True)
	#职业
	profession = models.CharField(max_length=100,null=True)
	#地址
	address = models.CharField(max_length=100,null=True)
	#自我介绍
	aboutme = models.TextField(null=True)

	class Meta:
		verbose_name = "用户信息管理"
		verbose_name_plural = "用户信息管理"

	def __str__(self):
		return 'user {}'.format(self.user.username)
