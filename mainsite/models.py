from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogArticles(models.Model):
	title = models.CharField(verbose_name='标题', max_length=300)
	author = models.ForeignKey(User,verbose_name='作者', related_name="mainsite_posts")
	body = models.TextField(verbose_name='文章内容')
	publish = models.DateTimeField(verbose_name='发布时间', default=timezone.now)

	class Meta:
		ordering = ("-publish",)
		verbose_name = "文章管理"
		verbose_name_plural = "文章管理"

	def __str__(self):
		return self.title
