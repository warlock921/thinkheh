from django.contrib import admin
from .models import AriticleColumn

class AriticleColumnAdmin(admin.ModelAdmin):
	list_display = ('column', 'created', 'user')
	list_filter = ('column',)

admin.site.register(AriticleColumn,AriticleColumnAdmin)

