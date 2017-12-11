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
