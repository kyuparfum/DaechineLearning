from django.contrib import admin
from .models import Article, Music

# Register your models here.
# class ArticlesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'content', 'created_at']


admin.site.register(Article)
admin.site.register(Music)
