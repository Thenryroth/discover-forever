import psycopg2
from contextlib import contextmanager

class DB:
    def __init__(self):
        self.dbname = "postgres"
        self.user ='postgres'
        self.password = 'postgres'
        self.host = 'localhost'
        self.port = 5432

    @contextmanager
    def get_conn(self):
        conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,

                )
        yield conn
        conn.close()


    def execute_query(self,string):
        with self.get_conn() as conn:
            with conn.cursor() as curr:
                curr.execute(string)
                return curr.fetchall()

    def execute_insert(self,string,values):
        conn = self.get_conn()
        with conn.cursor() as curr:
            curr.execute(string,values)
            resp = curr.fetchone()[0]
            conn.commit()

        return resp
