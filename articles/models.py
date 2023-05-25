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

class Music(models.Model):
    music_id = models.CharField("MusicId", max_length=50)
    name = models.CharField("Name", max_length=50)
    artist = models.CharField("Artist",max_length=50)
    album = models.CharField("Album",max_length=50)

    def __str__(self):
        return self.name

# 장르 모델
class Genre(CommonModel):
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField("장르", max_length=50, unique=True)

# 장르 - 게시글 테이블
class MusicGenreTable(CommonModel):
    music = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='genre_list')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='music_list')

