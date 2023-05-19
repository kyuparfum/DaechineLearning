from django.db import models

# Create your models here.
class Comment(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
