import sqlite3

'''
Generic db connection provider
'''


class DBbase:

    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        raise NotImplementedError()

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn


class Netflix(DBbase):

    def __init__(self):
        super().__init__("projects/movies/Movies.sqlite")

    def reset_database(self):
        # this must run once.
        try:
            super().connect()
            sql = """
                DROP TABLE IF EXISTS NetflixMovies;

                CREATE TABLE NetflixMovies (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    imdb_id TEXT,
                    title TEXT, 
                    certificate TEXT,
                    score TEXT,
                    genres TEXT,
                    runtime TEXT,
                    cover TEXT
                    );
                """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, movie_info):
        try:
            super().connect()
            super().get_cursor.execute("""Insert into NetflixMovies (imdb_id, title, certificate, score, genres, runtime, cover) values (?, ?, ?, ?, ?, ?, ?);""", (movie_info['id'], movie_info['title'], movie_info['certificate'], movie_info['score'], movie_info['genres'], movie_info['runtime'], movie_info['cover']))
            super().get_connection.commit()
            super().close_db()
            print(f"added {movie_info['title']} successfully")

        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()
