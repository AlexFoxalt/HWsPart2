from flask import abort, redirect
from queries import TracksNoLimitQuery, ArtistsNoLimitQuery, TopCityByGenre, AddLimitQuery
from utils import FormatMyResPls


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getTracks(self, limit):
        if limit:
            self.__cur.execute(TracksNoLimitQuery + AddLimitQuery, (limit, ))
        else:
            self.__cur.execute(TracksNoLimitQuery)
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)

    def getArtists(self, limit):
        if limit:
            self.__cur.execute(ArtistsNoLimitQuery + AddLimitQuery, (limit, ))
        else:
            self.__cur.execute(ArtistsNoLimitQuery)
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)

    def getStats(self, limit, genre):
        if genre:
            if limit:
                self.__cur.execute(TopCityByGenre + AddLimitQuery, (genre, limit))
            else:
                self.__cur.execute(TopCityByGenre, (genre, ))
        else:
            return redirect('https://everynoise.com/')
        res = self.__cur.fetchall()
        if res:
            return FormatMyResPls(res)
        else:
            return abort(422)
