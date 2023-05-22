from django.db import models
from users.models import CommonModel, User
# Create your models here.


class Article(CommonModel):
    # CommonModel 상속으로 데이터 생성일시는 명시할 필요 없음.
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE)  # related_name 필요할까요?
    title = models.CharField("Title", max_length=50)
    content = models.TextField("Review or something")
    # image = models.ImageField("Image", blank=True, upload_to='image/')
    media = models.FileField("Media", blank=True, upload_to='media/')
    sound = models.FileField("Sound", blank=True, upload_to='music/')

    def __str__(self):
        return self.title

    # 음악-Music모델 Article 상속
    # music = models.ForeignKey(Music, on_delete=models.CASCADE)


# class Music(Article):

#     GENRES = [
#         ('rock', 'rock'),
#         ('pop', 'pop'),
#         ('jazz', 'jazz'),
#         ('classical', 'classical'),
#         ('other', 'other'),
#     ]

#     genre = models.CharField("Genre", choices=GENRES,
#                              max_length=20, default=None)
#     singer = models.CharField("Singer", max_length=20, unique=True)
#     lyrics = models.TextField("Lyrics", max_length=20, unique=True)
#     lyrics_writer = models.CharField(
#         "Lyrics Writer", max_length=20, unique=True)
#     song_writer = models.CharField("Song Writer", max_length=20, unique=True)
