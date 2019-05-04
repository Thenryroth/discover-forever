import psycopg2
from contextlib import contextmanager

class DB:

    @contextmanager
    def get_conn(self):
        conn = psycopg2.connect(
                    dbname='postgres',
                    user='hudsonbuzby',
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

    def execute_insert(self,string,values):
        conn = self.get_conn()
        with conn.cursor() as curr:
            curr.execute(string,values)
            resp = curr.fetchone()[0]
            conn.commit()

        return resp
