UniqueNameQuery = 'SELECT COUNT ( DISTINCT FirstName ) AS counter FROM customers'

TracksCountQuery = 'SELECT count( Name ) AS counter FROM tracks'

CustomersNoParamQuery = 'SELECT * FROM customers '

GenresQuery = "SELECT ( SUM ( tracks.Milliseconds ) / 6000 ), genres.Name " \
            "FROM tracks " \
            "INNER JOIN genres ON tracks.GenreId=genres.GenreId " \
            "GROUP BY tracks.GenreId"

GetFieldsQuery = "SELECT name FROM PRAGMA_TABLE_INFO( 'customers' )"


def add_params_to_customers_query(text: str):
    return f"WHERE FirstName IN ('{text}') OR " \
           f"LastName IN ('{text}') OR " \
           f"Company IN ('{text}') OR " \
           f"Address IN ('{text}') OR " \
           f"City IN ('{text}') OR " \
           f"State IN ('{text}') OR " \
           f"Country IN ('{text}')"


def add_params_to_sales_query(arg1: str, arg2: str):
    return f"SELECT sum({arg1} * {arg2}) as total from invoice_items"
