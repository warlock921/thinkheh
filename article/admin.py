from django.contrib import admin
from .models import AriticleColumn,ArticleTag,AriticlePost,Comment

class AriticleColumnAdmin(admin.ModelAdmin):
	list_display = ('column', 'created', 'user')
	list_filter = ('column',)

class ArticleTagAdmin(admin.ModelAdmin):
	list_display = ('author','tag')
	list_filter = ('author',)

class AriticlePostAdmin(admin.ModelAdmin):
	list_display = ('author','title','slug','column','body','created','updated')
	list_filter = ('author','title','created','updated',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('article','commentator','body','created')
	list_filter = ('commentator','created',)

admin.site.register(AriticleColumn,AriticleColumnAdmin)
admin.site.register(ArticleTag,ArticleTagAdmin)
admin.site.register(AriticlePost,AriticlePostAdmin)
admin.site.register(Comment,CommentAdmin)


