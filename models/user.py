import psycopg2
from contextlib import contextmanager
class User:
    all = []

    def __init__(self,id,playlist_id,refresh_token):
        self.id = id
        self.playlist_id = playlist_id
        self.refresh_token = refresh_token

    @contextmanager
    def get_conn(self):
        conn = psycopg2.connect(
                    dbname='postgres',
                    user='postgres',
                    password='postgres',
                    host='localhost',
                    port=5432,

                )
        yield conn
        conn.close()


    def execute_query(self,string):
        with self.get_conn() as conn:
            with conn.cursor() as curr:
                curr.execute(string)
                return curr.fetchall()
    def execute_insert(self,string):
        conn = self.get_conn()
        with conn.cursor() as curr:
            curr.execute(string,values)
            resp = curr.fetchone()[0]
            conn.commit()
        return resp
    # This function will get a sql connection, format a string to insert a user, and then run execute query on that string
    # If this works, you should see a user in our user table in postgres
    def insert_string(self):
        return """insert into spotify.user (id, playlist_id, refresh_token)
                VALUES (%(id)s, $(playlist_id)s, $(refresh_token)s) RETURNING id)"""

    def select_statement(self,id):
        return """ select * from spotify.user where id = '{user_id}'
        """.format(user_id=id)

    def save_user(self):
        insert_statement = self.insert_string()
        values = {"id":self.id,"playlist_id":self.playlist_id,"refresh_token":self.refresh_token}
        self.execute_insert(insert_statement,values)


    def exists(self,user_id):
        select_statement = self.select_statement(user_id)

        resp = self.execute_query(select_statement)
        return resp
