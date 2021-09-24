import sqlite3
from webargs import fields

int_limit = {
    "limit": fields.Int(
        required=False,
        missing=None
    )
}

int_limit_and_genre_type = {
    "limit": fields.Int(
        required=False,
        missing=None
    ),
    "genre": fields.Str(
        required=False,
        missing=None
    )
}


def execute_query(query, args=()):
    with sqlite3.connect('../chinook.db') as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        records = cur.fetchall()
    return records


def FormatMyResPls(res):
    return '<br>'.join(str(num + 1) + '. ' + str(item[0]) for num, item in enumerate(res))
