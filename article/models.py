from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify

#栏目设置数据库模型
class AriticleColumn(models.Model):
	user = models.ForeignKey(User,verbose_name='创建者', related_name = 'article_column')
	column = models.CharField(verbose_name='栏目',max_length=200)
	created = models.DateField(verbose_name='创建日期',auto_now_add=True)

	def __str__(self):
		return self.column

	class Meta:
		verbose_name = "栏目管理"
		verbose_name_plural = "栏目管理"

#栏目文章发送数据库模型
class AriticlePost(models.Model):
	author = models.ForeignKey(User,verbose_name="作者",related_name="article")
	title = models.CharField(verbose_name="文章标题", max_length=200)
	#重要的标志
	slug = models.SlugField(verbose_name="段塞", max_length=500)
	column = models.ForeignKey(AriticleColumn, verbose_name="栏目标题ID", related_name="article_column")
	body = models.TextField(verbose_name="文章内容")
	created = models.DateTimeField(verbose_name="创建日期", default=timezone.now())
	updated = models.DateTimeField(verbose_name="更新日期", auto_now=True)
	
	class Meta:
		ordering = ("-updated",)
		index_together = (('id','slug'),)

	def __str__(self):
		return self.title

	def save(self,*args, **kargs):
		self.slug = slugify(self.title)
		super(AriticlePost,self).save(*args, **kargs)

	def get_absolute_url(self):
		return reverse("article:article_detail", args=[self.id,self.slug])

