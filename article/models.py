from django.db import models
from django.contrib.auth.models import User 

class AriticleColumn(models.Model):
	user = models.ForeignKey(User,verbose_name='创建者', related_name = 'article_column')
	column = models.CharField(verbose_name='栏目',max_length=200)
	created = models.DateField(verbose_name='创建日期',auto_now_add=True)

	def __str__(self):
		return self.column

	class Meta:
		verbose_name = "栏目管理"
		verbose_name_plural = "栏目管理"

