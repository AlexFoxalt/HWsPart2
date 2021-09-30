import sqlite3
from webargs import fields

int_limit = {
    "count": fields.Int(
        required=False,
        missing=None
    )
}

genre_type = {
    "genre": fields.Str(
        required=False,
        missing=None
    )
}


def execute_query(query, args=()):
    with sqlite3.connect('../TechFiles/chinook.db') as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        records = cur.fetchall()
    return records


def FormatMyResPls(res):
    return '<br>'.join(str(num) + '. ' + str(item[0]) for num, item in enumerate(res, 1))
