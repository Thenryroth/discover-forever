from .db import DB
class User:
    all = []

    def __init__(self,id,playlist_id,refresh_token):
        self.id = str(id)
        self.playlist_id = str(playlist_id)
        self.refresh_token = str(refresh_token)

    # This function will get a sql connection, format a string to insert a user, and then run execute query on that string
    # If this works, you should see a user in our user table in postgres
    def insert_string(self):
        return """insert into spotify.user(id, playlist_id, refresh_token)
                VALUES (%(id)s, %(playlist_id)s, %(refresh_token)s) RETURNING id """

    def select_statement(self,id):
        return """ select * from spotify.user where id = '{user_id}'
        """.format(user_id=id)

    def save_user(self):
        insert_statement = self.insert_string()
        values = {"id":self.id,"playlist_id":self.playlist_id,"refresh_token":self.refresh_token}
        return DB.execute_insert(insert_statement,values)


    def exists(self,user_id):
        select_statement = self.select_statement(user_id)

        resp = DB.execute_query(select_statement)
        return resp
