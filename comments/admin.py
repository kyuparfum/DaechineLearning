from django.contrib import admin
from comments.models import Comment
from comments.models import Emoticon
from comments.models import EmoticonImages

# Register your models here.
admin.site.register(Comment)
admin.site.register(Emoticon)
admin.site.register(EmoticonImages)
