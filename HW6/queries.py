TracksNoLimitQuery = """
SELECT tracks.Name, (tracks.UnitPrice * invoice_items.Quantity) as Summ, invoice_items.Quantity
FROM tracks
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
ORDER BY invoice_items.Quantity DESC
"""

ArtistsNoLimitQuery = """
SELECT tracks.Composer
FROM tracks
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
GROUP BY tracks.Composer
ORDER BY invoice_items.Quantity DESC
"""


TopCityByGenre = """
SELECT invoices.BillingCity as city
FROM tracks
INNER JOIN genres ON tracks.GenreId = genres.GenreId
INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId
INNER JOIN invoices ON invoice_items.InvoiceId = invoices.InvoiceId
WHERE genres.Name = ?
GROUP BY invoices.BillingCity
ORDER BY count(genres.Name) DESC
"""


AddLimitQuery = """
LIMIT ?
"""

