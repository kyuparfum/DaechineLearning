from django.db import models
from users.models import CommonModel

# Create your models here.
class Comment(CommonModel):
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # music = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField("댓글")

    def __str__(self):
        return self.comment
