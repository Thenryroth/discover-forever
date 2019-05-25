from flask import Flask
from flask import request,session,redirect
import requests
from requests_oauthlib import OAuth2Session
import pdb
import base64
import json
from models import User,Playlist
app = Flask(__name__)


client_id = '2b18dda2b5d445e4ae09f6df7f10df8a'
client_secret = '72243f3b650947e2a97f747aaeaf6d21'
authorization_base_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'

@app.route('/auth',methods=['GET'])
def hello_world():
    access_code = request.args.get('code')
    #####
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
    access_token = token['access_token']
    refresh_token = token['refresh_token']
    header = {'Authorization':f"Bearer {access_token}",'Content-Type':'application/json'}

    user = requests.get(url='https://api.spotify.com/v1/me',headers=header).json()
    user_id = user['id']
    # print(user)
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
        discover_forever_id = new_playlist['id']
    new_user = User(user_id,discover_forever_id,refresh_token)
    if not new_user.exists(new_user.id):
        new_user.save_user()
    forever_playlist = Playlist(discover_forever_id,discover_id)

    if not forever_playlist.exists(forever_playlist.id):
        forever_playlist.save_playlist()
    discover_forever_playlist = requests.get(
            url=f'https://api.spotify.com/v1/playlists/{discover_forever_id}',
            headers=header).json()
    new_playlist.save_tracks(header)

    return redirect(f"/success/{user['id']}/{discover_forever_playlist['name']}")



@app.route('/success/<user_id>/<playlist_id>',methods=['GET'])
def success(user_id,playlist_id):
    return f'User: {user_id} Playlist: {playlist_id}'
