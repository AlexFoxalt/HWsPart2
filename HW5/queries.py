from utils import execute_query

UniqueNameQuery = 'SELECT COUNT ( DISTINCT FirstName ) AS counter FROM customers'

TracksCountQuery = 'SELECT count( Name ) AS counter FROM tracks'

CustomersNoParamQuery = 'SELECT * FROM customers '

GenresQuery = "SELECT ( SUM ( tracks.Milliseconds ) / 1000 ), genres.Name " \
              "FROM tracks " \
              "INNER JOIN genres ON tracks.GenreId=genres.GenreId " \
              "GROUP BY tracks.GenreId"

GetFieldsQuery = "SELECT name FROM PRAGMA_TABLE_INFO( 'customers' )"


def add_params_to_customers_query(text: str):
    """
    Generate SQL request to DB with filter.

    :param text: Filter as str
    :return: SQL request as str
    """

    Fields = execute_query(GetFieldsQuery)

    start = 'WHERE '
    query = []

    for field in Fields:
        query.append(f"{field[0]} LIKE ('%{text}%')")

    return start + ' OR '.join(query)


def add_params_to_sales_query(arg1: str, arg2: str):
    """
    Generate SQL request to DB with two arguments which will need to be multiplied

    :param arg1: First multiplier as name of column from DB as str
    :param arg2: Second multiplier as name of column from DB as str
    :return: SQL request as str
    """
    return f"SELECT sum({arg1} * {arg2}) as total from invoice_items"
