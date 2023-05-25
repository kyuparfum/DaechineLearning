from django.db import models
from users.models import CommonModel, User
# Create your models here.


class Article(CommonModel):
    """ CommonModel 상속으로 데이터 생성일시는 명시할 필요 없음. """
    writer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    title = models.CharField("Title", max_length=50) # required
    content = models.TextField("Review or something") # required
    image = models.ImageField("Image", blank=True, upload_to='image/')
    media = models.FileField("Media", blank=True, upload_to='media/')
    sound = models.FileField("Sound", blank=True, upload_to='music/')

    def __str__(self):
        return self.title
