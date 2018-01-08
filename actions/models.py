from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
	user = models.ForeignKey(User,verbose_name="用户",related_name='actions',db_index=True)
	verb = models.CharField(verbose_name="用户动作",max_length=255)
	target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj')
	target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
	target = GenericForeignKey('target_ct', 'target_id')
	created = models.DateTimeField(verbose_name="动作创建时间",auto_now_add=True,db_index=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = "用户动作管理"
		verbose_name_plural = "用户动作管理"
