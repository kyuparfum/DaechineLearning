import base64
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
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
    print(access_token)
    return access_token
# 스케줄링 함수 등록
scheduler.add_job(get_token, 'interval', minutes=59)
# 스케줄링 시작
scheduler.start()

class MusicGenreApiDetail(APIView):# 음악장르 전체목록 조회
    def get(self, request):
        access_token=get_token()
        url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return JsonResponse(data, safe=False)

class MusicSearchApiDetail(APIView):# 검색 api 작업중 10:48
    def get(self, request):
        url = f"https://api.spotify.com/v1/search?q=remaster%2520track%3ADoxy%2520artist%3AMiles%2520Davis&type=album&market=KR'"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return JsonResponse(data, safe=False)



class MusicApiDetail(APIView):# 음악 api2023년 리스트 인기도순으로 정렬
    def get(self, request):
        track_info = [] 
        for i in range(0, 1000, 50):
            track_results = sp.search(q='year:2023', type='track', limit=50, offset=i)
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
    

