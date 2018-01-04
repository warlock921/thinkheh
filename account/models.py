from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserProfile(models.Model):
	SEX_CHOICES = (('男', '男'),('女', '女'),)
	RE_KIND = (('企业', '企业'),('个人', '个人'),)
	user = models.OneToOneField(User,unique=True)
	birth = models.DateField(blank=True,null=True)
	phone = models.CharField(max_length=11,null=True)
	sex = models.CharField(max_length=2,choices=SEX_CHOICES,default='男')
	company_or_person = models.CharField(max_length=2,choices=RE_KIND,default='个人')
	#用户ip地址
	user_ip = models.CharField(max_length=18,null=True,blank=True)
	last_article_id = models.IntegerField(null=True,blank=True)
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
	company = models.CharField(max_length=100,blank=True)
	#社会统一信用代码
	SUC_code = models.CharField(max_length=18,null=True,blank=True)
	#职业
	profession = models.CharField(max_length=100,blank=True)
	#地址
	address = models.CharField(max_length=100,blank=True)
	#自我介绍
	aboutme = models.TextField(blank=True)
	
	class Meta:
		verbose_name = "用户信息管理"
		verbose_name_plural = "用户信息管理"

	def __str__(self):
		return 'user {}'.format(self.user.username)

class FollowUser(models.Model):
	user_from = models.ForeignKey(User,related_name="rel_user_from",default=1,blank=True)
	user_to = models.ForeignKey(User,related_name="rel_user_to",default=1,blank=True)
	follow_time = models.DateTimeField(auto_now_add=True,db_index=True)

	class Meta:
		ordering = ('follow_time',)
		verbose_name = "关注用户管理"
		verbose_name_plural = "关注用户管理"

	def get_absolute_url(self):
		return reverse("account:user_detail", args=[self.username])

	def __str__(self):
		return '{} follow_user {}'.format(self.user_from,self.user_to)

User.add_to_class('following',models.ManyToManyField('self',through=FollowUser,related_name='followers',symmetrical=False))