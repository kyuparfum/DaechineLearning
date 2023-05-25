from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from articles.models import Article
from articles.serializers import (
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
)
import base64
import requests
from rest_framework.exceptions import ParseError
from .serializers import MusicSerializer, ArtistSerializer
from django.http import JsonResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import my_settings
from apscheduler.schedulers.background import BackgroundScheduler

# 스케줄러 객체 생성
client_credentials_manager = SpotifyClientCredentials(
    client_id=my_settings.SPOTYPY_KEY["music_id"], client_secret=my_settings.SPOTYPY_KEY["music_pw"])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
client_id = my_settings.SPOTYPY_KEY["music_id"]
client_pw = my_settings.SPOTYPY_KEY["music_pw"]
access_token = ""
scheduler = BackgroundScheduler()
# Create your views here.


class GetMusicAccessToken(APIView):
    def post(self, request, format=None):
        auth_url = 'https://accounts.spotify.com/api/token'

        message = f"{client_id}:{client_pw}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        header = {'Authorization': f"Basic {base64_message}"}
        data = {'grant_type': 'client_credentials'}
        res = requests.post(auth_url, headers=header, data=data)
        response_object = res.json()
        access_token = response_object['access_token']

        my_settings.SPOTYPY_KEY["bearer_token"] = access_token
        return Response({'access_token': access_token})


def get_token():
    global access_token
    auth_url = 'https://accounts.spotify.com/api/token'
    message = f"{client_id}:{client_pw}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    header = {'Authorization': f"Basic {base64_message}"}
    data = {'grant_type': 'client_credentials'}
    res = requests.post(auth_url, headers=header, data=data)
    response_object = res.json()
    access_token = response_object['access_token']


# 스케줄링 함수 등록
get_token()
scheduler.add_job(get_token, 'interval', minutes=59)
# 스케줄링 시작
scheduler.start()


class MusicGenreApiDetail(APIView):  # 음악장르 전체목록 조회
    def get(self, request):
        url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return JsonResponse(data, safe=False)


class MusicSearchApiDetail(APIView):
    def post(self, request, format=None):
        query = request.data.get('query', None)  # 검색어는 필수로 작성해야 함.
        limit = request.data.get('limit', 10)  # 기본값은 10이라 하고 작성 가능하게 만들 예정
        # 앨범으로도 검색 가능한데 이건 트랙으로 해둬도 될 거 같습니다.
        search_type = request.data.get('type', 'track')

        if not access_token:
            get_token()

        if not query:
            raise ParseError('검색어를 입력해주세요')

        search_url = f'https://api.spotify.com/v1/search?q={query}&type={search_type}&limit={limit}'
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            artists = data.get('artists', {}).get('items', [])
            tracks_serializer = MusicSerializer(tracks, many=True)
            artists_serializer = ArtistSerializer(artists, many=True)

            for artist in artists:
                artist_id = artist.get('id')
                artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
                artist_headers = {
                    'Authorization': f'Bearer {access_token}',
                }
                artist_response = requests.get(
                    artist_url, headers=artist_headers)

                if artist_response.status_code == 200:
                    artist_data = artist_response.json()
                    artist['images'] = artist_data.get('images', [])

            return Response({
                'tracks': tracks_serializer.data,
                'artists': artists_serializer.data,
            })
        else:
            return Response({'message': '트랙을 불러 올 수 없습니다.'}, status=response.status_code)


class MusicApiDetail(APIView):  # 음악 api2023년 리스트 인기도순으로 정렬
    def get(self, request):
        track_info = []
        for i in range(0, 1000, 50):
            track_results = sp.search(
                q='year:2023', type='track', limit=50, offset=i)
            for idx, t in enumerate(sorted(track_results['tracks']['items'], key=lambda x: x['popularity'], reverse=True), start=i+1):
                try:
                    album_data = {
                        '장르': t['album']['seed_genres'],
                        'id': t['album']['id'],
                        'popularity': t['popularity'],
                        '앨범자켓': t['album']['images'],
                        '곡명': t['album']['name'],
                        '미리듣기': t['preview_url'],
                        '가수': [{
                            '스포티파이_url': a['external_urls']['spotify'],
                            '세부정보_구독이안돼서안보임': a['href'],
                            'id': a['id'],
                            '가수이름or팀이름': a['name'],
                            '직업?유형?': a['type'],
                            '스포티파이자체_주소?키값?': a['uri']} for a in t['album']['artists']],
                        # '앨범전체': t['album'],
                        # '앨범유형': t['album']['album_type'],
                        # '스포티파이_곡페이지': t['album']['external_urls']['spotify'],
                        # '세부정보_구독이안돼서안보임': t['album']['href'],

                        # '출시일': t['album']['release_date'],
                        # 'release_date_precision': t['album']['release_date_precision'],
                        # '전첵트랙수': t['album']['total_tracks'],
                        # 'type': t['album']['type'],
                        # 'uri': t['album']['uri'],
                    }
                except KeyError:
                    album_data = {
                        'id': t['album']['id'],
                        'popularity': t['popularity'],
                        'rank': idx,
                        '장르': None,
                        '앨범자켓': t['album']['images'],
                        '곡명': t['album']['name'],
                        '미리듣기': t['preview_url'],
                        '가수': [{
                            '스포티파이_url': a['external_urls']['spotify'],
                            '세부정보_구독이안돼서안보임': a['href'],
                            'id': a['id'],
                            '가수이름or팀이름': a['name'],
                            '직업?유형?': a['type'],
                            '스포티파이자체_주소?키값?': a['uri']} for a in t['album']['artists']],
                        # 'popularity': t['popularity'],
                        # '앨범유형': t['album']['album_type'],
                        # '스포티파이_곡페이지': t['album']['external_urls']['spotify'],
                        # '세부정보_구독이안돼서안보임': t['album']['href'],
                        # '출시일': t['album']['release_date'],
                        # 'release_date_precision': t['album']['release_date_precision'],
                        # '전첵트랙수': t['album']['total_tracks'],
                        # 'type': t['album']['type'],
                        # 'uri': t['album']['uri'],
                    }
                result_data = {
                    'album': album_data,
                }
                track_info.append(result_data)
        return JsonResponse(track_info, safe=False)


class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        """ GET : 생성된 모든 게시글 불러오기 """
        post = Article.objects.filter(db_status=1)
        serializer = ArticleListSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ POST : 게시글 생성하기 """
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # exception handling : title/content required


class ArticleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, article_id):
        """ GET : 특정 게시글 불러오기 """
        post = get_object_or_404(Article, id=article_id, db_status=1) # exception handling : valid article_id/db_status required
        serializer = ArticleDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, article_id):
        """ PUT : 작성자 게시글 수정하기 """
        post = get_object_or_404(Article, id=article_id, db_status=1)

        if post.writer != request.user: # exception handling : only writer(refer User FK) can delete
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleCreateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        """ DELETE : 작성자 게시글 삭제하기 """
        post = get_object_or_404(Article, id=article_id, db_status=1)

        if post.writer != request.user:
            return Response({"message": "삭제 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        else:
            post.db_status = 2
            post.save()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
