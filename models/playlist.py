class Playlist:
    all = []

    def __init__(self,id,discover_weekly_id):
        self.id = id
        self.discover_weekly_id = discover_weekly_id

    def get_conn(self):
        conn = psycopg2.connect(
                    dbname='postgres',
                    user='postgres',
                    password='postgres',
                    host='localhost',
                    port=5432,

                )
        return conn

    def execute_query(self,string):
        conn = self.get_conn()
        with conn.cursor() as curr:
            curr.execute(string)
            resp = curr.fetchone()
            conn.commit()
            return resp



    # This function will get a sql connection, format a string to insert a user, and then run execute query on that string
    # If this works, you should see a user in our user table in postgres
    def insert_string(self):
        return """insert into spotify.user (id, playlist_id, refresh_token)
                VALUES ('{id}', '{playlist_id}', '{refresh_token}')
        """.format(id=self.id, playlist_id=self.playlist_id, refresh_token=self.refresh_token)

    def select_statement(self,id):
        return """ select * from spotify.user where id = '{user_id}'
        """.format(user_id=id)

    def save_user(self):
        insert_statement = self.insert_string()
        self.execute_query(insert_statement)


    def exists(self,user_id):
        select_statement = self.select_statement(user_id)

        resp = self.execute_query(select_statement)
        return resp
