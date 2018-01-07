#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-07 23:27:23
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://www.thinkheh.cn
# @Version : $Id$
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user,verb,target=None):
	#检查最后一分钟是否有相同动作
	now = timezone.now()
	last_minute = now - datetime.timedelta(seconds=60)
	similar_acitons = Action.objects.filter(user_id=user.id,verb=verb,created__gte=last_minute)

	if target:
		target_ct = ContentType.objects.get_for_model(target)
		similar_acitons = similar_acitons.filter(target_ct=target_ct,target_id=target.id)

	#如果和最后一分钟不是相同动作，就储存用户的新动作
	if not similar_acitons:

		action = Action(user=user,verb=verb,target=target)
		action.save()
		return True

	return False
