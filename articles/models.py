from django.db import models
from users.models import CommonModel, User
# Create your models here.


class Article(CommonModel):
    """ CommonModel 상속으로 데이터 생성일시는 명시할 필요 없음. """
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=50)
    content = models.TextField("Review or something")
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
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField("장르", max_length=50, unique=True)

# 장르 - 게시글 테이블
class MusicGenreTable(CommonModel):
    music = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='genre_list')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='music_list')

# data = {
#     "genres": ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]
# }

# # Genre 객체 생성
# genres = [Genre(creator=User.objects.get(id=1), name=genre) for genre in data['genres']]

# # 객체들을 한 번에 DB에 저장
# Genre.objects.bulk_create(genres)
