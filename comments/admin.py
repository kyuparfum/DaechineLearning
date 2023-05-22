from django.contrib import admin
from comments.models import Comment, Emoticon, EmoticonImages, UserBoughtEmoticon

# Register your models here.
admin.site.register(Comment)
admin.site.register(Emoticon)
admin.site.register(EmoticonImages)
admin.site.register(UserBoughtEmoticon)
