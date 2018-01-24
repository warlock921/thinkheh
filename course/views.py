from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from braces.views import LoginRequiredMixin

from .models import Course

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .forms import CreateCourseForm

class AboutView(TemplateView):
	template_name = "course/about.html"

class CourseListView(ListView):
	model = Course
	context_object_name = "courses"
	template_name = 'course/course_list.html'

#这是一个用户基类
class UserMixin:
	def get_queryset(self):
		qs = super(UserMixin, self).get_queryset()
		return qs.filter(user=self.request.user)

class UserCourseMixin(UserMixin,LoginRequiredMixin):
	model = Course
	login_url = "/account/login/"

#管理视频新闻列表视图类
class ManageCourseListView(UserCourseMixin,ListView):
	context_object_name = "courses"
	template_name = 'course/manage/manage_course_list.html'

#创建视频新闻类
class CreateCourseView(UserCourseMixin,CreateView):
	fields = ['title','overview']
	template_name = 'course/manage/create_course.html'

	def post(self,request,*args,**kargs):
		form = CreateCourseForm(data=request.POST)
		if form.is_valid():
			new_course = form.save(commit=False)
			new_course.user = self.request.user
			new_course.save()
			return redirect("course:manage_course")
		return self.render_to_response({"form":form})
