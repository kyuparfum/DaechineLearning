from django.contrib import admin
from .models import Articles

# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at']


admin.site.register(Articles, ArticlesAdmin)