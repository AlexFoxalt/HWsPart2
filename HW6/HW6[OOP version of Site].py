from flask import Flask, Response, g
from webargs.flaskparser import use_kwargs
import status_codes
from utils import int_limit, genre_type
from DataBase import FDataBase, get_db

DATABASE = '../chinook.db'
DEBUG = True
dbase = None

app = Flask(__name__)
app.config.from_object(__name__)


@app.errorhandler(status_codes.HTTP_404_NOT_FOUND)
def error_404(err):
    return Response('404 Not found', status=err.code)


@app.errorhandler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
def error_422(err):
    return Response('422 Invalid parameters', status=err.code)


@app.before_request
def before_request():
    db = get_db(app)
    app.dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(err):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/greatest_hits")
@use_kwargs(int_limit, location='query')
def get_greatest_hits(count: int):
    return app.dbase.getTracks(count)


@app.route("/greatest_artists")
@use_kwargs(int_limit, location='query')
def get_greatest_artists(count: int):
    return app.dbase.getArtists(count)


@app.route("/stats_by_city")
@use_kwargs(dict(**int_limit, **genre_type), location='query')
def get_stats_by_city(count: int, genre: str):
    return app.dbase.getStats(count, genre)


if __name__ == '__main__':
    app.run()
