import sqlite3
from flask import Flask, Response, g
from webargs.flaskparser import use_kwargs
import status_codes
from utils import int_limit, int_limit_and_genre_type
from DataBase import FDataBase

DATABASE = '../chinook.db'
DEBUG = True
dbase = None

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    """Find our DB in local files"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Set connection with DB if it not exists"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.errorhandler(status_codes.HTTP_404_NOT_FOUND)
def error(err):
    return Response('404 Not found', status=err.code)


@app.errorhandler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
def error(err):
    return Response('422 Invalid parameters', status=err.code)


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/greatest_hits")
@use_kwargs(int_limit, location='query')
def get_greatest_hits(limit: int):
    return dbase.getTracks(limit)


@app.route("/greatest_artists")
@use_kwargs(int_limit, location='query')
def get_greatest_artists(limit: int):
    return dbase.getArtists(limit)


@app.route("/stats_by_city")
@use_kwargs(int_limit_and_genre_type, location='query')
def get_stats_by_city(limit: int, genre: str):
    return dbase.getStats(limit, genre)


if __name__ == '__main__':
    app.run()
