from .db import DB
import requests
import json
class Playlist:
    all = []

    def __init__(self,id,discover_weekly_id):
        #discover forever id that we created
        self.id = id
        #discover weekly playlist updated by spotify
        self.discover_weekly_id = discover_weekly_id

    # This function will get a sql connection, format a string to insert a user, and then run execute query on that string
    # If this works, you should see a user in our user table in postgres
    def insert_string(self):
        return """insert into spotify.user (id, playlist_id, refresh_token)
                VALUES ('{id}', '{playlist_id}')
        """.format(id=self.id, playlist_id=self.playlist_id, refresh_token=self.refresh_token)

    def select_statement(self,id):
        return """ select * from spotify.user where id = '{user_id}'
        """.format(user_id=id)

    def select_all_statement(self):
        return """ select * from spotify.user u
        inner join spotify.playlist p
        on u.playlist_id = p.id """
    def save_user(self):
        db = DB()
        insert_statement = self.insert_string()
        return db.execute_query(insert_statement)


    def exists(self,user_id):
        db = DB()
        select_statement = self.select_statement(user_id)
        resp = db.execute_query(select_statement)
        return resp

    def update_tracks(self,header):
        tracks = requests.get(
                    url=f'https://api.spotify.com/v1/playlists/{self.discover_weekly_id}/tracks',
                    headers=header).json()
        track_ids = []
        for track in tracks['items']:
            track_ids.append(track['track']['uri'])
        tracks_body = {'uris':track_ids}
        add_songs_requests = requests.post(f'https://api.spotify.com/v1/playlists/{self.id}/tracks',
                                       headers=header,
                                       data=json.dumps(tracks_body)).json()

    def update_all(self):
        db = DB()
        users = db.execute_query(self.select_all_statement)
        ## this returns an array of users
