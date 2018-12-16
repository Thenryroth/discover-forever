from flask import Flask
from flask import request,session,redirect
import requests
from requests_oauthlib import OAuth2Session
import pdb
import base64
import json
app = Flask(__name__)


client_id = '2b18dda2b5d445e4ae09f6df7f10df8a'
client_secret = '72243f3b650947e2a97f747aaeaf6d21'
authorization_base_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'

@app.route('/auth',methods=['GET'])
def hello_world():
    access_code = request.args.get('code')
    body = {
            'grant_type':'authorization_code',
            'code':access_code,
            'redirect_uri':'http://localhost:5000/auth',
            'client_id':client_id,
            'client_secret':client_secret
            }
    token = requests.post(
                            url='https://accounts.spotify.com/api/token',
                            data=body
                            ).json()
    print(token)
    header = {'Authorization':f"Bearer {token['access_token']}",'Content-Type':'application/json'}

    user = requests.get(url='https://api.spotify.com/v1/me',headers=header).json()
    print(user)
    playlists = requests.get(url='https://api.spotify.com/v1/me/playlists',headers=header).json()
    discover_forever_id = None
    for p in playlists['items']:
        if p['name'] == 'Discover Weekly':
            discover_id = p['id']
        elif p['name'] == 'Discover Forever':
            discover_forever_id = p['id']

    if not discover_forever_id:
        playlist_body = {
            "name":"Discover Forever",
            "description": "A collection of all your Discover Weekly songs",
            "public": True

            }
        new_playlist = requests.post(
                            url=f"https://api.spotify.com/v1/users/{user['id']}/playlists",
                            headers=header,
                            data=json.dumps(playlist_body)).json()
        print(new_playlist,f"https://api.spotify.com/v1/users/{user['id']}/playlists")
        discover_forever_id = new_playlist['id']
    print('discover_id-',discover_id)
    discover_forever_playlist = requests.get(url=f'https://api.spotify.com/v1/playlists/{discover_forever_id}',headers=header).json()
    tracks = requests.get(url=f'https://api.spotify.com/v1/playlists/{discover_id}/tracks',headers=header).json()
    track_ids = []
    for track in tracks['items']:
        track_ids.append(track['track']['uri'])
    tracks_body = {'uris':track_ids}
    add_songs_requests = requests.post(f'https://api.spotify.com/v1/playlists/{discover_forever_id}/tracks',
                                   headers=header,
                                   data=json.dumps(tracks_body)).json()
    return redirect(f"/success/{user['id']}/{discover_forever_playlist['name']}")



@app.route('/success/<user_id>/<playlist_id>',methods=['GET'])
def success(user_id,playlist_id):
    return f'User: {user_id} Playlist: {playlist_id}'
