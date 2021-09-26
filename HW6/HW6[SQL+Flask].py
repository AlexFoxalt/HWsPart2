"""HW6 Чернышов Алексей [sql+flask part]"""

# ✔ 1.[done in HW5] Вывести общую длительность треков в таблице в секундах, сгруппированную по музыкальным жанрам
# ✔ 2.Вывести count самых продаваемых треков. count - необязательный параметр, ограничивает кол-во выводимых записей.
#     Если не указан, то вернуть все. Показывать поля: названия композиций, ???сумма??? и кол-во проданных копий.
# ✔ 3.Вывести count самых продаваемых исполнителей. count - необязательный параметр, если не указан, то вернуть все.
# ✔ 4.В каком городе больше всего слушают Hip-Hop? Необязательный параметр count ограничивает кол-во возвращаемых
#     городов. Так же параметр genre не обязательный.


from flask import Flask, Response, redirect, abort
from webargs.flaskparser import use_kwargs
from queries import TracksNoLimitQuery, ArtistsNoLimitQuery, TopCityByGenre, AddLimitQuery
import status_codes
from utils import int_limit, execute_query, genre_type, FormatMyResPls

app = Flask(__name__)


@app.errorhandler(status_codes.HTTP_404_NOT_FOUND)
def error(err):
    return Response('404 Not found', status=err.code)


@app.errorhandler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
def error(err):
    return Response('422 Invalid parameters', status=err.code)


@app.route("/greatest_hits")
@use_kwargs(int_limit, location='query')
def get_greatest_hits(count: int):
    if not count:
        res = execute_query(TracksNoLimitQuery)
        return FormatMyResPls(res)
    else:
        res = execute_query(TracksNoLimitQuery + AddLimitQuery, (count,))
        return FormatMyResPls(res)


@app.route("/greatest_artists")
@use_kwargs(int_limit, location='query')
def get_greatest_artists(count: int):
    if not count:
        res = execute_query(ArtistsNoLimitQuery)
        return FormatMyResPls(res)
    else:
        res = execute_query(ArtistsNoLimitQuery + AddLimitQuery, (count, ))
        return FormatMyResPls(res)


@app.route("/stats_by_city")
@use_kwargs(dict(**int_limit, **genre_type), location='query')
def get_stats_by_city(count: int, genre: str):
    if genre:
        if not count:
            res = execute_query(TopCityByGenre, (genre, ))
        else:
            res = execute_query(TopCityByGenre + AddLimitQuery, (genre, count))
    else:
        return redirect('https://everynoise.com/')
    if not res:
        abort(status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
    return FormatMyResPls(res)


if __name__ == '__main__':
    app.run(debug=True)
