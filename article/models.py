from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify

#栏目设置数据库模型
class AriticleColumn(models.Model):
	user = models.ForeignKey(User,verbose_name='创建者', related_name = 'article_column')
	column = models.CharField(verbose_name='私有栏目名称',max_length=200)
	created = models.DateField(verbose_name='创建日期',auto_now_add=True)

	def __str__(self):
		return self.column

	class Meta:
		verbose_name = "私有栏目管理"
		verbose_name_plural = "私有栏目管理"

#问题标签---注意：这个类必须放在AriticlePost的前面
class ArticleTag(models.Model):
	author = models.ForeignKey(User,verbose_name="用户名", related_name="tag")
	tag = models.CharField(verbose_name="问题标签", max_length=24)

	def __str__(self):
		return self.tag

#问答主题发布-数据库模型
class AriticlePost(models.Model):
	author = models.ForeignKey(User,verbose_name="作者",related_name="article")
	title = models.CharField(verbose_name="话题名称", max_length=200)
	#重要的标志
	slug = models.SlugField(verbose_name="地址", max_length=500)
	column = models.ForeignKey(AriticleColumn, verbose_name="话题栏目名称", related_name="article_column")
	body = models.TextField(verbose_name="话题内容")
	created = models.DateTimeField(verbose_name="创建日期", default=timezone.now)
	updated = models.DateTimeField(verbose_name="更新日期", auto_now=True)
	users_like = models.ManyToManyField(User,verbose_name="点赞数", related_name="articles_like", blank=True)
	article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)
	
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

	def get_url_path(self):
		return reverse("article:list_article_detail", args=[self.id,self.slug])

#问题评论或答案发布-数据库模型
class Comment(models.Model):
	article = models.ForeignKey(AriticlePost,verbose_name="问题外键", related_name="comments")
	commentator = models.CharField(max_length=90)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	#is_best_answer = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return "Comment by {0} on {1}".format(self.commentator,self.article)

class FollowUser(models.Model):
	#用户关注的其他用户
	follow_user = models.ForeignKey(User,verbose_name="用户关注的其他用户", related_name="user_follow")
	#是否已经关注
	follow_flag = models.BooleanField(default=False)
	#关注的时间
	follow_time = models.DateTimeField(verbose_name="关注日期", default=timezone.now)
	#取关的时间
	unfollow_time = models.DateTimeField(verbose_name="取关日期", auto_now=True)

	class Meta:
		ordering = ('-follow_time',)

	def __str__(self):
		return self.follow_user
		


		