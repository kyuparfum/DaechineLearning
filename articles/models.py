from django.db import models
from users.models import CommonModel
# Create your models here.


class Article(CommonModel):
    # 작성자-User모델
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)  #related_name 필요할까요?
    # 음악-Music모델
    # music = models.ForeignKey(Music, on_delete=models.CASCADE)
    content = models.TextField("후기")
    

    # def __str__(self):
    #     return self.music