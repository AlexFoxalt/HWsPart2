import sqlite3

from flask import abort, redirect, g
from queries import TracksNoLimitQuery, ArtistsNoLimitQuery, TopCityByGenre, AddLimitQuery
from utils import FormatMyResPls


def connect_db(app):
    """Find our DB in local files"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db(app):
    """Set connection with DB if it not exists"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db(app)
    return g.link_db


class FDataBase:
    def __init__(self, db):
        self.__cur = db.cursor()

    def getTracks(self, count):
        if count:
            self.__cur.execute(TracksNoLimitQuery + AddLimitQuery, (count, ))
        else:
            self.__cur.execute(TracksNoLimitQuery)
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)

    def getArtists(self, count):
        if count:
            self.__cur.execute(ArtistsNoLimitQuery + AddLimitQuery, (count, ))
        else:
            self.__cur.execute(ArtistsNoLimitQuery)
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)

    def getStats(self, count, genre):
        if genre:
            if count:
                self.__cur.execute(TopCityByGenre + AddLimitQuery, (genre, count))
            else:
                self.__cur.execute(TopCityByGenre, (genre, ))
        else:
            return redirect('https://everynoise.com/')
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)
